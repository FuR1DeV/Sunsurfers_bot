import logging
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
    async def hi_user(callback: types.CallbackQuery):
        if not user_get_db_obj.user_exists(callback.from_user.id):
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button = types.KeyboardButton(text='Phone request', request_contact=True)
            keyboard.add(button)
            await bot.send_message(callback.from_user.id,
                                   f"{callback.from_user.first_name}\n"
                                   f"Share with us your phone number!",
                                   reply_markup=keyboard)
            await states.UserPhone.phone.set()
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
    async def phone(message: types.Message, state: FSMContext):
        if message.contact.user_id == message.from_user.id:
            index = message.contact.phone_number.find("+")
            if index == 0:
                telephone = message.contact.phone_number
            else:
                telephone = f"+{message.contact.phone_number}"
            async with state.proxy() as data:
                data["user_id"] = message.from_user.id
                data["username"] = message.from_user.username
                data["contact"] = telephone
                data["first_name"] = message.from_user.first_name
                data["last_name"] = message.from_user.last_name
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   f"{message.from_user.first_name} In order to use this bot you must "
                                   f"provide information about your location",
                                   reply_markup=markup_start.send_my_geo())
            await states.UserStart.geo.set()
        else:
            await bot.send_message(message.from_user.id,
                                   "This is not your phone number!\n"
                                   "Press /start to start again")

    @staticmethod
    async def geo_position(message: types.Message, state: FSMContext):
        try:
            n = Nominatim(user_agent='User')
            loc = f"{message.location.latitude}, {message.location.longitude}"
            location = n.reverse(loc)
            country = location.raw.get("address").get("country")
            state_ = location.raw.get("address").get("state")
            city = location.raw.get("address").get("city")
            address = f'{location.raw.get("address").get("road")} - {location.raw.get("address").get("house_number")}'
            latitude = location.raw.get("lat")
            longitude = location.raw.get("lon")
            if city is None:
                city = location.raw.get("address").get("town")
            await bot.send_message(message.from_user.id,
                                   f'Country: {country}\n'
                                   f'State: {state_}\n'
                                   f'City: {city}\n'
                                   f'Address: {address}\n')
            if country is None:
                await bot.send_message(message.from_user.id,
                                       "Your location has not been determined"
                                       "Submit your location again",
                                       reply_markup=markup_start.send_my_geo())
                await states.UserStart.geo.set()
            if country and message.reply_to_message.text:
                await bot.send_message(message.from_user.id,
                                       "Please check the coordinates, if you made a mistake, "
                                       "you can send the geolocation again. If everything is ok, "
                                       "click Enter Main Menu",
                                       reply_markup=markup_start.start_menu())
                async with state.proxy() as data:
                    data["country"] = country
                    data["state"] = state_
                    data["city"] = city
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
        async with state.proxy() as data:
            user_set_db_obj.user_add(callback.from_user.id,
                                     data.get("username"),
                                     data.get("contact"),
                                     data.get("first_name"),
                                     data.get("last_name"))
            user_set_db_obj.user_set_geo(callback.from_user.id,
                                         data.get("country"),
                                         data.get("state"),
                                         data.get("city"),
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
            res = user_get_db_obj.user_exists(message.from_user.id)
            await states.UserProfile.my_profile.set()
            await bot.send_message(message.from_user.id,
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"Your Profile:\n"
                                   f"{config.KEYBOARD.get('ID_BUTTON')} "
                                   f"Your ID: <b>{message.from_user.id}</b>\n"
                                   f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} "
                                   f"Your nickname: <b>@{message.from_user.username}</b>\n"
                                   f"{config.KEYBOARD.get('TELEPHONE')} "
                                   f"Your number: <b>{res[3]}</b>\n"
                                   f"{config.KEYBOARD.get('INFORMATION')} "
                                   f"Your Country: <b>{res[7]}</b>\n"
                                   f"{config.KEYBOARD.get('INFORMATION')} "
                                   f"Your State: <b>{res[8]}</b>\n"
                                   f"{config.KEYBOARD.get('INFORMATION')} "
                                   f"Your City: <b>{res[9]}</b>\n"
                                   f"{config.KEYBOARD.get('INFORMATION')} "
                                   f"Your Address: <b>{res[10]}</b>\n"
                                   f"{config.KEYBOARD.get('INFORMATION')} "
                                   f"Last Update: <b>{res[13]}</b>\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}",
                                   reply_markup=markup_users.user_profile())
        if "Locations" in message.text:
            Locations.register_info(dp)
            await states.Information.info.set()
            await bot.send_message(message.from_user.id,
                                   "Here, you can see information about your friends",
                                   reply_markup=markup_users.go_info())
        if "Feedback" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Describe your problem\n"
                                   "When you're done, you can return to the main menu",
                                   reply_markup=markup_users.user_feedback())
            Feedback.register_feedback(dp)
            await states.Feedback.help.set()
        if "OM" in message.text:
            await bot.send_message(message.from_user.id,
                                   "Here you can get Human Design, Gene Keys",
                                   reply_markup=markup_users.user_om())
            await states.UserStart.om.set()

    @staticmethod
    async def om(message: types.Message):
        if "Gene Keys" in message.text:
            await bot.send_message(message.from_user.id, "Will be implemented here (if needed)\n"
                                                         "Gene Keys")
        if "Human Design" in message.text:
            await bot.send_message(message.from_user.id, "Will be implemented here (if needed)\n"
                                                         "Human Design")
        if "Main menu" in message.text:
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the main menu",
                                   reply_markup=markup_users.main_menu())

    @staticmethod
    def register_user_handler(dp: Dispatcher):
        dp.register_message_handler(UserMain.phone, content_types=['contact'],
                                    state=states.UserPhone.phone)
        dp.register_callback_query_handler(UserMain.hi_user, text='enter_bot')
        dp.register_message_handler(UserMain.geo_position, content_types=['location', 'text'],
                                    state=states.UserStart.geo)
        dp.register_callback_query_handler(UserMain.main, state=states.UserStart.geo, text='enter_menu')
        dp.register_message_handler(UserMain.user_menu, state=states.UserStart.user_menu)
        dp.register_message_handler(UserMain.om, state=states.UserStart.om)


