from aiogram import types, Dispatcher
from create_bot import bot, dp, db
import config as cfg
from inline.markup import chatChannel



def check_member(chat_member):
    return chat_member['status'] != 'left'

async def new_member_chat(message: types.Message):
    await message.answer('Добро пожаловать\nЧтобы отправлять сообщения, подпишитесь на канал', reply_markup=chatChannel)
async def filter_chat(message: types.Message):
    if not db.user_chat_is(message.from_user.id):
        db.add_user_chat(message.from_user.id)
    # проверка подписки на канал
    if check_member(await bot.get_chat_member(chat_id=cfg.CHANNEL_ID, user_id=message.from_user.id)):

        # проверка мута
        if not db.mute_is(message.from_user.id):

            # фильтр слов в общем чате
            if message.chat.type == 'supergroup':
                text = message.text.lower()
                for word in cfg.WORDS:
                    if word in text:
                        await message.delete()
        else:
            await message.answer('Вы в муте')
            await message.delete()
    else:
        await message.answer('Чтобы отправлять сообщения, подпишитесь на канал', reply_markup=chatChannel)
        await message.delete()

def register_other_message(dp: Dispatcher):
    dp.register_message_handler(filter_chat)
    dp.register_message_handler(new_member_chat, content_types=['new_chat_members'])