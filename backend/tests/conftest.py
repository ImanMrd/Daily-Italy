import os
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models.user import User
from backend.app.services.auth_service import hash_password, create_access_token

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def user_token(db_session):
    user = db_session.query(User).filter(User.username == "test_standard_user").first()
    if not user:
        user = User(
            username="test_standard_user",
            email="standard@test.com",
            role="user",
            hashed_password=hash_password("userpass123"),
            xp=50,
            streak_days=2,
            hearts=5
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return create_access_token({"sub": user.username})

@pytest.fixture(scope="session")
def admin_token(db_session):
    admin = db_session.query(User).filter(User.username == "test_admin_user").first()
    if not admin:
        admin = User(
            username="test_admin_user",
            email="admin@test.com",
            role="admin",
            hashed_password=hash_password("adminpass123"),
            xp=500,
            streak_days=10,
            hearts=5
        )
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)
    return create_access_token({"sub": admin.username})
