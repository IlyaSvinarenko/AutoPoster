from aiogram import types
import Posting
import logins_and_passwords


async def create_pre_posting_menu(message: types.Message, queue, hours):
    # Создаем инлайн-клавиатуру
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    # Создаем две кнопки с уникальными callback_data
    button1 = types.InlineKeyboardButton(text="Развернуть последовательность", callback_data='m1 reverse')
    button2 = types.InlineKeyboardButton(text="Начать постинг", callback_data='m1 posting')
    # Добавляем кнопки в меню
    inline_keyboard.add(button1, button2)

    await message.answer(f"Последовательность постинга: {queue}\n"
                         f"Отложенное удаление: {hours}ч", reply_markup=inline_keyboard)


async def revers_queue_or_posting(callback_query: types.CallbackQuery, text_to_photo, hours):
    call = callback_query.data.split()
    if call[1] == 'reverse':
        return True
    elif call[1] == 'posting':
        for account_data in logins_and_passwords.get_accounts_data():
            login = account_data[0]
            password = account_data[1]
            Posting.fansly_open(text_to_photo, hours, login, password)
