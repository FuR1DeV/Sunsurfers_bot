from datetime import datetime
from collections import Counter

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from geopy.geocoders import Nominatim

from bot import bot, dp
from data.commands import user_get, user_set
from markups import markup_start, markup_users
from settings import config
from states import states


class UserMain:
    @staticmethod
    async def hi_user(callback: types.CallbackQuery, state: FSMContext):
        user = await user_get.user_select(callback.from_user.id)
        if user is None:
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
        elif user.ban == 0:
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
                    data["time_location"] = datetime.now().strftime('%d %B %Y')
        except AttributeError:
            await bot.send_message(message.from_user.id,
                                   "Something went wrong\n"
                                   "You need to click on the submit my location button\n")

    @staticmethod
    async def main(callback: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        async with state.proxy() as data:
            await user_set.user_add(callback.from_user.id,
                                    data.get("username"),
                                    data.get("first_name"),
                                    data.get("last_name"))
            await user_set.user_set_geo(callback.from_user.id,
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
            UserProfile.register_user_profile(dp)
            user = await user_get.user_select(message.from_user.id)
            await states.UserProfile.my_profile.set()
            sungatherings = await user_get.user_get_count_sungatherings(message.from_user.id)
            await bot.send_message(message.from_user.id,
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"<em>Your Profile:</em>\n"
                                   f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} "
                                   f"Name: <b>{user.first_name} {user.last_name}</b>\n"
                                   f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} "
                                   f"Nickname: <b>@{message.from_user.username}</b>\n"
                                   f"{config.KEYBOARD.get('GLOBE_SHOWING')} "
                                   f"Country: <b>{user.country}</b> | State: <b>{user.state}</b>\n"
                                   f"{config.KEYBOARD.get('CITYSCAPE')} "
                                   f"Province: <b>{user.province}</b> | City: <b>{user.city}</b>\n"
                                   f"{config.KEYBOARD.get('TENT')} "
                                   f"Town: <b>{user.town}</b> | Address: <b>{user.address}</b>\n"
                                   f"{config.KEYBOARD.get('HOURGLASS_NOT_DONE')} "
                                   f"Last Update: <b>{user.updated_location}</b>\n"
                                   f"{config.KEYBOARD.get('SUN')} "
                                   f"SunGatherings: | <b>{len(sungatherings)}</b> | <b>{', '.join(sungatherings)}</b>\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}",
                                   reply_markup=markup_users.user_profile())
        if "Locations" in message.text:
            res = await user_get.all_users()
            country = []
            for i in res:
                country.append(i.country)
            inline_country = InlineKeyboardMarkup()
            countries = Counter(country)
            for k, v in countries.items():
                inline_country.insert(InlineKeyboardButton(text=f'{k} ({v})', callback_data=f'country_{k}'))
            await bot.send_message(message.from_user.id,
                                   f"Display all countries in which there are friends",
                                   reply_markup=inline_country)
            EnterCountry.register_enter_country(dp)
            await states.UserStart.user_menu.set()
        if "Projects" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Here are the services that can be implemented in the future",
                                   reply_markup=markup_users.projects())
            await states.Projects.start.set()
            Projects.register_services(dp)
        if "Events" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Here you can view information about SunGatherings",
                                   reply_markup=markup_users.sun_gathering_menu())
            await states.Sun.sun_menu.set()
            await Events.register_sun_gathering(dp)

    @staticmethod
    def register_user_handler(disp: Dispatcher):
        disp.register_callback_query_handler(UserMain.hi_user, text='enter_bot')
        disp.register_message_handler(UserMain.geo_position, content_types=['location', 'text'],
                                      state=states.UserStart.geo)
        disp.register_callback_query_handler(UserMain.main, state=states.UserStart.geo, text='enter_menu')
        disp.register_message_handler(UserMain.user_menu, state=states.UserStart.user_menu)


