from fastapi import APIRouter, status, Depends
from app.schemas.user import (SignUpModel, LoginModel, UserUpdateModel)
from app.db.database import session, engine
from app.models.user import User
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
import datetime

auth_routers = APIRouter(
    prefix="/auth"
)

session = session(bind=engine)


@auth_routers.get("/")
async def home(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {"message": "Auth sigunp sahifasi"}


@auth_routers.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    username = User.get_by_username(session, user.username)
    email = User.get_by_email(session, user.email)

    if username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )

    session.add(new_user)
    session.commit()
    data = {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "is_staff": new_user.is_staff,
        "is_active": new_user.is_active
    }

    respons_model = {
        "success": True,
        "code": 201,
        "message": "user is crated successfully",
        "data": data
    }

    return JSONResponse(content=respons_model, status_code=status.HTTP_201_CREATED)


@auth_routers.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = User.get_by_username(session,user.username)
    if db_user and check_password_hash(db_user.password, user.password):
        acess_lifetime = datetime.timedelta(minutes=1)
        refresh_lifetime = datetime.timedelta(hours=1)
        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=acess_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_lifetime)

        token = {
            "access": access_token,
            "refresh": refresh_token
        }
        response = {
            "success": True,
            "code": 200,
            "message": "user successfully login",
            "data": token
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")


@auth_routers.get("/login/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        acess_lifetime = datetime.timedelta(minutes=1)
        refresh_lifetime = datetime.timedelta(hours=1)
        Authorize.jwt_refresh_token_required()  # valid refresh token talab qiladi
        current_user = Authorize.get_jwt_subject()  # access tokendan username ajratib oladi

        # Databasedan userni filter orqali topamiz

        db_user = User.get_by_username(session,current_user)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # access token yratiladi
        new_access = Authorize.create_access_token(subject=db_user.username, expires_time=acess_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_lifetime)

        token = {
            "access": new_access,
            "refresh": refresh_token
        }
        response = {
            "success": True,
            "code": 200,
            "message": "New access token is created",
            "data": token
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Refresh token")


@auth_routers.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(Authorize: AuthJWT = Depends()):
    # bu endpoint avtorizatsiya o'tgan user uzini akkauntini uchirishi uchun
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access Token")
    user = Authorize.get_jwt_subject()
    current_user = User.get_by_username(session, user)
    if current_user:
        session.delete(current_user)
        session.commit()
        response = {
            "success": True,
            "code": 200,
            "message": f"User {current_user.username} has been successfully deleted ",
            "data": None
        }

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.username} has been not found")


@auth_routers.put("/update", status_code=status.HTTP_200_OK)
async def update_user(update_data: UserUpdateModel, Authorize: AuthJWT = Depends()):
    # bu endpoint avtorizatsiya o'tgan user uzini akkauntini update qilishi uchun
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access Token")
    user = Authorize.get_jwt_subject()
    current_user = User.get_by_username(session, user)
    if current_user:
        # update user info
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(current_user, key, value)
        session.commit()
        data = {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "is_staff": current_user.is_staff,
            "is_active": current_user.is_active
        }
        response = {
            "success": True,
            "code": 200,
            "message": f"User {current_user.username} has been successfully updated ",
            "data": data
        }

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.username} has been not found")
