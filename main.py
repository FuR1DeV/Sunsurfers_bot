from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from geopy import Nominatim

from bot import dp, bot
from data import create_db, get_set_db
from users.user import UserMain
from markups import markup_start
from settings import config
from states import states


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,
                           f'<b>Hello there</b>'
                           , reply_markup=markup_start.markup_clean)
    await bot.send_message(message.from_user.id,
                           f'<b>Click start to start using the bot</b>'
                           , reply_markup=markup_start.start())
    UserMain.register_user_handler(dp)

# @dp.message_handler(commands='admin', state='*')
# async def admin(message: types.Message, state: FSMContext):
#     await state.finish()
#     if str(message.from_user.id) in config.ADMIN_ID:
#         if not admin_get_db_obj.admin_exists(message.from_user.id):
#             admin_get_db_obj.admin_add(message.from_user.id,
#                                        message.from_user.username,
#                                        message.from_user.first_name,
#                                        message.from_user.last_name)
#         AdminMain.register_admin_handler(dp)
#         await bot.send_message(message.from_user.id,
#                                f'Добро пожаловать в панель администратора',
#                                reply_markup=markup_admin.admin_main())
#         await states.AdminStates.enter.set()
#     else:
#         await bot.send_message(message.from_user.id, "У вас нет прав доступа!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
