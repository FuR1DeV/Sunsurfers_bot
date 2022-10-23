from datetime import datetime
from collections import Counter

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from geopy.geocoders import Nominatim

from bot import bot, dp
from data.get_set_db import global_get_db_obj, user_get_db_obj, user_set_db_obj
from markups import markup_start, markup_users
from settings import config
from states import states


class UserMain:
    @staticmethod
    async def hi_user(callback: types.CallbackQuery, state: FSMContext):
        if not user_get_db_obj.user_exists(callback.from_user.id):
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            async with state.proxy() as data:
                data["user_id"] = callback.from_user.id
                data["username"] = callback.from_user.username
                data["first_name"] = callback.from_user.first_name
                data["last_name"] = callback.from_user.last_name
            await bot.send_message(callback.from_user.id,
                                   f"{callback.from_user.first_name} In order to use this bot you must "
                                   f"provide information about your location",
                                   reply_markup=markup_start.send_my_geo())
            await states.UserStart.geo.set()
        elif not user_get_db_obj.user_ban(callback.from_user.id)[0]:
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await states.UserStart.user_menu.set()
            await bot.send_message(callback.from_user.id,
                                   "<b>Welcome Sunsurfer</b>!",
                                   reply_markup=markup_users.main_menu())
        else:
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await bot.send_message(callback.from_user.id, "You are blocked! Contact technical support!")

    @staticmethod
    async def geo_position(message: types.Message, state: FSMContext):
        try:
            n = Nominatim(user_agent='User')
            loc = f"{message.location.latitude}, {message.location.longitude}"
            location = n.reverse(loc, language='en')
            country = location.raw.get("address").get("country")
            state_ = location.raw.get("address").get("state")
            province = location.raw.get("address").get("province")
            city = location.raw.get("address").get("city")
            town = location.raw.get("address").get("town")
            road = location.raw.get("address").get("road")
            house = location.raw.get("address").get("house_number")
            if road is None:
                road = f"{config.KEYBOARD.get('MINUS')}"
            if house is None:
                house = f"{config.KEYBOARD.get('MINUS')}"
            address = f'{road} - {house}'
            latitude = location.raw.get("lat")
            longitude = location.raw.get("lon")
            if state_ is None:
                state_ = f"{config.KEYBOARD.get('MINUS')}"
            if province is None:
                province = f"{config.KEYBOARD.get('MINUS')}"
            if city is None:
                city = f"{config.KEYBOARD.get('MINUS')}"
            if town is None:
                town = f"{config.KEYBOARD.get('MINUS')}"
            await bot.send_message(message.from_user.id,
                                   f'Country: <b>{country}</b>\n'
                                   f'State: <b>{state_}</b>\n'
                                   f'Province: <b>{province}</b>\n'
                                   f'City: <b>{city}</b>\n'
                                   f'Town: <b>{town}</b>\n'
                                   f'Address: <b>{address}</b>\n')
            if country is None:
                await bot.send_message(message.from_user.id,
                                       "Your location has not been determined"
                                       "Submit your location again",
                                       reply_markup=markup_start.send_my_geo())
                await states.UserStart.geo.set()
            if country:
                await bot.send_message(message.from_user.id,
                                       "Please check the coordinates, if you made a mistake, "
                                       "you can send the geolocation again. If everything is ok, "
                                       "click Enter Main Menu",
                                       reply_markup=markup_start.start_menu())
                async with state.proxy() as data:
                    data["country"] = country
                    data["state"] = state_
                    data["province"] = province
                    data["city"] = city
                    data["town"] = town
                    data["address"] = address
                    data["latitude"] = latitude
                    data["longitude"] = longitude
                    data["time_location"] = str(datetime.now())[:19]
        except AttributeError:
            await bot.send_message(message.from_user.id,
                                   "Something went wrong\n"
                                   "You need to click on the submit my location button\n")

    @staticmethod
    async def main(callback: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        async with state.proxy() as data:
            user_set_db_obj.user_add(callback.from_user.id,
                                     data.get("username"),
                                     data.get("first_name"),
                                     data.get("last_name"))
            user_set_db_obj.user_set_geo(callback.from_user.id,
                                         data.get("country"),
                                         data.get("state"),
                                         data.get("province"),
                                         data.get("city"),
                                         data.get("town"),
                                         data.get("address"),
                                         data.get("latitude"),
                                         data.get("longitude"),
                                         data.get("time_location"))
        await bot.send_message(callback.from_user.id,
                               f"{callback.from_user.first_name} You are in the main menu",
                               reply_markup=markup_users.main_menu())
        await states.UserStart.user_menu.set()

    @staticmethod
    async def user_menu(message: types.Message, state: FSMContext):
        await state.finish()
        if "My profile" in message.text:
            countries = {f"{config.COUNTRIES.get('Thailand')}": "Thailand",
                         f"{config.COUNTRIES.get('India')}": "India",
                         f"{config.COUNTRIES.get('Vietnam')}": "Vietnam",
                         f"{config.COUNTRIES.get('Philippines')}": "Philippines",
                         f"{config.COUNTRIES.get('Georgia')}": "Georgia",
                         f"{config.COUNTRIES.get('Indonesia')}": "Indonesia",
                         f"{config.COUNTRIES.get('Nepal')}": "Nepal",
                         f"{config.COUNTRIES.get('Morocco')}": "Morocco",
                         f"{config.COUNTRIES.get('Turkey')}": "Turkey",
                         f"{config.COUNTRIES.get('Mexico')}": "Mexico",
                         f"{config.COUNTRIES.get('SriLanka')}": "SriLanka"}
            UserProfile.register_user_profile(dp)
            res = user_get_db_obj.user_exists(message.from_user.id)
            await states.UserProfile.my_profile.set()
            state_, province, city, town, address = res[7], res[8], res[9], res[10], res[11]
            sungatherings = []
            for k, v in countries.items():
                if user_get_db_obj.user_get_info_country(res[1], v):
                    sungatherings.append(v)
            await bot.send_message(message.from_user.id,
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"<em>Your Profile:</em>\n"
                                   f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} "
                                   f"Name: <b>{res[3]} {res[4]}</b>\n"
                                   f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} "
                                   f"Nickname: <b>@{message.from_user.username}</b>\n"
                                   f"{config.KEYBOARD.get('GLOBE_SHOWING')} "
                                   f"Country: <b>{res[6]}</b> | State: <b>{state_}</b>\n"
                                   f"{config.KEYBOARD.get('CITYSCAPE')} "
                                   f"Province: <b>{province}</b> | City: <b>{city}</b>\n"
                                   f"{config.KEYBOARD.get('TENT')} "
                                   f"Town: <b>{town}</b> | Address: <b>{address}</b>\n"
                                   f"{config.KEYBOARD.get('HOURGLASS_NOT_DONE')} "
                                   f"Last Update: <b>{res[14].strftime('%d %B, %Y')}</b>\n"
                                   f"{config.KEYBOARD.get('SUN')} "
                                   f"SunGatherings: | <b>{len(sungatherings)}</b> | <b>{', '.join(sungatherings)}</b>\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}",
                                   reply_markup=markup_users.user_profile())
        if "Locations" in message.text:
            res = global_get_db_obj.all_users()
            country = []
            for i in res:
                country.append(i[6])
            inline_country = InlineKeyboardMarkup()
            countrys = Counter(country)
            for k, v in countrys.items():
                inline_country.insert(InlineKeyboardButton(text=f'{k} ({v})', callback_data=f'country_{k}'))
            await bot.send_message(message.from_user.id,
                                   f"Display all countries in which there are friends",
                                   reply_markup=inline_country)
            EnterCountry.register_enter_country(dp)
            await states.UserStart.user_menu.set()
        if "Services" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Here are the services that can be implemented in the future",
                                   reply_markup=markup_users.services())
            await states.Services.start.set()
            Services.register_services(dp)
        if "SunGatherings" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Here you can view information about SunGatherings",
                                   reply_markup=markup_users.sun_gathering_menu())
            await states.Sun.sun_menu.set()
            SunGathering.register_sun_gathering(dp)

    @staticmethod
    def register_user_handler(dp: Dispatcher):
        dp.register_callback_query_handler(UserMain.hi_user, text='enter_bot')
        dp.register_message_handler(UserMain.geo_position, content_types=['location', 'text'],
                                    state=states.UserStart.geo)
        dp.register_callback_query_handler(UserMain.main, state=states.UserStart.geo, text='enter_menu')
        dp.register_message_handler(UserMain.user_menu, state=states.UserStart.user_menu)


