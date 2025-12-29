from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from typing import Optional
from contextlib import asynccontextmanager

from database import Base, engine, get_db
from schema import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse,
    PrioritySuggestion,
    ChatRequest,
    ChatResponse,
    AIParseRequest,
    AIParseResponse
)
from security import hash_password, verify_password, create_access_token
from auth import get_current_user
from models import TaskDB, UserDB, TaskStatus
from sqlalchemy.exc import IntegrityError
from config import CORS_ORIGINS
from ai_assistant import (
    generate_task_summary,
    suggest_priorities,
    generate_daily_plan,
    chat_with_task_context,
    parse_task_draft
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------- AI ASSISTANT (READ-ONLY, ADVISORY) ----------------

@app.get("/ai/task-summary")
def get_task_summary(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a human-readable summary of user's tasks.
    
    This is READ-ONLY - it only summarizes, never modifies data.
    LLM is used as an assistive layer for user understanding.
    """
    # Fetch user's tasks
    tasks = db.query(TaskDB).filter(TaskDB.user_id == current_user.id).all()
    
    # Convert to dict format
    task_dicts = [
        {
            "title": task.title,
            "status": task.status,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "description": task.description
        }
        for task in tasks
    ]
    
    # Generate summary
    summary = generate_task_summary(task_dicts)
    
    return {"summary": summary}


@app.get("/ai/priorities", response_model=PrioritySuggestion)
def get_priority_suggestions(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Suggest task priorities based on due dates and status.
    
    This is ADVISORY - backend still controls actual priority.
    LLM suggests, user decides, backend enforces.
    """
    # Fetch user's tasks
    tasks = db.query(TaskDB).filter(TaskDB.user_id == current_user.id).all()
    
    # Convert to dict format
    task_dicts = [
        {
            "title": task.title,
            "status": task.status,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "description": task.description
        }
        for task in tasks
    ]
    
    # Get suggestions
    suggestions = suggest_priorities(task_dicts)
    
    return PrioritySuggestion(**suggestions)


@app.post("/ai/task-draft", response_model=AIParseResponse)
def create_task_draft(
    request: AIParseRequest,
    current_user: UserDB = Depends(get_current_user)
):
    """
    Parse natural language into a task DRAFT. (Use Case 3)
    """
    draft = parse_task_draft(request.text)
    
    # Parse due_date string to datetime if present
    due_date_dt = None
    if draft.get("due_date"):
        try:
             # Handle YYYY-MM-DD
            due_date_dt = datetime.strptime(draft["due_date"], "%Y-%m-%d")
        except:
            pass

    return AIParseResponse(
        title=draft["title"],
        description=draft.get("description"),
        due_date=due_date_dt,
        confidence=draft.get("confidence", 0.5)
    )


@app.post("/ai/chat", response_model=ChatResponse)
def chat_ai(
    request: ChatRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with the AI Assistant about your tasks.
    """
    # Fetch recent tasks for context
    tasks = db.query(TaskDB).filter(TaskDB.user_id == current_user.id).order_by(TaskDB.id.desc()).limit(20).all()
    
    # Serialize tasks for the context window
    task_list = []
    for t in tasks:
        task_list.append({
            "title": t.title,
            "status": t.status,
            "due_date": t.due_date.strftime("%Y-%m-%d") if t.due_date else "No Date"
        })
    
    reply = chat_with_task_context(request.message, task_list)
    return ChatResponse(reply=reply)


@app.get("/ai/daily-plan")
def get_daily_plan(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a daily planning summary combining summary + priorities.
    
    This is READ-ONLY assistance for user planning.
    """
    # Fetch user's tasks
    tasks = db.query(TaskDB).filter(TaskDB.user_id == current_user.id).all()
    
    # Convert to dict format
    task_dicts = [
        {
            "title": task.title,
            "status": task.status,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "description": task.description
        }
        for task in tasks
    ]
    
    # Generate daily plan
    plan = generate_daily_plan(task_dicts)
    
    return {"plan": plan}


# ---------------- TASKS ---------------- #

@app.post("/tasks/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    try:
        now = datetime.now(timezone.utc)

        db_task = TaskDB(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status=TaskStatus.pending.value,
            created_at=now,
            updated_at=now,
            user_id=current_user.id
        )

        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@app.get("/tasks", response_model=list[TaskResponse])
def read_tasks(
    overdue: Optional[bool] = Query(default=None),
    today: Optional[bool] = Query(default=None),
    upcoming: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # ✅ FIX: DO NOT FILTER STATUS HERE
    query = db.query(TaskDB).filter(
        TaskDB.user_id == current_user.id
    )

    today_date = datetime.now(timezone.utc).date()
    start_of_today = datetime.combine(today_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_of_today = datetime.combine(today_date, datetime.max.time()).replace(tzinfo=timezone.utc)

    if overdue:
        query = query.filter(
            TaskDB.due_date.isnot(None),
            TaskDB.due_date < start_of_today
        )

    if today:
        query = query.filter(
            TaskDB.due_date.isnot(None),
            TaskDB.due_date >= start_of_today,
            TaskDB.due_date <= end_of_today
        )

    if upcoming is not None:
        end_date = datetime.combine(
            today_date + timedelta(days=upcoming),
            datetime.max.time()
        ).replace(tzinfo=timezone.utc)

        query = query.filter(
            TaskDB.due_date.isnot(None),
            TaskDB.due_date > start_of_today,
            TaskDB.due_date <= end_date
        )

    return query.all()


# ✅ FIX: GENERIC UPDATE MUST BE PATCH
@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    task = db.query(TaskDB).filter(
        TaskDB.id == task_id,
        TaskDB.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Use model_dump for Pydantic v2, fallback to dict for v1
    try:
        update_data = task_update.model_dump(exclude_unset=True)
    except AttributeError:
        update_data = task_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    task = db.query(TaskDB).filter(
        TaskDB.id == task_id,
        TaskDB.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    task = db.query(TaskDB).filter(
        TaskDB.id == task_id,
        TaskDB.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = TaskStatus.completed.value
    task.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)
    return task


@app.patch("/tasks/{task_id}/reopen", response_model=TaskResponse)
def reopen_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    task = db.query(TaskDB).filter(
        TaskDB.id == task_id,
        TaskDB.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = TaskStatus.pending.value
    task.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)
    return task


# ---------------- AUTH ---------------- #

@app.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        password_hash = hash_password(user.password)

        db_user = UserDB(
            username=user.username,
            email=user.email,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc)
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(ve))

    except IntegrityError as ie:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@app.post("/login", response_model=TokenResponse)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(UserDB).filter(
        UserDB.username == credentials.username
    ).first()

    if not db_user or not verify_password(credentials.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(db_user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ---------------- STATS ---------------- #

@app.get("/tasks/progress")
def task_progress(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    total_tasks = db.query(TaskDB).filter(
        TaskDB.user_id == current_user.id
    ).count()

    completed_tasks = db.query(TaskDB).filter(
        TaskDB.user_id == current_user.id,
        TaskDB.status == TaskStatus.completed.value
    ).count()

    pending = total_tasks - completed_tasks
    completion_percentage = int(
        (completed_tasks / total_tasks) * 100
    ) if total_tasks > 0 else 0

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending": pending,
        "completion_percentage": completion_percentage
    }

