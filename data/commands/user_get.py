from sqlalchemy import and_

from data.models.users import Users
from data.models.events import Sungatherings


"""Functions for get information from the database"""


async def user_select(user_id):
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    return user


async def user_get_event_sungathering(user_id):
    """User checks info about sun gathering in country"""
    user = await Sungatherings.query.where(Sungatherings.user_id == user_id).gino.first()
    return user








