from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import os
from pathlib import Path
import Posting
import menu_and_callback
from menu_and_callback import create_menu, process_button1, process_button2

bot_token = os.environ.get('bot_token')
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
hours = 24
count_message = 0
text_to_photo = {}


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
async def posting_command(message: Message):
    global hours
    await menu_and_callback.create_menu(message)
    # Posting.posting(text_to_photo, hours)



@dp.message_handler(commands=['stop'])
async def clear_data(message: Message):
    global count_message
    global text_to_photo
    text_to_photo = {}
    count_message = 0
    # Получаем список файлов и папок в указанной папке
    folder_path = ".\images"
    files = os.listdir(folder_path)
    # Проходим по каждому файлу/папке
    for file_name in files:
        # Формируем полный путь к файлу/папке
        file_path = os.path.join(folder_path, file_name)

        # Проверяем, является ли объект файлом
        if os.path.isfile(file_path):
            # Если это файл, удаляем его
            os.remove(file_path)
    print(text_to_photo)
    await message.answer('Данные изображений и текстов очищены \n Таймер удаления постов выставлен на 24 часа')


@dp.message_handler(content_types=types.ContentTypes.ANY, is_forwarded=True)
async def saver_msg(message: Message):
    """ Перехватывает ПЕРЕСЛАНЫЕ сообщения и сохраняет фото и текст"""

    print('//////    New forwarded message   //////')
    try:
        global count_message
        global text_to_photo
        file_id = message.photo[-1]["file_id"]
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file_extension = Path(file_path).suffix
        file_name = f"{count_message}{file_extension}"
        save_path = f"images/{file_name}"
        count_message += 1
        # Сохраняем файл на компьютере
        await bot.download_file(file_path, save_path)
        full_pass = os.path.abspath(save_path)
        text = message.caption
        if text:
            text_to_photo[text] = full_pass
            print(text_to_photo)
            await message.answer(f'Изображение ({file_name}) сохранено в:\n' + full_pass)
        else:
            await message.answer("Похоже пересланное сообщение не содержит текста")
    except:
        await message.answer("Похоже пересланное сообщение не содержит изображения")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def time_to_delete(message: Message):
    try:
        global hours
        hours = int(message.text)
        await message.answer(f"Таймер удаления постов выставлен на {hours}ч")
    except:
        await message.answer('Введите число')

dp.register_callback_query_handler(process_button1, lambda c: c.data == 'button1')
dp.register_callback_query_handler(process_button2, lambda c: c.data == 'button2')

executor.start_polling(dp, skip_updates=True)
