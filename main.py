import logging
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from fastapi import FastAPI

from bot import dp, bot
from data.commands import user_set
from users.user import UserMain
from markups import markup_start
from sun_api import api_users


app = FastAPI()
app.include_router(api_users.router)


@app.get("/")
def hello():
    return {"SunSurfers": "Hello World"}


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,
                           f'<b>Hello there</b>',
                           reply_markup=markup_start.markup_clean)
    await bot.send_message(message.from_user.id,
                           f'<b>Click start to start using the bot</b>',
                           reply_markup=markup_start.start())
    await UserMain.register_user_handler(dp)


async def on_startup(_):
    logging.basicConfig(level=logging.DEBUG)
    from data.db_gino import db
    from data import db_gino
    print("Database connected")
    await db_gino.on_startup(dp)

    """Удалить БД"""
    # await db.gino.drop_all()

    """Создание БД"""
    await db.gino.create_all()
    await user_set.add_sungatherings()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
