from aiogram import executor
from bot import dp
from handlers.user import register_user


register_user(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# TODO: Database
# TODO: Throttling
# TODO: Рассмотреть функцию draw на предмет SOLID