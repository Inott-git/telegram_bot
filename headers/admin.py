from aiogram import Dispatcher, types
from create_bot import db, bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config as cfg


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()


# рассылка сообщения
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == cfg.ADMIN_ID:
            text = message.text[9:]
            users = db.get_users()
            for item in users:
                try:
                    await bot.send_message(item[0], text)
                    if item[1] == 0:
                        db.set_active(item[0], 1)
                except:
                    db.set_active(item[0], 0)


# начало FSM
async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 868449417:
            await FSMAdmin.photo.set()
            await bot.send_message(message.from_user.id, 'Отправьте фото')


# ловим фото
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Название:')


# загрузка имени
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Описание:')


# получение описания
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        data_fsm = data
        await state.finish()
        # выход из состояния

        # рассылка fsm_сообщения
        users = db.get_users()
        for item in users:
            try:
                await bot.send_photo(item[0], data_fsm['photo'], f"{data_fsm['name']}\n{data_fsm['description']}")
                await bot.send_message(item[0], 'test')
                if item[1] == 0:
                        db.set_active(item[0], 1)

            except Exception as ex:
                db.set_active(item[0], 0)
                print(ex)


async def set_mute(message: types.Message):
    if message.chat.type == 'supergroup':
        if message.from_user.id == cfg.ADMIN_ID:
            if not message.reply_to_message:
                await message.answer('Нет указания сообщения')

            mute_sec = int(message[6:])
            db.add_mute(message.reply_to_message.from_user.id, mute_sec)


def register_admin_message(dp: Dispatcher):
    dp.register_message_handler(sendall, commands=['sendall'])
    dp.register_message_handler(fsm_start, commands=['sendall_fsm'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
