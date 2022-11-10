import requests
import aiohttp

from aiogram.types import Message, MediaGroup, InputMediaPhoto, InputFile

from bot import bot, dp, db, log
from utils.translator import translate_api
from utils.translator.token import Token
from utils.file_manager import Images

token = Token().get_token()



async def welcome(message: Message):
    """Запуск диалога с ботом."""
    # user_data = db.user_info(message.from_user.id)
    # if user_data is False:
    #     db.user_create(message.from_user.id)
    await message.answer('Напиши словесное описание того, что хочешь видеть '
                         'нарисованным. Например, "Ельцин носит латы".')


async def draw(message: Message):
    """Отправляет запрос Craiyon и возвращает изображения."""
    # Просим пользователя подождать.
    await message.answer('Подожди 1-2 минуты.')
    prompt = message.text  # The arguments come as a list, and we need a single string.
    log.info(f'The requested prompt is: {prompt}')
    # Send into translation API with the prompt text and initial IAM Token.
    try:
        translated = translate_api.translate(prompt, token)
    except PermissionError:
        new_token = Token().get_token()
        translated = translate_api.translate(prompt, new_token)
    log.info(f'It has been translated as: {translated}')
    # Request and response.
    async with aiohttp.ClientSession() as session:
        async with session.post('https://backend.craiyon.com/generate',
                                 # !!! Now it can respond with 'Too much traffic'. Gotta log the response.
                                 json={"prompt": translated}) as response:
            log.info(f"Craiyon's response: {response.status}")
    # Response comes as a dict with a list of b64-encoded images {'images':[]}.
    # Decode, save to filesystem and send to the same chat.
            images = Images(data=await response.json(),
                            owner=message.from_id,
                            prompt=translated)
            images.save_images()
            media_group = MediaGroup()
            for image_path in images.paths:
                media_unit = InputFile(image_path)
                media_group.attach_photo(media_unit)
            db.save_image_paths(message.from_id, images.paths)
            await message.answer_media_group(media_group)


def register_user(d: dp):
    d.register_message_handler(welcome, commands=['start'])
    d.register_message_handler(draw)
    