class UserProfile:
    @staticmethod
    async def user_profile(message: types.Message):
        if "Main menu" in message.text:
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the main menu",
                                   reply_markup=markup_users.main_menu())
        if message.text == f"{config.KEYBOARD.get('UP!_BUTTON')} Update Information":
            await states.UserProfile.update_info.set()
            await bot.send_message(message.from_user.id,
                                   "Here you can update your information",
                                   reply_markup=markup_users.user_profile_update_info())
        if message.text == f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} About me":
            res = user_get_db_obj.user_about(message.from_user.id)[0]
            await bot.send_message(message.from_user.id,
                                   f"Your information about yourself\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"<b>{res}</b>\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}",
                                   reply_markup=markup_users.user_profile())

    @staticmethod
    async def update_information(message: types.Message):
        if "Update Location" in message.text:
            await bot.send_message(message.from_user.id,
                                   f"{message.from_user.first_name} Update your location",
                                   reply_markup=markup_start.update_location_send_my_geo())
            await states.UserProfile.update_location.set()
        if message.text == f"{config.KEYBOARD.get('CLIPBOARD')} Update About me":
            await bot.send_message(message.from_user.id,
                                   "<b>Here you can edit your information</b>\n"
                                   "<b>Enter any information about yourself and send me a message</b>",
                                   reply_markup=markup_users.back())
            await states.UserProfile.update_about_me.set()
        if message.text == f"{config.KEYBOARD.get('INFORMATION')} Update First Name":
            await bot.send_message(message.from_user.id,
                                   "<b>Here you can edit your First Name</b>\n"
                                   "<b>Enter First Name and send me a message</b>",
                                   reply_markup=markup_users.back())
            await states.UserProfile.update_first_name.set()
        if message.text == f"{config.KEYBOARD.get('INFORMATION')} Update Last Name":
            await bot.send_message(message.from_user.id,
                                   "<b>Here you can edit your Last Name</b>\n"
                                   "<b>Enter Last Name and send me a message</b>",
                                   reply_markup=markup_users.back())
            await states.UserProfile.update_last_name.set()
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            countries = {f"{config.COUNTRIES.get('Thailand')}": "Thailand",
                         f"{config.COUNTRIES.get('India')}": "India",
                         f"{config.COUNTRIES.get('Vietnam')}": "Vietnam",
                         f"{config.COUNTRIES.get('Philippines')}": "Philippines",
                         f"{config.COUNTRIES.get('Georgia')}": "Georgia",
                         f"{config.COUNTRIES.get('Indonesia')}": "Indonesia",
                         f"{config.COUNTRIES.get('Nepal')}": "Nepal",
                         f"{config.COUNTRIES.get('Morocco')}": "Morocco",
                         f"{config.COUNTRIES.get('Turkey')}": "Turkey",
                         f"{config.COUNTRIES.get('Mexico')}": "Mexico",
                         f"{config.COUNTRIES.get('SriLanka')}": "SriLanka"}
            UserProfile.register_user_profile(dp)
            res = user_get_db_obj.user_exists(message.from_user.id)
            await states.UserProfile.my_profile.set()
            state_, province, city, town, address = res[7], res[8], res[9], res[10], res[11]
            sungatherings = []
            for k, v in countries.items():
                if user_get_db_obj.user_get_info_country(res[1], v):
                    sungatherings.append(v)
            await bot.send_message(message.from_user.id,
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"<em>Your Profile:</em>\n"
                                   f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} "
                                   f"Your Name: <b>{res[3]} {res[4]}</b>\n"
                                   f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} "
                                   f"Your Nickname: <b>@{message.from_user.username}</b>\n"
                                   f"{config.KEYBOARD.get('GLOBE_SHOWING')} "
                                   f"Country: <b>{res[6]}</b> | State: <b>{state_}</b>\n"
                                   f"{config.KEYBOARD.get('CITYSCAPE')} "
                                   f"Province: <b>{province}</b> | City: <b>{city}</b>\n"
                                   f"{config.KEYBOARD.get('TENT')} "
                                   f"Town: <b>{town}</b> | Address: <b>{address}</b>\n"
                                   f"{config.KEYBOARD.get('HOURGLASS_NOT_DONE')} "
                                   f"Last Update: <b>{res[14].strftime('%d %B, %Y')}</b>\n"
                                   f"{config.KEYBOARD.get('SUN')} "
                                   f"SunGatherings: | <b>{len(sungatherings)}</b> | <b>{', '.join(sungatherings)}</b>\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}",
                                   reply_markup=markup_users.user_profile())

    @staticmethod
    async def update_location(message: types.Message, state: FSMContext):
        try:
            if "Back" in message.text:
                await bot.send_message(message.from_user.id,
                                       "<b>You are back in Update Information</b>",
                                       reply_markup=markup_users.user_profile_update_info())
                await states.UserProfile.update_info.set()
        except:
            try:
                n = Nominatim(user_agent='User')
                loc = f"{message.location.latitude}, {message.location.longitude}"
                location = n.reverse(loc, language='en')
                country = location.raw.get("address").get("country")
                state_ = location.raw.get("address").get("state")
                province = location.raw.get("address").get("province")
                city = location.raw.get("address").get("city")
                town = location.raw.get("address").get("town")
                road = location.raw.get("address").get("road")
                house = location.raw.get("address").get("house_number")
                if road is None:
                    road = f"{config.KEYBOARD.get('MINUS')}"
                if house is None:
                    house = f"{config.KEYBOARD.get('MINUS')}"
                address = f'{road} - {house}'
                latitude = location.raw.get("lat")
                longitude = location.raw.get("lon")
                if state_ is None:
                    state_ = f"{config.KEYBOARD.get('MINUS')}"
                if province is None:
                    province = f"{config.KEYBOARD.get('MINUS')}"
                if city is None:
                    city = f"{config.KEYBOARD.get('MINUS')}"
                if town is None:
                    town = f"{config.KEYBOARD.get('MINUS')}"
                await bot.send_message(message.from_user.id,
                                       f'Country: <b>{country}</b>\n'
                                       f'State: <b>{state_}</b>\n'
                                       f'Province: <b>{province}</b>\n'
                                       f'City: <b>{city}</b>\n'
                                       f'Town: <b>{town}</b>\n'
                                       f'Address: <b>{address}</b>\n')
                if country is None:
                    await bot.send_message(message.from_user.id,
                                           "Your location has not been determined"
                                           "Submit your location again",
                                           reply_markup=markup_start.update_location())
                if country:
                    await bot.send_message(message.from_user.id,
                                           "Please check the coordinates, if you made a mistake, "
                                           "you can send the geolocation again. If everything is ok, "
                                           "click <b>Update My Location</b>",
                                           reply_markup=markup_start.update_location())
                    async with state.proxy() as data:
                        data["country"] = country
                        data["state"] = state_
                        data["province"] = province
                        data["city"] = city
                        data["town"] = town
                        data["address"] = address
                        data["latitude"] = latitude
                        data["longitude"] = longitude
                        data["time_location"] = str(datetime.now())[:19]
            except AttributeError:
                await bot.send_message(message.from_user.id,
                                       "Something went wrong\n"
                                       "You need to click on the submit my location button\n")

    @staticmethod
    async def update_location_menu(callback: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        async with state.proxy() as data:
            user_set_db_obj.user_set_geo(callback.from_user.id,
                                         data.get("country"),
                                         data.get("state"),
                                         data.get("province"),
                                         data.get("city"),
                                         data.get("town"),
                                         data.get("address"),
                                         data.get("latitude"),
                                         data.get("longitude"),
                                         data.get("time_location"))
            await bot.send_message(callback.from_user.id,
                                   "Update completed!",
                                   reply_markup=markup_users.user_profile_update_info())
            await states.UserProfile.update_info.set()

    @staticmethod
    async def update_about_me(message: types.Message):
        if message.text != f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            user_set_db_obj.user_set_about_me(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id,
                                   "<b>Successfully!</b>",
                                   reply_markup=markup_users.user_profile_update_info())
            await states.UserProfile.update_info.set()
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            await bot.send_message(message.from_user.id,
                                   "<b>You are back in Update Information</b>",
                                   reply_markup=markup_users.user_profile_update_info())
            await states.UserProfile.update_info.set()

    @staticmethod
    async def update_first_name(message: types.Message):
        if message.text != f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            user_set_db_obj.user_set_first_name(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id,
                                   "<b>Successfully!</b>",
                                   reply_markup=markup_users.user_profile_update_info())
            await states.UserProfile.update_info.set()
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            await bot.send_message(message.from_user.id,
                                   "<b>You are back in Update Information</b>",
                                   reply_markup=markup_users.user_profile_update_info())
            await states.UserProfile.update_info.set()

    @staticmethod
    async def update_last_name(message: types.Message):
        if message.text != f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            user_set_db_obj.user_set_last_name(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id,
                                   "<b>Successfully!</b>",
                                   reply_markup=markup_users.user_profile_update_info())
            await states.UserProfile.update_info.set()
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            await bot.send_message(message.from_user.id,
                                   "<b>You are back in Update Information</b>",
                                   reply_markup=markup_users.user_profile_update_info())
            await states.UserProfile.update_info.set()

    @staticmethod
    def register_user_profile(dp):
        dp.register_message_handler(UserProfile.user_profile,
                                    state=states.UserProfile.my_profile)
        dp.register_message_handler(UserProfile.update_information,
                                    state=states.UserProfile.update_info)
        dp.register_message_handler(UserProfile.update_location, content_types=['location', 'text'],
                                    state=states.UserProfile.update_location)
        dp.register_callback_query_handler(UserProfile.update_location_menu,
                                           state=states.UserProfile.update_location)
        dp.register_message_handler(UserProfile.update_about_me,
                                    state=states.UserProfile.update_about_me)
        dp.register_message_handler(UserProfile.update_first_name,
                                    state=states.UserProfile.update_first_name)
        dp.register_message_handler(UserProfile.update_last_name,
                                    state=states.UserProfile.update_last_name)


class EnterCountry:
    @staticmethod
    async def country(callback: types.CallbackQuery):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        country = callback.data[8:]
        await bot.send_message(callback.from_user.id,
                               f"Great! You choose {country}\n"
                               f"Here are the people who are in this country")
        res = global_get_db_obj.all_users_in_country(country)
        inline_country = InlineKeyboardMarkup()
        for i in res:
            inline_country.insert(InlineKeyboardButton(text=f'{i[2]}', callback_data=f'user_{i[2]}'))
        await bot.send_message(callback.from_user.id,
                               f"Show all users in the selected country",
                               reply_markup=inline_country)

    @staticmethod
    async def user(callback: types.CallbackQuery, state: FSMContext):
        countries = {f"{config.COUNTRIES.get('Thailand')}": "Thailand",
                     f"{config.COUNTRIES.get('India')}": "India",
                     f"{config.COUNTRIES.get('Vietnam')}": "Vietnam",
                     f"{config.COUNTRIES.get('Philippines')}": "Philippines",
                     f"{config.COUNTRIES.get('Georgia')}": "Georgia",
                     f"{config.COUNTRIES.get('Indonesia')}": "Indonesia",
                     f"{config.COUNTRIES.get('Nepal')}": "Nepal",
                     f"{config.COUNTRIES.get('Morocco')}": "Morocco",
                     f"{config.COUNTRIES.get('Turkey')}": "Turkey",
                     f"{config.COUNTRIES.get('Mexico')}": "Mexico",
                     f"{config.COUNTRIES.get('SriLanka')}": "SriLanka"}
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        user = callback.data[5:]
        await bot.send_message(callback.from_user.id,
                               f"Great! You choose {user}\n"
                               f"You can view information about this user")
        async with state.proxy() as data:
            res = user_get_db_obj.user_get_info_username(callback.from_user.id, user)
            data["user"] = res
        sungatherings = []
        for k, v in countries.items():
            if user_get_db_obj.user_get_info_country(res[1], v):
                sungatherings.append(v)
        await bot.send_message(callback.from_user.id,
                               f"{config.KEYBOARD.get('DASH') * 14}\n"
                               f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} "
                               f"Name: <b>{res[3]} {res[4]}</b>\n"
                               f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} "
                               f"Nickname: <b>@{res[2]}</b>\n"
                               f"{config.KEYBOARD.get('GLOBE_SHOWING')} "
                               f"Country: <b>{res[6]}</b> | State: <b>{res[7]}</b>\n"
                               f"{config.KEYBOARD.get('CITYSCAPE')} "
                               f"Province: <b>{res[8]}</b> | City: <b>{res[9]}</b>\n"
                               f"{config.KEYBOARD.get('TENT')} "
                               f"Town: <b>{res[10]}</b>\n"
                               f"{config.KEYBOARD.get('HOURGLASS_NOT_DONE')} "
                               f"Last Update: <b>{res[14].strftime('%d %B, %Y')}</b>\n"
                               f"{config.KEYBOARD.get('SUN')} "
                               f"SunGatherings: | <b>{len(sungatherings)}</b> | <b>{', '.join(sungatherings)}</b>\n"
                               f"{config.KEYBOARD.get('DASH') * 14}",
                               reply_markup=markup_users.user_choose())
        await states.Information.user_info.set()

    @staticmethod
    async def user_info(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            user_res = data.get("user")
        if "About him/her" in message.text:
            about = user_get_db_obj.user_about(user_res[1])[0]
            await bot.send_message(message.from_user.id,
                                   f"Information about this person\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"<b>{about}</b>\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}")
        if f"{config.KEYBOARD.get('SUN')} Words about SunGatherings" in message.text:
            countries = {f"{config.COUNTRIES.get('Thailand')}": "Thailand",
                         f"{config.COUNTRIES.get('India')}": "India",
                         f"{config.COUNTRIES.get('Vietnam')}": "Vietnam",
                         f"{config.COUNTRIES.get('Philippines')}": "Philippines",
                         f"{config.COUNTRIES.get('Georgia')}": "Georgia",
                         f"{config.COUNTRIES.get('Indonesia')}": "Indonesia",
                         f"{config.COUNTRIES.get('Nepal')}": "Nepal",
                         f"{config.COUNTRIES.get('Morocco')}": "Morocco",
                         f"{config.COUNTRIES.get('Turkey')}": "Turkey",
                         f"{config.COUNTRIES.get('Mexico')}": "Mexico",
                         f"{config.COUNTRIES.get('SriLanka')}": "SriLanka"}
            sungatherings = []
            for k, v in countries.items():
                if user_get_db_obj.user_get_info_country(user_res[1], v):
                    sungatherings.append(v)
            inline_gathering = InlineKeyboardMarkup()
            for i in sungatherings:
                inline_gathering.insert(InlineKeyboardButton(text=f'{i}',
                                                             callback_data=f'sun_gathering_{i}'))
            await bot.send_message(message.from_user.id,
                                   f"Choose the SunGathering",
                                   reply_markup=inline_gathering)
        if "Main menu" in message.text:
            await bot.send_message(message.from_user.id,
                                   f"{message.from_user.first_name} You are in the main menu",
                                   reply_markup=markup_users.main_menu())
            await states.UserStart.user_menu.set()

    @staticmethod
    def register_enter_country(dp):
        dp.register_callback_query_handler(EnterCountry.country,
                                           state=states.UserStart.user_menu,
                                           text_contains='country_')
        dp.register_callback_query_handler(EnterCountry.user,
                                           state=states.UserStart.user_menu,
                                           text_contains='user_')
        dp.register_message_handler(EnterCountry.user_info,
                                    state=states.Information.user_info)


class SunGathering:
    @staticmethod
    async def sun_main(message: types.Message):
        if "Main menu" in message.text:
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the main menu",
                                   reply_markup=markup_users.main_menu())
        if "Choose SunGathering" in message.text:
            countries = [f"{config.COUNTRIES.get('Thailand')} Thailand",
                         f"{config.COUNTRIES.get('India')} India",
                         f"{config.COUNTRIES.get('Vietnam')} Vietnam",
                         f"{config.COUNTRIES.get('Philippines')} Philippines",
                         f"{config.COUNTRIES.get('Georgia')} Georgia",
                         f"{config.COUNTRIES.get('Indonesia')} Indonesia",
                         f"{config.COUNTRIES.get('Nepal')} Nepal",
                         f"{config.COUNTRIES.get('Morocco')} Morocco",
                         f"{config.COUNTRIES.get('Turkey')} Turkey",
                         f"{config.COUNTRIES.get('Mexico')} Mexico",
                         f"{config.COUNTRIES.get('SriLanka')} SriLanka"]
            inline_gathering = InlineKeyboardMarkup()
            v = 1
            for i in countries:
                inline_gathering.insert(InlineKeyboardButton(text=f'{v}.0 {i}',
                                                             callback_data=f'sun_gathering_{i}'))
                v += 1
            await bot.send_message(message.from_user.id,
                                   f"Choose the SunGathering",
                                   reply_markup=inline_gathering)
        if "Choose SunUniversity" in message.text:
            countries = [f"{config.COUNTRIES.get('India')} India",
                         f"{config.COUNTRIES.get('SriLanka')} SriLanka",
                         f"{config.COUNTRIES.get('Turkey')} Turkey",
                         f"{config.COUNTRIES.get('Thailand')} Thailand",
                         f"{config.COUNTRIES.get('Albania')} Albania"]
            inline_university = InlineKeyboardMarkup()
            v = 1
            for i in countries:
                inline_university.insert(InlineKeyboardButton(text=f'{v}.0 {i}',
                                                              callback_data=f'sun_university_{i}'))
                v += 1
            await bot.send_message(message.from_user.id,
                                   f"Choose the SunUniversity",
                                   reply_markup=inline_university)

    @staticmethod
    async def select_sun_gathering(callback: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        res = callback.data.split()[1]
        async with state.proxy() as data:
            data["sun_gathering_country"] = res
        await states.Sun.country_menu.set()
        user_exist = user_get_db_obj.user_get_info_country(callback.from_user.id, res)
        await bot.send_message(callback.from_user.id,
                               f"Super! You choosed {res}",
                               reply_markup=markup_users.sun_gathering_menu_select_country(user_exist))

    @staticmethod
    async def select_sun_gathering_menu(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            res = data.get("sun_gathering_country")
        if message.text == f"{config.KEYBOARD.get('SUNRISE')} About SunGathering":
            await bot.send_message(message.from_user.id,
                                   f"Here will be shown information about the SunGathering in {res}")
        if message.text == f"{config.KEYBOARD.get('WAVING_HAND')} I was there!":
            await bot.send_message(message.from_user.id,
                                   "If you were at this SunGathering, "
                                   "then you can be added to the participants of this event",
                                   reply_markup=markup_users.add_event())
        if message.text == f"{config.KEYBOARD.get('CLIPBOARD')} My words about SunGathering":
            async with state.proxy() as data:
                country = data.get("sun_gathering_country")
            res = global_get_db_obj.check_user_sun_gathering(message.from_user.id,
                                                             country)
            if res[2]:
                await bot.send_message(message.from_user.id,
                                       "Describe your memories\n"
                                       "Now your memories are:\n"
                                       f"<b>{res[2]}</b>",
                                       reply_markup=markup_users.about_sun_gathering())
                await states.Sun.about.set()
            else:
                await bot.send_message(message.from_user.id,
                                       "Describe your memories",
                                       reply_markup=markup_users.about_sun_gathering())
                await states.Sun.about.set()
        if message.text == f"{config.KEYBOARD.get('EX_QUEST_MARK')} Who was there?":
            all_users = global_get_db_obj.check_users_in_sun_gathering(res)
            if all_users:
                await bot.send_message(message.from_user.id,
                                       "Here's who was on the SunGathering")
                v = 1
                for i in all_users:
                    await bot.send_message(message.from_user.id,
                                           f"{v}. @{' | '.join(global_get_db_obj.load_username_first_last_name(i[1]))}")
                    v += 1
            else:
                await bot.send_message(message.from_user.id,
                                       "No one yet =(")
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu":
            await states.Sun.sun_menu.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the main menu",
                                   reply_markup=markup_users.sun_gathering_menu())

    @staticmethod
    async def add_person_to_sun_gathering(callback: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        res = None
        try:
            async with state.proxy() as data:
                res = user_get_db_obj.user_get_info_country(callback.from_user.id,
                                                            data.get("sun_gathering_country"))[0]
        except TypeError:
            pass
        if res is None:
            async with state.proxy() as data:
                user_set_db_obj.user_set_sun_gathering(callback.from_user.id,
                                                       data.get("sun_gathering_country").lower())
            await bot.send_message(callback.from_user.id,
                                   f"Great you were at this event! <b>SunGathering - "
                                   f"{data.get('sun_gathering_country')}</b>\n",
                                   reply_markup=markup_users.sun_gathering_menu_select_country(True))
        if res:
            await bot.send_message(callback.from_user.id,
                                   "You are already there")

    @staticmethod
    async def about_sun_gathering(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            res = data.get("sun_gathering_country")
        user_exist = user_get_db_obj.user_get_info_country(message.from_user.id, res)
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            await states.Sun.country_menu.set()
            await bot.send_message(message.from_user.id,
                                   f"You are in {res}",
                                   reply_markup=markup_users.sun_gathering_menu_select_country(user_exist))
        if message.text != f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            async with state.proxy() as data:
                user_set_db_obj.user_set_sun_gathering_about(message.from_user.id,
                                                             data.get("sun_gathering_country"),
                                                             message.text)
            await states.Sun.country_menu.set()
            await bot.send_message(message.from_user.id,
                                   f"Success! Your data has been updated!\n"
                                   f"You are in {res}",
                                   reply_markup=markup_users.sun_gathering_menu_select_country(user_exist))

    @staticmethod
    def register_sun_gathering(dp):
        dp.register_message_handler(SunGathering.sun_main,
                                    state=states.Sun.sun_menu)
        dp.register_callback_query_handler(SunGathering.select_sun_gathering,
                                           state=states.Sun.sun_menu,
                                           text_contains='sun_gathering_')
        dp.register_message_handler(SunGathering.select_sun_gathering_menu,
                                    state=states.Sun.country_menu)
        dp.register_callback_query_handler(SunGathering.add_person_to_sun_gathering,
                                           state="*",
                                           text='add_to_event')
        dp.register_message_handler(SunGathering.about_sun_gathering,
                                    state=states.Sun.about)


class Services:
    @staticmethod
    async def services(message: types.Message):
        if "Feedback" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Describe your problem\n"
                                   "When you're done, you can return to the main menu",
                                   reply_markup=markup_users.user_feedback())
            await states.Services.help.set()
        if "OM" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Here you can get Human Design, Gene Keys",
                                   reply_markup=markup_users.user_om())
            await states.Services.om.set()
        if "Main menu" in message.text:
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the main menu",
                                   reply_markup=markup_users.main_menu())

    @staticmethod
    async def help(message: types.Message):
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            await bot.send_message(message.from_user.id,
                                   f"{message.from_user.first_name} You are in the services",
                                   reply_markup=markup_users.services())
            await states.Services.start.set()
        if message.text != f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            await bot.send_message('@sunsurfers_bot_help',
                                   f"Name {message.from_user.first_name}\n"
                                   f"ID {message.from_user.id}\n"
                                   f"Message - <b>{message.text}</b>\n")
            await states.Services.start.set()
            await bot.send_message(message.from_user.id,
                                   "Message sent to tech support!",
                                   reply_markup=markup_users.services())

    @staticmethod
    async def om(message: types.Message):
        if "Gene Keys" in message.text:
            await bot.send_message(message.from_user.id, "Will be implemented here (if needed)\n"
                                                         "Gene Keys")
        if "Human Design" in message.text:
            await bot.send_message(message.from_user.id, "Will be implemented here (if needed)\n"
                                                         "Human Design")
        if "Back" in message.text:
            await states.Services.start.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the services",
                                   reply_markup=markup_users.services())

    @staticmethod
    def register_services(dp):
        dp.register_message_handler(Services.services,
                                    state=states.Services.start)
        dp.register_message_handler(Services.help,
                                    state=states.Services.help)
        dp.register_message_handler(Services.om,
                                    state=states.Services.om)