class UserProfile:
    @staticmethod
    async def user_profile(message: types.Message):
        res = await user_get.user_select(message.from_user.id)
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
            await bot.send_message(message.from_user.id,
                                   f"Your information about yourself\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"<b>{res.about}</b>\n"
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
            user = await user_get.user_select(message.from_user.id)
            await states.UserProfile.my_profile.set()
            sungatherings = await user_get.user_get_count_sungatherings(message.from_user.id)
            await bot.send_message(message.from_user.id,
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"<em>Your Profile:</em>\n"
                                   f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} "
                                   f"Name: <b>{user.first_name} {user.last_name}</b>\n"
                                   f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} "
                                   f"Nickname: <b>@{message.from_user.username}</b>\n"
                                   f"{config.KEYBOARD.get('GLOBE_SHOWING')} "
                                   f"Country: <b>{user.country}</b> | State: <b>{user.state}</b>\n"
                                   f"{config.KEYBOARD.get('CITYSCAPE')} "
                                   f"Province: <b>{user.province}</b> | City: <b>{user.city}</b>\n"
                                   f"{config.KEYBOARD.get('TENT')} "
                                   f"Town: <b>{user.town}</b> | Address: <b>{user.address}</b>\n"
                                   f"{config.KEYBOARD.get('HOURGLASS_NOT_DONE')} "
                                   f"Last Update: <b>{user.updated_location}</b>\n"
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
        except TypeError:
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
                        data["time_location"] = datetime.now().strftime('%d %B %Y')
            except AttributeError:
                await bot.send_message(message.from_user.id,
                                       "Something went wrong\n"
                                       "You need to click on the submit my location button\n")

    @staticmethod
    async def update_location_menu(callback: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        async with state.proxy() as data:
            await user_set.user_set_geo(callback.from_user.id,
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
            await user_set.user_set_about_me(message.from_user.id, message.text)
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
            await user_set.user_set_first_name(message.from_user.id, message.text)
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
            await user_set.user_set_last_name(message.from_user.id, message.text)
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
    def register_user_profile(disp: Dispatcher):
        disp.register_message_handler(UserProfile.user_profile,
                                      state=states.UserProfile.my_profile)
        disp.register_message_handler(UserProfile.update_information,
                                      state=states.UserProfile.update_info)
        disp.register_message_handler(UserProfile.update_location, content_types=['location', 'text'],
                                      state=states.UserProfile.update_location)
        disp.register_callback_query_handler(UserProfile.update_location_menu,
                                             state=states.UserProfile.update_location)
        disp.register_message_handler(UserProfile.update_about_me,
                                      state=states.UserProfile.update_about_me)
        disp.register_message_handler(UserProfile.update_first_name,
                                      state=states.UserProfile.update_first_name)
        disp.register_message_handler(UserProfile.update_last_name,
                                      state=states.UserProfile.update_last_name)


class EnterCountry:
    @staticmethod
    async def country(callback: types.CallbackQuery):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        country = callback.data[8:]
        await bot.send_message(callback.from_user.id,
                               f"Great! You choose {country}\n"
                               f"Here are the people who are in this country")
        res = await user_get.all_users_in_country(country)
        inline_country = InlineKeyboardMarkup()
        for i in res:
            inline_country.insert(InlineKeyboardButton(text=f'{i.username}', callback_data=f'user_{i.username}'))
        await bot.send_message(callback.from_user.id,
                               f"Show all users in the selected country",
                               reply_markup=inline_country)

    @staticmethod
    async def user(callback: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        user = callback.data[5:]
        await bot.send_message(callback.from_user.id,
                               f"Great! You choose {user}\n"
                               f"You can view information about this user")
        async with state.proxy() as data:
            res = await user_get.user_get_info_username(user)
            data["user"] = res
        sungatherings = await user_get.user_get_count_sungatherings(res.user_id)
        await bot.send_message(callback.from_user.id,
                               f"{config.KEYBOARD.get('DASH') * 14}\n"
                               f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} "
                               f"Name: <b>{res.first_name} {res.last_name}</b>\n"
                               f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} "
                               f"Nickname: <b>@{res.username}</b>\n"
                               f"{config.KEYBOARD.get('GLOBE_SHOWING')} "
                               f"Country: <b>{res.country}</b> | State: <b>{res.state}</b>\n"
                               f"{config.KEYBOARD.get('CITYSCAPE')} "
                               f"Province: <b>{res.province}</b> | City: <b>{res.city}</b>\n"
                               f"{config.KEYBOARD.get('TENT')} "
                               f"Town: <b>{res.town}</b>\n"
                               f"{config.KEYBOARD.get('HOURGLASS_NOT_DONE')} "
                               f"Last Update: <b>{res.updated_location}</b>\n"
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
            await bot.send_message(message.from_user.id,
                                   f"Information about this person\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"<b>{user_res.about}</b>\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}")
        if f"{config.KEYBOARD.get('SUN')} Words about SunGatherings" in message.text:
            countries = {f"{config.COUNTRIES.get('Thailand')} Thailand": "1.0",
                         f"{config.COUNTRIES.get('India')} India": "2.0",
                         f"{config.COUNTRIES.get('Vietnam')} Vietnam": "3.0",
                         f"{config.COUNTRIES.get('Philippines')} Philippines": "4.0",
                         f"{config.COUNTRIES.get('Georgia')} Georgia": "5.0",
                         f"{config.COUNTRIES.get('Indonesia')} Indonesia": "6.0",
                         f"{config.COUNTRIES.get('Nepal')} Nepal": "7.0",
                         f"{config.COUNTRIES.get('Morocco')} Morocco": "8.0",
                         f"{config.COUNTRIES.get('Turkey')} Turkey": "9.0",
                         f"{config.COUNTRIES.get('Mexico')} Mexico": "10.0",
                         f"{config.COUNTRIES.get('SriLanka')} SriLanka": "11.0"}
            sungatherings = await user_get.user_get_count_sungatherings(user_res.user_id)
            inline_gathering = InlineKeyboardMarkup()
            for i in sungatherings:
                inline_gathering.insert(InlineKeyboardButton(text=f'{countries.get(i)} {i}',
                                                             callback_data=f'us_sun_a_{i}'))

            if inline_gathering.values.get("inline_keyboard"):
                await bot.send_message(message.from_user.id,
                                       f"Choose the SunGathering",
                                       reply_markup=inline_gathering)
            else:
                await bot.send_message(message.from_user.id,
                                       f"While there are no SunGatherings in which he was")
        if "Main menu" in message.text:
            await bot.send_message(message.from_user.id,
                                   f"{message.from_user.first_name} You are in the main menu",
                                   reply_markup=markup_users.main_menu())
            await states.UserStart.user_menu.set()

    @staticmethod
    async def user_info_about_sun_gathering(callback: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        country = callback.data.split()[1]
        async with state.proxy() as data:
            user_res = data.get("user")
            about = await user_get.check_user_sun_gathering(user_res.user_id, country)
        if about is None:
            await bot.send_message(callback.from_user.id,
                                   f"Words about SunGathering in <b>{country}:</b>\n"
                                   f"\n"
                                   f"<b>There is no information yet</b>",
                                   reply_markup=markup_users.user_choose())
        else:
            await bot.send_message(callback.from_user.id,
                                   f"Words about SunGathering in <b>{country}:</b>\n"
                                   f"\n"
                                   f"<b>{about}</b>",
                                   reply_markup=markup_users.user_choose())

    @staticmethod
    def register_enter_country(disp: Dispatcher):
        disp.register_callback_query_handler(EnterCountry.country,
                                             state=states.UserStart.user_menu,
                                             text_contains='country_')
        disp.register_callback_query_handler(EnterCountry.user,
                                             state=states.UserStart.user_menu,
                                             text_contains='user_')
        disp.register_message_handler(EnterCountry.user_info,
                                      state=states.Information.user_info)
        disp.register_callback_query_handler(EnterCountry.user_info_about_sun_gathering,
                                             state=states.Information.user_info,
                                             text_contains='us_sun_a_')


class Events:
    @staticmethod
    async def sun_main(message: types.Message):
        if "Main menu" in message.text:
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the main menu",
                                   reply_markup=markup_users.main_menu())
        if "SunGathering" in message.text:
            user = await user_get.user_get_event_sungathering(message.from_user.id)
            countries_dict = {"Thailand": 0, "India": 0, "Vietnam": 0, "Philippines": 0, "Georgia": 0,
                              "Indonesia": 0, "Nepal": 0, "Morocco": 0, "Turkey": 0, "Mexico": 0, "SriLanka": 0}
            if user is None:
                await user_set.user_add_sungathering(message.from_user.id)
                await bot.send_message(message.from_user.id,
                                       "<b>Choose which sungatherings you were on</b>\n"
                                       "If you have not been to any SunGatherings, then select <b>That's all</b>",
                                       reply_markup=markup_users.sungatherings(countries_dict))
            else:
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
                user_countries = await user_get.user_get_event_sungathering(message.from_user.id)
                for i in range(1, 12):
                    if user_countries.thailand:
                        countries_dict["Thailand"] = 1
                    if user_countries.india:
                        countries_dict["India"] = 1
                    if user_countries.vietnam:
                        countries_dict["Vietnam"] = 1
                    if user_countries.philippines:
                        countries_dict["Philippines"] = 1
                    if user_countries.georgia:
                        countries_dict["Georgia"] = 1
                    if user_countries.indonesia:
                        countries_dict["Indonesia"] = 1
                    if user_countries.nepal:
                        countries_dict["Nepal"] = 1
                    if user_countries.morocco:
                        countries_dict["Morocco"] = 1
                    if user_countries.turkey:
                        countries_dict["Turkey"] = 1
                    if user_countries.mexico:
                        countries_dict["Mexico"] = 1
                    if user_countries.srilanka:
                        countries_dict["SriLanka"] = 1
                inline_gathering = InlineKeyboardMarkup()
                v = 1
                for i in countries:
                    if countries_dict.get(i.split()[1]) == 1:
                        inline_gathering.insert(
                            InlineKeyboardButton(text=f'{v}.0 {config.KEYBOARD.get("CHECK_MARK_BUTTON")} {i}',
                                                 callback_data=f'sun_gathering_{i}'))
                    else:
                        inline_gathering.insert(InlineKeyboardButton(text=f'{v}.0 {i}',
                                                                     callback_data=f'sun_gathering_{i}'))
                    v += 1
                await bot.send_message(message.from_user.id,
                                       f"Choose the SunGathering",
                                       reply_markup=inline_gathering)
        if "SunUniversity" in message.text:
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
        if "SunAtorium" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Info about SunAtorium")
        if "Yoga Retreat" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Info about Yoga Retreat")
        if "SunWomanCamp" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Info about SunWomanCamp")
        if "Meetups" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Info about Meetups")

    @staticmethod
    async def add_gathering(callback: types.CallbackQuery):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        country = callback.data.split()[1]
        await user_set.user_update_sungathering(callback.from_user.id, country)
        user_countries = await user_get.user_get_event_sungathering(callback.from_user.id)
        countries_dict = {"Thailand": 0, "India": 0, "Vietnam": 0, "Philippines": 0, "Georgia": 0, "Indonesia": 0,
                          "Nepal": 0, "Morocco": 0, "Turkey": 0, "Mexico": 0, "SriLanka": 0}
        for i in range(1, 12):
            if user_countries.thailand:
                countries_dict["Thailand"] = 1
            if user_countries.india:
                countries_dict["India"] = 1
            if user_countries.vietnam:
                countries_dict["Vietnam"] = 1
            if user_countries.philippines:
                countries_dict["Philippines"] = 1
            if user_countries.georgia:
                countries_dict["Georgia"] = 1
            if user_countries.indonesia:
                countries_dict["Indonesia"] = 1
            if user_countries.nepal:
                countries_dict["Nepal"] = 1
            if user_countries.morocco:
                countries_dict["Morocco"] = 1
            if user_countries.turkey:
                countries_dict["Turkey"] = 1
            if user_countries.mexico:
                countries_dict["Mexico"] = 1
            if user_countries.srilanka:
                countries_dict["SriLanka"] = 1
        await bot.send_message(callback.from_user.id,
                               "<b>Choose which sungatherings you were on</b>",
                               reply_markup=markup_users.sungatherings(countries_dict))
        await bot.send_message(callback.from_user.id,
                               f"{country} - Added!")

    @staticmethod
    async def finish_sun_gathering(callback: types.CallbackQuery):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)

    @staticmethod
    async def select_sun_gathering(callback: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        res = callback.data.split()[1]
        async with state.proxy() as data:
            data["sun_gathering_country"] = res
        await states.Sun.country_menu.set()
        user_exist = await user_get.user_get_info_country(callback.from_user.id, res)
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
            res = await user_get.check_user_sun_gathering(message.from_user.id,
                                                          country)
            if res:
                await bot.send_message(message.from_user.id,
                                       "Describe your memories\n"
                                       "Now your memories are:\n"
                                       f"<b>{res}</b>",
                                       reply_markup=markup_users.about_sun_gathering())
                await states.Sun.about.set()
            else:
                await bot.send_message(message.from_user.id,
                                       "Describe your memories",
                                       reply_markup=markup_users.about_sun_gathering())
                await states.Sun.about.set()
        if message.text == f"{config.KEYBOARD.get('EX_QUEST_MARK')} Who was there?":
            all_users = await user_get.check_users_in_sun_gathering(res)
            if all_users:
                await bot.send_message(message.from_user.id,
                                       "Here's who was on the SunGathering")
                v = 1
                for i in all_users:
                    user = await user_get.user_select(i.user_id)
                    await bot.send_message(message.from_user.id,
                                           f"{v}. @{user.username} | {user.first_name}")
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
        async with state.proxy() as data:
            await user_set.user_update_sungathering(callback.from_user.id,
                                                    data.get("sun_gathering_country"))
        await bot.send_message(callback.from_user.id,
                               f"Great you were at this event! <b>SunGathering - "
                               f"{data.get('sun_gathering_country')}</b>\n",
                               reply_markup=markup_users.sun_gathering_menu_select_country(True))

    @staticmethod
    async def about_sun_gathering(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            res = data.get("sun_gathering_country")
        user_exist = await user_get.user_get_info_country(message.from_user.id, res)
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            await states.Sun.country_menu.set()
            await bot.send_message(message.from_user.id,
                                   f"You are in {res}",
                                   reply_markup=markup_users.sun_gathering_menu_select_country(user_exist))
        if message.text != f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            async with state.proxy() as data:
                await user_set.user_set_sun_gathering_about(message.from_user.id,
                                                            data.get("sun_gathering_country"),
                                                            message.text)
            await states.Sun.country_menu.set()
            await bot.send_message(message.from_user.id,
                                   f"Success! Your data has been updated!\n"
                                   f"You are in {res}",
                                   reply_markup=markup_users.sun_gathering_menu_select_country(user_exist))

    @staticmethod
    async def register_sun_gathering(disp: Dispatcher):
        disp.register_message_handler(Events.sun_main,
                                      state=states.Sun.sun_menu)
        disp.register_callback_query_handler(Events.add_gathering,
                                             state=states.Sun.sun_menu,
                                             text_contains='add_sun_gathering_')
        disp.register_callback_query_handler(Events.select_sun_gathering,
                                             state=states.Sun.sun_menu,
                                             text_contains='sun_gathering_')
        disp.register_message_handler(Events.select_sun_gathering_menu,
                                      state=states.Sun.country_menu)
        disp.register_callback_query_handler(Events.add_person_to_sun_gathering,
                                             state="*",
                                             text='add_to_event')
        disp.register_message_handler(Events.about_sun_gathering,
                                      state=states.Sun.about)
        disp.register_callback_query_handler(Events.finish_sun_gathering,
                                             state="*",
                                             text='clean')


class Projects:
    @staticmethod
    async def services(message: types.Message):
        if "Feedback" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Describe your problem\n"
                                   "When you're done, you can return to the main menu",
                                   reply_markup=markup_users.user_feedback())
            await states.Projects.help.set()
        if "Marathons" in message.text:
            await states.Projects.marathons.set()
            await bot.send_message(message.from_user.id,
                                   "Information about marathons",
                                   reply_markup=markup_users.marathons())
        if "SunSchool" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Information about SunSchool")
        if "Travel Book" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Information about Travel Book")
        if "Ecovillage in Georgia" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Information about Ecovillage in Georgia")
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
                                   reply_markup=markup_users.projects())
            await states.Projects.start.set()
        if message.text != f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            await bot.send_message('@sunsurfers_bot_help',
                                   f"Name {message.from_user.first_name}\n"
                                   f"ID {message.from_user.id}\n"
                                   f"Message - <b>{message.text}</b>\n")
            await states.Projects.start.set()
            await bot.send_message(message.from_user.id,
                                   "Message sent to tech support!",
                                   reply_markup=markup_users.projects())

    @staticmethod
    async def marathons(message: types.Message):
        if "Yoga marathon" in message.text:
            await bot.send_message(message.from_user.id,
                                   "There will be information about\n"
                                   "Yoga marathon")
        if "Interval training marathon" in message.text:
            await bot.send_message(message.from_user.id,
                                   "There will be information about\n"
                                   "Interval training marathon")
        if "Marathon of minimalism" in message.text:
            await bot.send_message(message.from_user.id,
                                   "There will be information about\n"
                                   "Marathon of minimalism")
        if "Marathon of early rises" in message.text:
            await bot.send_message(message.from_user.id,
                                   "There will be information about\n"
                                   "Marathon of early rises")
        if "Back" in message.text:
            await states.Projects.start.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the services",
                                   reply_markup=markup_users.projects())

    @staticmethod
    def register_services(disp: Dispatcher):
        disp.register_message_handler(Projects.services,
                                      state=states.Projects.start)
        disp.register_message_handler(Projects.help,
                                      state=states.Projects.help)
        disp.register_message_handler(Projects.marathons,
                                      state=states.Projects.marathons)
