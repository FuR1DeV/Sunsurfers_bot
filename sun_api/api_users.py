from datetime import datetime

from fastapi import status, HTTPException, APIRouter

from settings import config
from data.commands import user_get
from data.db_gino import db

router = APIRouter()


@router.get("/users")
async def get_users():
    await db.set_bind(config.POSTGRES_URI)
    users = await user_get.all_users()
    for i in users:
        countries = await user_get.user_get_countries_in_number(i.__values__.get("user_id"))
        i.__values__["sun"] = countries
        i.__values__["updated_location"] = datetime.strptime(i.__values__["updated_location"], '%d %B %Y')
    res = []
    for i in users:
        res.append(i.__values__)
    bind = db.pop_bind()
    if bind:
        await bind.close()
    return res


@router.get("/users/{user_id}")
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
    return user.__values__


@router.get("/events")
async def get_gatherings():
    await db.set_bind(config.POSTGRES_URI)
    sungatherings = await user_get.sungatherings()
    sununiversities = await user_get.sununiversities()
    bind = db.pop_bind()
    if bind:
        await bind.close()
    result = {
        "sungatherings": [],
        "sununiversities": []
    }
    for i in sungatherings:
        result["sungatherings"].append(i.__values__)
    for i in sununiversities:
        result["sununiversities"].append(i.__values__)
    return result
