import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import Database
from config import token

logging.basicConfig(level=logging.INFO)

API_TOKEN = token # в файле config.py токен

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
db = Database('database.db')