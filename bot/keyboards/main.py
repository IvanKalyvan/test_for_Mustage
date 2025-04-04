from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Додати статтю витрат')],
                                      [KeyboardButton(text='Отримати звіт витрат')],
                                     [KeyboardButton(text='Видалити статтю')],
                                     [KeyboardButton(text='Відредагувати статтю')]],
                                       resize_keyboard=True)
skip_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Skip", callback_data="skip")]])