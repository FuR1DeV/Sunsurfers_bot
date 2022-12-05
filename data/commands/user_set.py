from sqlalchemy import and_

from data.models.users import Users
from data.models.events import Sungatherings


"""Functions for adding/updating the database"""


async def user_add(user_id, username, first_name, last_name):
    """The user add to users table"""
    user = Users(user_id=user_id, username=username, first_name=first_name,
                 last_name=last_name)
    await user.create()


async def user_set_about_me(user_id, about):
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    await user.update(about=about).apply()


async def user_set_first_name(user_id, first_name):
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    await user.update(first_name=first_name).apply()


async def user_set_last_name(user_id, last_name):
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    await user.update(last_name=last_name).apply()


async def user_add_sungathering(user_id):
    """The user add to sungatherings table"""
    user = Sungatherings(user_id=user_id)
    await user.create()


async def user_set_geo(user_id, country, state, province, city, town, address, latitude, longitude, updated_location):
    """The user updates his geo data"""
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    await user.update(country=country, state=state, province=province, city=city, town=town, address=address,
                      latitude=latitude, longitude=longitude, updated_location=updated_location).apply()


async def user_update_sungathering(user_id, country, switch: int):
    user = await Sungatherings.query.where(Sungatherings.user_id == user_id).gino.first()
    match country:
        case "Thailand":
            await user.update(thailand=switch).apply()
        case "India":
            await user.update(india=switch).apply()
        case "Vietnam":
            await user.update(vietnam=switch).apply()
        case "Philippines":
            await user.update(philippines=switch).apply()
        case "Georgia":
            await user.update(georgia=switch).apply()
        case "Indonesia":
            await user.update(indonesia=switch).apply()
        case "Nepal":
            await user.update(nepal=switch).apply()
        case "Morocco":
            await user.update(morocco=switch).apply()
        case "Turkey":
            await user.update(turkey=switch).apply()
        case "Mexico":
            await user.update(mexico=switch).apply()
        case "SriLanka":
            await user.update(srilanka=switch).apply()


async def user_set_sun_gathering_about(user_id, country, message):
    user = await Sungatherings.query.where(Sungatherings.user_id == user_id).gino.first()
    match country:
        case "Thailand":
            await user.update(thailand_info=message).apply()
        case "India":
            await user.update(india_info=message).apply()
        case "Vietnam":
            await user.update(vietnam_info=message).apply()
        case "Philippines":
            await user.update(philippines_info=message).apply()
        case "Georgia":
            await user.update(georgia_info=message).apply()
        case "Indonesia":
            await user.update(indonesia_info=message).apply()
        case "Nepal":
            await user.update(nepal_info=message).apply()
        case "Morocco":
            await user.update(morocco_info=message).apply()
        case "Turkey":
            await user.update(turkey_info=message).apply()
        case "Mexico":
            await user.update(mexico_info=message).apply()
        case "SriLanka":
            await user.update(srilanka_info=message).apply()
