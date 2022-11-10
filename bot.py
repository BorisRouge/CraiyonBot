from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils import settings
from utils.db_manager import Database  # To be used to store the images.
from utils.logger import get_logger


log = get_logger()
config = settings.get_config("sample.env")
bot = Bot(token=config.telegram.telegram_bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(config.database.con_data, log)

