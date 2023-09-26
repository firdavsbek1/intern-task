from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

from models import User
from schemas import SignUpModel, LoginModel
from database import SessionLocal, engine
from fastapi.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_

auth_router = APIRouter(
    prefix="/auth"
)

session = SessionLocal(bind=engine)


@auth_router.get("/")
async def auth(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to see this page.")
    return {"message": "You are successfully authenticated!"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_email or db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with that credentials already taken. Use another one!")

    new_user = User(
        username=user.username,
        password=generate_password_hash(user.password),
        email=user.email,
        is_staff=user.is_staff,
        is_active=user.is_active
    )
    session.add(new_user)
    session.commit()

    data = {
        'username': new_user.username,
        'password': new_user.password,
        'email': new_user.email,
        'is_staff': new_user.is_staff,
        'is_active': new_user.is_active,
    }
    return {
        'message': 'User registration is complete.',
        'status': 201,
        'data': data
    }


@auth_router.post("/login", status_code=200)
async def login(user: LoginModel, authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )
    ).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = authorize.create_access_token(subject=db_user.username)
        refresh_token = authorize.create_refresh_token(subject=db_user.username)
        response = {
            'success': True,
            'message': "Successful Login",
            'status': 200,
            "token": {
                'access': access_token,
                'refresh': refresh_token
            }
        }
        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password.")
