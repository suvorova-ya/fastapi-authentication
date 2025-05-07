from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.shemas import UserInDB, User, TokenData
from app.core.database import async_session_maker
from app.dependencies.password import verify_password, oauth2_scheme, SECRET_KEY, ALGORITHM
from app.core.models import UserBase


async def get_user(session: AsyncSession, username: str) -> UserBase | None:
    stmt = select(UserBase).where(UserBase.username == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def authenticate_user(session: AsyncSession, username: str, password: str):
    """аутентификация пользователя"""
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: AsyncSession = Depends(async_session_maker)
                           ) -> UserBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[UserBase, Depends(get_current_user)],
) -> UserBase:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
