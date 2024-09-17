from fastapi import APIRouter, status
from database.database import Session, engine
from database.schemas import SignUpModel
from database.models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

session = Session(bind=engine)


@auth_router.get("/get_users")
async def getUsers():
    users = session.query(User).all()
    
    if users is None:
        return HTTPException(status_code=404, detail="No users found!")
    
    return users, HTTPException(status_code=200, detail="Users found!")


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(
            status_code=400, detail="User with this email already exists!"
        )

    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists!"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )
    
    session.add(new_user)
    session.commit()
    return new_user
