from create_bot import bot, dp
from aiogram import types, Dispatcher
from datetime import datetime
import openai
import work_db


from dotenvy import load_env, read_file
from os import environ
load_env(read_file('.env'))
openai.api_key = environ.get('OPENAI_API_KEY')
SHOP_API_TOKEN = environ.get('SHOP_API_TOKEN')


async def start(message: types.Message):
    await message.reply("Отправьте конкретный и детальный вопрос, чтобы получить самый релевантный ответ")
    await bot.send_invoice(chat_id=message.from_user.id,
                           title='Оплата',
                           description='test',
                           payload='5_counts',
                           currency='RUB',
                           prices=[{'label':' Руб', 'amount':9000}],
                           provider_token=SHOP_API_TOKEN,)
    work_db.insert_new_user(message.from_user.id, message.from_user.username, datetime.now().strftime("%d-%m-%Y "))

@dp.pre_checkout_query_handler()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == '5_counts':
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=open('telegram-premium-logo.png', 'rb'),
                             caption='Оплата прошла')
        #await bot.send_message(chat_id=message.from_user.id, text="Оплата прошла")



async def bot_answer_from_openai(message: types.Message):
    count = work_db.check_count(message.from_user.id)[0]  # Получить количество доступных использований
    if 0 < count <= 5:
        msg_text = await bot.send_message(chat_id=message.from_user.id, text="ChatGPT генерирут ответ на Ваше сообщение, подождите...")
        msg_stiker = await bot.send_sticker(message.chat.id,
                                     'CAACAgIAAxkBAAEGRIFjYDB2O_zAbzSB6kCUIrfPqdk8TgACIwADKA9qFCdRJeeMIKQGKgQ')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        await msg_text.delete()
        await msg_stiker.delete()
        await bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
        work_db.update_count(message.from_user.id, count-1)
    else:
        await bot.send_message(chat_id=message.from_user.id, text='Ссори примогемы закончились')  # Выводится если у пользователя закончились использования



def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(bot_answer_from_openai)
    dp.register_message_handler(pre_checkout)
    dp.register_message_handler(process_pay, content_types='SUCCESSFULL_PAYMENT')






