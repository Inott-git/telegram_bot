from aiogram import Dispatcher, types
from create_bot import db, bot


async def start(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_is(message.from_user.id):
            db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Hello')


def register_client_message(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
