from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status
from app.api.shemas import User, Token, UserCreate
from app.core.database import get_async_session
from app.core.models import UserBase
from app.dependencies.password import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash
from app.dependencies.user import authenticate_user, get_current_active_user

router = APIRouter(prefix='/auth', tags=["auth"])


@router.post('/register')
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    # Проверка уникальности по email
    stmt = select(UserBase).where(UserBase.email == user.email)
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail='Пользователь уже существует'
        )
    hashed_password = get_password_hash(user.password)
    new_user = UserBase(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
        disabled=False
    )
    session.add(new_user)
    await session.commit()
    return {"msg": "Регистрация прошла успешно"}


@router.post("/login", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session)
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=User)
async def read_users_me(
        current_user: Annotated[UserBase, Depends(get_current_active_user)],
):
    return current_user
