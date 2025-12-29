import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from database import Base, engine


# 🔁 Reset DB before & after each test
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_complete_app_flow():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        # ---------- REGISTER ----------
        r = await client.post("/register", json={
            "username": "u1",
            "email": "u1@test.com",
            "password": "StrongPass123"   # ✅ valid password
        })
        assert r.status_code == 200
        assert r.json()["username"] == "u1"

        # ---------- LOGIN ----------
        r = await client.post("/login", json={
            "username": "u1",
            "password": "StrongPass123"
        })
        assert r.status_code == 200
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # ---------- CREATE TASK ----------
        r = await client.post("/tasks/", json={
            "title": "Task A",
            "description": "Test task"
        }, headers=headers)
        assert r.status_code == 200
        task_id = r.json()["id"]

        # ---------- CHECK PROGRESS (AFTER CREATE) ----------
        r = await client.get("/tasks/progress", headers=headers)
        data = r.json()
        assert data["total_tasks"] == 1
        assert data["completed_tasks"] == 0
        assert data["pending"] == 1
        assert data["completion_percentage"] == 0

        # ---------- COMPLETE TASK ----------
        r = await client.patch(f"/tasks/{task_id}/complete", headers=headers)
        assert r.status_code == 200
        assert r.json()["status"] == "completed"

        # ---------- CHECK PROGRESS (AFTER COMPLETE) ----------
        r = await client.get("/tasks/progress", headers=headers)
        data = r.json()
        assert data["total_tasks"] == 1
        assert data["completed_tasks"] == 1
        assert data["pending"] == 0
        assert data["completion_percentage"] == 100

        # ---------- REOPEN TASK ----------
        r = await client.patch(f"/tasks/{task_id}/reopen", headers=headers)
        assert r.status_code == 200
        assert r.json()["status"] == "pending"

        # ---------- DELETE TASK ----------
        r = await client.delete(f"/tasks/{task_id}", headers=headers)
        assert r.status_code == 200

        # ---------- FINAL PROGRESS ----------
        r = await client.get("/tasks/progress", headers=headers)
        data = r.json()
        assert data["total_tasks"] == 0
        assert data["completed_tasks"] == 0
        assert data["pending"] == 0
        assert data["completion_percentage"] == 0
