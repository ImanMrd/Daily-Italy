from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.schemas import UserCreate, UserLogin, UserOut, Token
from backend.app.services.auth_service import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    username_clean = user_in.username.strip()
    if not username_clean:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username cannot be empty"
        )

    # Strictly enforce unique username (case-insensitive)
    existing = db.query(User).filter(func.lower(User.username) == func.lower(username_clean)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The username '{username_clean}' is already taken. Please choose another unique username."
        )
    
    today_str = date.today().isoformat()
    new_user = User(
        username=username_clean,
        email=user_in.email.strip() if user_in.email else None,
        hashed_password=hash_password(user_in.password),
        xp=10,  # Welcome bonus
        streak_days=1,
        last_active_date=today_str,
        hearts=5,
        gems=50,
        unlocked_levels="A1"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer", "user": new_user}

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(func.lower(User.username) == func.lower(user_in.username.strip())).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Check streak update
    today_str = date.today().isoformat()
    if user.last_active_date != today_str:
        # Check if yesterday
        try:
            last_date = datetime.strptime(user.last_active_date, "%Y-%m-%d").date()
            diff = (date.today() - last_date).days
            if diff == 1:
                user.streak_days += 1
            elif diff > 1:
                user.streak_days = 1
        except Exception:
            user.streak_days = 1
        user.last_active_date = today_str
        db.commit()

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
