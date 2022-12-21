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


@router.get("/")
async def get_users():
    await db.set_bind(config.POSTGRES_URI)
    users = await user_get.all_users()
    for i in users:
        countries = await user_get.user_get_countries_in_number(i.__values__.get("user_id"))
        i.__values__["sun"] = countries
    bind = db.pop_bind()
    if bind:
        await bind.close()
    return users


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    await db.set_bind(config.POSTGRES_URI)
    user = await user_get.user_select(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {user_id} does not exist")
    countries = await user_get.user_get_countries_in_number(user.__values__.get("user_id"))
    user.__values__["sun"] = countries
    bind = db.pop_bind()
    if bind:
        await bind.close()
    return user