class UserProfile:
    @staticmethod
    async def user_profile(message: types.Message):
        if "Main menu" in message.text:
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the main menu",
                                   reply_markup=markup_users.main_menu())
        if message.text == f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} About me":
            res = user_get_db_obj.user_about(message.from_user.id)[0]
            await bot.send_message(message.from_user.id,
                                   f"Your information about yourself\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"<b>{res}</b>\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}",
                                   reply_markup=markup_users.user_profile())
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
            await states.UserProfile.about_me.set()

    @staticmethod
    async def update_location(message: types.Message, state: FSMContext):
        try:
            n = Nominatim(user_agent='User')
            loc = f"{message.location.latitude}, {message.location.longitude}"
            location = n.reverse(loc)
            country = location.raw.get("address").get("country")
            state_ = location.raw.get("address").get("state")
            city = location.raw.get("address").get("city")
            address = f'{location.raw.get("address").get("road")} - {location.raw.get("address").get("house_number")}'
            latitude = location.raw.get("lat")
            longitude = location.raw.get("lon")
            if city is None:
                city = location.raw.get("address").get("town")
            await bot.send_message(message.from_user.id,
                                   f'Country: {country}\n'
                                   f'State: {state_}\n'
                                   f'City: {city}\n'
                                   f'Address: {address}\n')
            if country is None:
                await bot.send_message(message.from_user.id,
                                       "Your location has not been determined"
                                       "Submit your location again",
                                       reply_markup=markup_start.update_location())
            if country and message.reply_to_message.text:
                await bot.send_message(message.from_user.id,
                                       "Please check the coordinates, if you made a mistake, "
                                       "you can send the geolocation again. If everything is ok, "
                                       "click Enter Main Menu",
                                       reply_markup=markup_start.update_location())
                async with state.proxy() as data:
                    data["country"] = country
                    data["state"] = state_
                    data["city"] = city
                    data["address"] = address
                    data["latitude"] = latitude
                    data["longitude"] = longitude
                    data["time_location"] = str(datetime.now())[:19]
            print(message.reply_to_message.text)
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
                                         data.get("city"),
                                         data.get("address"),
                                         data.get("latitude"),
                                         data.get("longitude"),
                                         data.get("time_location"))
            await states.UserStart.user_menu.set()
            await bot.send_message(callback.from_user.id,
                                   "Update completed!",
                                   reply_markup=markup_users.main_menu(),
                                   )

    @staticmethod
    async def update_about_me(message: types.Message):
        if message.text != f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            user_set_db_obj.user_set_about_me(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id,
                                   "<b>Successfully!</b>",
                                   reply_markup=markup_users.user_profile())
            await states.UserProfile.my_profile.set()
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back":
            await bot.send_message(message.from_user.id,
                                   "<b>You are back in My Profile</b>",
                                   reply_markup=markup_users.user_profile())
            await states.UserProfile.my_profile.set()

    @staticmethod
    def register_user_profile(dp):
        dp.register_message_handler(UserProfile.user_profile,
                                    state=states.UserProfile.my_profile)
        dp.register_message_handler(UserProfile.update_location, content_types=['location', 'text'],
                                    state=states.UserProfile.update_location)
        dp.register_callback_query_handler(UserProfile.update_location_menu,
                                           state=states.UserProfile.update_location)
        dp.register_message_handler(UserProfile.update_about_me,
                                    state=states.UserProfile.about_me)


