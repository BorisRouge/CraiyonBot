from dataclasses import dataclass
from environs import Env


@dataclass
class Database:
    con_data: str


@dataclass
class Telegram:
    telegram_bot_token: str


@dataclass
class Translator:
    service_account_id: str
    key_id: str


@dataclass
class Settings:
    database: Database
    telegram: Telegram
    translator: Translator


def get_config(path: str = None):
    """Получение переменных из указанной среды."""
    env = Env()
    env.read_env(path)
    return Settings(
        database=Database(f"""dbname={env.str('DB')}
                          user={env.str('DBUSER')}
                          password={env.str('DBPASS')}""",
                          ),
        telegram=Telegram(telegram_bot_token=env.str('TELEGRAM_BOT_TOKEN'),
                          ),
        translator=Translator(service_account_id=env.str('SERVICE_ACCOUNT_ID'),
                              key_id=env.str('KEY_ID'))
    )
