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


async def user_get_info_country(user_id, country):
    """User checks info about sun gathering in country"""
    user = await Sungatherings.query.where(Sungatherings.user_id == user_id).gino.first()
    match country:
        case "Thailand":
            return user.thailand
        case "India":
            return user.india
        case "Vietnam":
            return user.vietnam
        case "Philippines":
            return user.philippines
        case "Georgia":
            return user.georgia
        case "Indonesia":
            return user.indonesia
        case "Nepal":
            return user.nepal
        case "Morocco":
            return user.morocco
        case "Turkey":
            return user.turkey
        case "Mexico":
            return user.mexico
        case "SriLanka":
            return user.srilanka


async def check_user_sun_gathering(user_id, country):
    """The function checks if there was a person at this gathering"""
    user = await Sungatherings.query.where(Sungatherings.user_id == user_id).gino.first()
    match country:
        case "Thailand":
            return user.thailand_info
        case "India":
            return user.india_info
        case "Vietnam":
            return user.vietnam_info
        case "Philippines":
            return user.philippines_info
        case "Georgia":
            return user.georgia_info
        case "Indonesia":
            return user.indonesia_info
        case "Nepal":
            return user.nepal_info
        case "Morocco":
            return user.morocco_info
        case "Turkey":
            return user.turkey_info
        case "Mexico":
            return user.mexico_info
        case "SriLanka":
            return user.srilanka_info


async def check_users_in_sun_gathering(country):
    """The function checks all person at this gathering"""
    match country:
        case "Thailand":
            users = await Sungatherings.query.where(Sungatherings.thailand == 1).gino.all()
            return users
        case "India":
            users = await Sungatherings.query.where(Sungatherings.india == 1).gino.all()
            return users
        case "Vietnam":
            users = await Sungatherings.query.where(Sungatherings.vietnam == 1).gino.all()
            return users
        case "Philippines":
            users = await Sungatherings.query.where(Sungatherings.philippines == 1).gino.all()
            return users
        case "Georgia":
            users = await Sungatherings.query.where(Sungatherings.georgia == 1).gino.all()
            return users
        case "Indonesia":
            users = await Sungatherings.query.where(Sungatherings.indonesia == 1).gino.all()
            return users
        case "Nepal":
            users = await Sungatherings.query.where(Sungatherings.nepal == 1).gino.all()
            return users
        case "Morocco":
            users = await Sungatherings.query.where(Sungatherings.morocco == 1).gino.all()
            return users
        case "Turkey":
            users = await Sungatherings.query.where(Sungatherings.turkey == 1).gino.all()
            return users
        case "Mexico":
            users = await Sungatherings.query.where(Sungatherings.mexico == 1).gino.all()
            return users
        case "SriLanka":
            users = await Sungatherings.query.where(Sungatherings.srilanka == 1).gino.all()
            return users