class Locations:
    @staticmethod
    async def main(message: types.Message):
        await bot.delete_message(message.from_user.id, message.message.message_id)
        await bot.send_message(message.from_user.id,
                               f"{message.from_user.first_name} You are in the main menu",
                               reply_markup=markup_users.main_menu())
        await states.UserStart.user_menu.set()

    @staticmethod
    async def info(callback: types.CallbackQuery):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        res = global_get_db_obj.all_users()
        country = []
        for i in res:
            country.append(i[7])
        inline_country = InlineKeyboardMarkup()
        countrys = Counter(country)
        for k, v in countrys.items():
            inline_country.insert(InlineKeyboardButton(text=f'{k} ({v})', callback_data=f'country_{k}'))
        inline_country.insert(InlineKeyboardButton(text="Back", callback_data="main_menu"))
        await bot.send_message(callback.from_user.id,
                               f"Display all countries in which there are friends",
                               reply_markup=inline_country)
        await bot.send_message(callback.from_user.id,
                               "Select a country or return to the main menu",
                               reply_markup=markup_start.markup_clean)

    @staticmethod
    def register_info(dp):
        dp.register_callback_query_handler(Locations.info,
                                           state=states.Information.info, text='go_info')
        dp.register_callback_query_handler(Locations.main,
                                           state=states.Information.info, text='main_menu')


class Feedback:
    @staticmethod
    async def help(message: types.Message):
        if message.text == f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu":
            await bot.send_message(message.from_user.id,
                                   f"{message.from_user.first_name} You are in the main menu",
                                   reply_markup=markup_users.main_menu())
            await states.UserStart.user_menu.set()
        if message.text != f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu":
            await bot.send_message('@sunsurfers_bot_help',
                                   f"Name {message.from_user.first_name}\n"
                                   f"ID {message.from_user.id}\n"
                                   f"Message - <b>{message.text}</b>\n")
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   "Message sent to tech support!",
                                   reply_markup=markup_users.main_menu())

    @staticmethod
    def register_feedback(dp):
        dp.register_message_handler(Feedback.help,
                                    state=states.Feedback.help)
