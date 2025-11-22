from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    exist_query = text('select * from users where email = :uid')
    existing = db.execute(exist_query,{"uid":user.email}).fetchone()
    
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_query = text("""INSERT INTO USERS (name,email)values(:name,:email) RETURNING *""")
    
    new_user = db.execute(user_query,{
        "name":user.name,
        "email":user.email
        }).fetchone()

    db.commit()
    return dict(new_user._mapping)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user_query = text('select * from users where id = :uid')
    user = db.execute(user_query,{"uid":user_id}).fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
