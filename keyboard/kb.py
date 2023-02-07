from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


about_bot = InlineKeyboardButton(text='about_bot', callback_data='/about_bot')

about_chatGPT = InlineKeyboardButton(text='about_chatGPT', callback_data='/about_chatGPT')

about_bot_line = InlineKeyboardMarkup(row_width=1).add(about_bot )
about_chatGPT_line = InlineKeyboardMarkup(row_width=1).add(about_chatGPT)



