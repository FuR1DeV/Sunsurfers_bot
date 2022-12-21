import logging
from data.models.users import Users
from data.models.events import Sungatherings, Events
from settings.config import COUNTRIES
from data.db_gino import db

"""Functions for get information from the database"""
logger = logging.getLogger("data.commands.user_get")


async def user_select(user_id):
    logger.debug(f"User select {user_id}")
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    return user


async def all_users():
    logger.debug(f"User select all users")
    users = await Users.query.gino.all()
    return users


async def all_users_with_gatherings():
    logger.debug(f"User select all users with gatherings")
    users = await Users.query.gino.all()
    return users


async def user_get_event_sungathering(user_id):
    logger.debug(f"User checks {user_id} info about sun gathering in country")
    user = await Sungatherings.query.where(Sungatherings.user_id == user_id).gino.first()
    return user


async def user_get_info_country(user_id, country):
    logger.debug(f"User {user_id} checks info about sun gathering in {country}")
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
    logger.debug(f"Checks if there was a user {user_id} at this gathering {country}")
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
    logger.debug(f"The function checks all person at this gathering {country}")
    match country:
        case "Thailand":
            users = await Sungatherings.query.where(Sungatherings.thailand == 1).gino.all()
            return users
        case "India":
            users = await Sungatherings.query.where(Sungatherings.india == 2).gino.all()
            return users
        case "Vietnam":
            users = await Sungatherings.query.where(Sungatherings.vietnam == 3).gino.all()
            return users
        case "Philippines":
            users = await Sungatherings.query.where(Sungatherings.philippines == 4).gino.all()
            return users
        case "Georgia":
            users = await Sungatherings.query.where(Sungatherings.georgia == 5).gino.all()
            return users
        case "Indonesia":
            users = await Sungatherings.query.where(Sungatherings.indonesia == 6).gino.all()
            return users
        case "Nepal":
            users = await Sungatherings.query.where(Sungatherings.nepal == 7).gino.all()
            return users
        case "Morocco":
            users = await Sungatherings.query.where(Sungatherings.morocco == 8).gino.all()
            return users
        case "Turkey":
            users = await Sungatherings.query.where(Sungatherings.turkey == 9).gino.all()
            return users
        case "Mexico":
            users = await Sungatherings.query.where(Sungatherings.mexico == 10).gino.all()
            return users
        case "SriLanka":
            users = await Sungatherings.query.where(Sungatherings.srilanka == 11).gino.all()
            return users


async def user_get_count_sungatherings(user_id):
    user = await Sungatherings.query.where(Sungatherings.user_id == user_id).gino.first()
    countries = []
    try:
        if user.thailand:
            countries.append(f"{COUNTRIES.get('Thailand')} Thailand")
        if user.india:
            countries.append(f"{COUNTRIES.get('India')} India")
        if user.vietnam:
            countries.append(f"{COUNTRIES.get('Vietnam')} Vietnam")
        if user.philippines:
            countries.append(f"{COUNTRIES.get('Philippines')} Philippines")
        if user.georgia:
            countries.append(f"{COUNTRIES.get('Georgia')} Georgia")
        if user.indonesia:
            countries.append(f"{COUNTRIES.get('Indonesia')} Indonesia")
        if user.nepal:
            countries.append(f"{COUNTRIES.get('Nepal')} Nepal")
        if user.morocco:
            countries.append(f"{COUNTRIES.get('Morocco')} Morocco")
        if user.turkey:
            countries.append(f"{COUNTRIES.get('Turkey')} Turkey")
        if user.mexico:
            countries.append(f"{COUNTRIES.get('Mexico')} Mexico")
        if user.srilanka:
            countries.append(f"{COUNTRIES.get('SriLanka')} SriLanka")
    except AttributeError:
        pass
    return countries


async def all_users_in_country(country):
    logger.debug(f"Check all users in {country}")
    users = await Users.query.where(Users.country == country).gino.all()
    return users


async def user_get_info_username(username):
    user = await Users.query.where(Users.username == username).gino.first()
    return user


async def user_get_countries_in_number(user_id):
    user = await Sungatherings.query.where(Sungatherings.user_id == user_id).gino.first()
    countries = []
    try:
        if user.thailand:
            countries.append(1)
        if user.india:
            countries.append(2)
        if user.vietnam:
            countries.append(3)
        if user.philippines:
            countries.append(4)
        if user.georgia:
            countries.append(5)
        if user.indonesia:
            countries.append(6)
        if user.nepal:
            countries.append(7)
        if user.morocco:
            countries.append(8)
        if user.turkey:
            countries.append(9)
        if user.mexico:
            countries.append(10)
        if user.srilanka:
            countries.append(11)
    except AttributeError:
        pass
    return countries


async def sungatherings():
    res = await Events.query.gino.all()
    return res
