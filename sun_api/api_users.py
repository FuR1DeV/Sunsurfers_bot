from fastapi import status, HTTPException, APIRouter
from typing import List

from settings import config
from sun_api import schemas
from data.commands import user_get
from data.db_gino import db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[schemas.User])
async def get_users():
    await db.set_bind(config.POSTGRES_URI)
    user = await user_get.all_users()
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int):
    await db.set_bind(config.POSTGRES_URI)
    users = await user_get.user_select(user_id)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {user_id} does not exist")
    return users
