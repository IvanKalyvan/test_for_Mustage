from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Додати статтю витрат')],
                                      [KeyboardButton(text='Отримати звіт витрат')],
                                     [KeyboardButton(text='Видалити статтю')],
                                     [KeyboardButton(text='Відредагувати статтю')]],
                                       resize_keyboard=True)