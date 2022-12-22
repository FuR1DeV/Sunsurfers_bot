import logging
from data.models.users import Users
from data.models.events import EventMembers, SunGatherings

"""Functions for adding/updating the database"""
logger = logging.getLogger("data.commands.user_set")


async def user_add(user_id, username, first_name, last_name):
    logger.debug(f"The user {first_name}, {last_name} add to users table")
    user = Users(user_id=user_id, username=username, first_name=first_name,
                 last_name=last_name)
    await user.create()


async def user_set_about_me(user_id, about):
    logger.debug(f"User update {user_id} about")
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    await user.update(about=about).apply()


async def user_set_first_name(user_id, first_name):
    logger.debug(f"User {user_id} update first_name - {first_name}")
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    await user.update(first_name=first_name).apply()


async def user_set_last_name(user_id, last_name):
    logger.debug(f"User {user_id} update last_name - {last_name}")
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    await user.update(last_name=last_name).apply()


async def user_add_sungathering(user_id):
    logger.debug(f"The user {user_id} add to sungatherings table")
    user = EventMembers(user_id=user_id)
    await user.create()


async def user_set_geo(user_id, country, state, province, city, town, latitude, longitude, updated_location):
    logger.debug(f"The user {user_id} updates his geo data")
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    await user.update(country=country, state=state, province=province, city=city, town=town,
                      latitude=latitude, longitude=longitude, updated_location=updated_location).apply()


async def user_update_sungathering(user_id, country):
    logger.debug(f"The user {user_id} update sungathering")
    user = await EventMembers.query.where(EventMembers.user_id == user_id).gino.first()
    match country:
        case "Thailand":
            await user.update(thailand=1).apply()
        case "India":
            await user.update(india=2).apply()
        case "Vietnam":
            await user.update(vietnam=3).apply()
        case "Philippines":
            await user.update(philippines=4).apply()
        case "Georgia":
            await user.update(georgia=5).apply()
        case "Indonesia":
            await user.update(indonesia=6).apply()
        case "Nepal":
            await user.update(nepal=7).apply()
        case "Morocco":
            await user.update(morocco=8).apply()
        case "Turkey":
            await user.update(turkey=9).apply()
        case "Mexico":
            await user.update(mexico=10).apply()
        case "SriLanka":
            await user.update(srilanka=11).apply()


async def user_delete_sungathering(user_id, country):
    logger.debug(f"The user {user_id} update sungathering")
    user = await EventMembers.query.where(EventMembers.user_id == user_id).gino.first()
    match country:
        case "Thailand":
            await user.update(thailand=0).apply()
        case "India":
            await user.update(india=0).apply()
        case "Vietnam":
            await user.update(vietnam=0).apply()
        case "Philippines":
            await user.update(philippines=0).apply()
        case "Georgia":
            await user.update(georgia=0).apply()
        case "Indonesia":
            await user.update(indonesia=0).apply()
        case "Nepal":
            await user.update(nepal=0).apply()
        case "Morocco":
            await user.update(morocco=0).apply()
        case "Turkey":
            await user.update(turkey=0).apply()
        case "Mexico":
            await user.update(mexico=0).apply()
        case "SriLanka":
            await user.update(srilanka=0).apply()


async def user_set_sun_gathering_about(user_id, country, message):
    logger.debug(f"The user {user_id} set sungathering")
    user = await EventMembers.query.where(EventMembers.user_id == user_id).gino.first()
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


async def add_sungatherings():
    exists = await SunGatherings.query.gino.all()
    if exists:
        pass
    else:
        thailand = SunGatherings(title="SunGathering 1.0 Thailand", country="th", year=2013)
        india = SunGatherings(title="SunGathering 2.0 India", country="in", year=2014)
        vietnam = SunGatherings(title="SunGathering 3.0 Vietnam", country="vn", year=2014)
        philippines = SunGatherings(title="SunGathering 4.0 Philippines", country="ph", year=2015)
        georgia = SunGatherings(title="SunGathering 5.0 Georgia", country="ph", year=2015)
        indonesia = SunGatherings(title="SunGathering 6.0 Indonesia", country="ph", year=2016)
        nepal = SunGatherings(title="SunGathering 7.0 Nepal", country="np", year=2016)
        morocco = SunGatherings(title="SunGathering 8.0 Morocco", country="np", year=2017)
        turkey = SunGatherings(title="SunGathering 9.0 Turkey", country="np", year=2017)
        mexico = SunGatherings(title="SunGathering 10.0 Mexico", country="mx", year=2018)
        srilanka = SunGatherings(title="SunGathering 11.0 Sri-Lanka", country="lk", year=2019)
        await thailand.create()
        await india.create()
        await vietnam.create()
        await philippines.create()
        await georgia.create()
        await indonesia.create()
        await nepal.create()
        await morocco.create()
        await turkey.create()
        await mexico.create()
        await srilanka.create()






