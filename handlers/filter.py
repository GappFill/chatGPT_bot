from aiogram import types, Dispatcher
from create_bot import bot, dp
from handlers import client


async def check_message(message: types.Message):
    if message.content_type == 'text':
        if str(message.text) == '/start':
            await client.start(message)
    elif message.content_type == 'successful_payment':
        await client.process_pay(message)
    else:
        print(message.content_type)  # Показывает тип сообщения
        await bot.send_message(message.chat.id,
                               "Пока я могу обрабатывать только текст")
        await bot.delete_message(message.chat.id, message.message_id)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(check_message, content_types=['any'])

