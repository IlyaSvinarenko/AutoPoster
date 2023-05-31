from aiogram import types


# Функция для создания инлайн-меню
async def create_menu_straight_revers_queue(message: types.Message):
    # Создаем инлайн-клавиатуру
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    # Создаем две кнопки с уникальными callback_data
    button1 = types.InlineKeyboardButton(text="Кнопка 1", callback_data='button1')
    button2 = types.InlineKeyboardButton(text="Кнопка 2", callback_data='button2')
    # Добавляем кнопки в меню
    inline_keyboard.add(button1, button2)

    # Отправляем сообщение с инлайн-меню
    await message.reply("Выберите действие:", reply_markup=inline_keyboard)


# Обработчик события для первой кнопки
async def straight_revers_queue_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("Вы нажали на кнопку 1!")

