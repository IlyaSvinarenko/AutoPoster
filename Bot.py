from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import os
from pathlib import Path
import menu_and_callback
from aiogram.dispatcher import FSMContext

bot_token = os.environ.get('bot_token')
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
hours = 24
count_message = 0
text_to_media = []
queue = ["Прямая", "Обратная"]
flag_queue = 0
saved_message = {}


@dp.message_handler(commands=['help'])
async def help(message: Message):
    await message.answer('Бот предназначен для автопостинга на fansly.com\n'
                         'Чтобы сделать посты автоматически нужно:\n'
                         '- Переслать боту одно и более сообщений (сообщение обязательно должно состоять из текста и '
                         'изображения)\n'
                         '- Ввести число, обозначающее количество часов для отложенного удаления поста\n'
                         '- Ввести команду /posting\n'
                         '- После завершения цикла постинга ввести в боте команду /stop (это очистит данные с вашего '
                         'устройства, которые были запосщены)')


@dp.message_handler(commands=['posting'])
async def posting_command(message: Message, state: FSMContext):
    global hours
    global text_to_media
    text_to_media = sorted(text_to_media, key=lambda x: x[1])
    await menu_and_callback.create_pre_posting_menu(message, queue[flag_queue], hours)


@dp.message_handler(commands=['stop'])
async def clear_data(message: Message):
    global count_message
    global text_to_media
    text_to_media = []
    count_message = 0
    folder_path = ".\media"
    files = os.listdir(folder_path)
    for file_name in files:
        # Формируем полный путь к файлу/папке
        file_path = os.path.join(folder_path, file_name)
        # Проверяем, является ли объект файлом
        if os.path.isfile(file_path):
            os.remove(file_path)
    print(text_to_media)
    await message.answer('Данные изображений и текстов очищены \n Таймер удаления постов выставлен на 24 часа')



@dp.message_handler(content_types=types.ContentTypes.ANY, is_forwarded=True)
async def saver_msg(message: Message):
    """ Перехватывает ПЕРЕСЛАНЫЕ сообщения и сохраняет медиа и текст"""

    print('//////    New forwarded message   //////')
    try:
        global saved_message
        global count_message
        global text_to_media
        media_types = (message.photo, message.video, message.animation)
        for type in media_types:
            if type:
                if type is message.photo:
                    file_id = type[-1]["file_id"]
                else:
                    file_id = type.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file_extension = Path(file_path).suffix
        if not file_extension:
            file_extension = '.mp4'
        file_name = f"{message.message_id}{file_extension}"
        save_path = f"media/{file_name}"
        # Сохраняем файл на компьютере
        await bot.download_file(file_path, save_path)
        full_pass = os.path.abspath(save_path)
        text = message.caption
        if text:
            print((f'Изображение ({file_name}) сохранено в:\n' + full_pass))
            text_to_media.append([text, full_pass])
            await message.answer(f'Изображение ({file_name}) сохранено в:\n' + full_pass)

        else:
            await message.answer("Похоже пересланное сообщение не содержит текста")

    except:
        await message.answer("Похоже пересланное сообщение не содержит медиа")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def time_to_delete(message: Message):
    try:
        global hours
        hours = int(message.text)
        await message.answer(f"Таймер удаления постов выставлен на {hours}ч")
    except:
        await message.answer('Введите число')


@dp.callback_query_handler(lambda query: query.data.startswith('m1'))
async def callback(callback_query: types.CallbackQuery):
    global text_to_media
    global flag_queue
    is_reverse = await menu_and_callback.callback_from_pre_posting_menu(callback_query, text_to_media, hours)
    if is_reverse:
        flag_queue = (flag_queue + 1) % 2
        text_to_media = text_to_media[::-1]
        print(queue[flag_queue], text_to_media)
        await callback_query.message.delete()
        await menu_and_callback.create_pre_posting_menu(callback_query.message, queue[flag_queue], hours)


executor.start_polling(dp, skip_updates=True)
