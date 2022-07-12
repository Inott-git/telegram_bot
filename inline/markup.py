from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg

btnChannel = InlineKeyboardButton(text='Перейти на канал', url=cfg.CHANNEL_URl)
chatChannel = InlineKeyboardMarkup(row_width=1)
chatChannel.insert(btnChannel)