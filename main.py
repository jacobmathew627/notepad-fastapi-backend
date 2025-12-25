from fastapi import FastAPI, Depends , HTTPException

from sqlalchemy import Column, Integer, String, DateTime,ForeignKey

from sqlalchemy.orm import Session

from datetime import datetime,timezone

from database import Base,engine,get_db

from schema import TaskCreate, TaskResponse , TaskUpdate
app = FastAPI()

@app.get("/health")

def health_check():
    return {"status":"ok"}

class UserDB(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True,nullable=False)
    username = Column(String,unique=True,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password_hash = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)

class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key = True,nullable=False)
    title = Column(String,nullable=False)
    description = Column(String,nullable=True)
    status = Column(String,nullable=False,default="pending")
    due_date = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    created_at=Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    updated_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)

Base.metadata.create_all(bind=engine)

@app.post("/tasks/",response_model=TaskResponse)
def create_task(
    task:TaskCreate,
    db:Session=Depends(get_db)
):
    now = datetime.now(timezone.utc)
    current_user_id = 1
    db_task = TaskDB(
        title = task.title,
        description = task.description,
        due_date = task.due_date,
        status="pending",
        created_at=now,
        updated_at=now,
        user_id = current_user_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@app.get("/tasks",response_model=list[TaskResponse])
def read_tasks(
    db:Session=Depends(get_db),
):
    tasks = db.query(TaskDB).all()
    return tasks

@app.put("/tasks/{task_id}",response_model=TaskResponse)
def update_task(
    task_id :int,
    task_update: TaskUpdate,
    db :Session = Depends(get_db)
):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.due_date is not None:
        task.due_date = task_update.due_date
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}")

def delete_task(
    task_id : int,
    db : Session = Depends(get_db)
):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if task is None:
        return {"error":"Task not found"}
    
    db.delete(task)
    db.commit()

    return {"message":"Task deleted successfully"}
    
