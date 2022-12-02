from sqlalchemy import and_

from data.models.users import Users
from data.models.events import Sungatherings


"""Functions for adding/updating the database"""


async def user_add(user_id, username, first_name, last_name):
    """The user add to users table"""
    user = Users(user_id=user_id, username=username, first_name=first_name,
                 last_name=last_name)
    await user.create()


async def user_add_sungathering(user_id):
    """The user add to sungatherings table"""
    user = Sungatherings(user_id=user_id)
    await user.create()


async def user_set_geo(user_id, country, state, province, city, town, address, latitude, longitude, updated_location):
    """The user updates his geo data"""
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    await user.update(country=country, state=state, province=province, city=city, town=town, address=address,
                      latitude=latitude, longitude=longitude, updated_location=updated_location).apply()


async def user_update_sungathering(user_id, country):
    user = await Sungatherings.query.where(Sungatherings.user_id == user_id).gino.first()
    match country:
        case "Thailand":
            await user.update(thailand=1).apply()
        case "India":
            await user.update(india=1).apply()
        case "Vietnam":
            await user.update(vietnam=1).apply()
        case "Philippines":
            await user.update(philippines=1).apply()
        case "Georgia":
            await user.update(georgia=1).apply()
        case "Indonesia":
            await user.update(indonesia=1).apply()
        case "Nepal":
            await user.update(nepal=1).apply()
        case "Morocco":
            await user.update(morocco=1).apply()
        case "Turkey":
            await user.update(turkey=1).apply()
        case "Mexico":
            await user.update(mexico=1).apply()
        case "SriLanka":
            await user.update(srilanka=1).apply()





