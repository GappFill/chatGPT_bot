from create_bot import bot, dp
from aiogram import types, Dispatcher
from datetime import datetime
import openai
import work_db

import time

from dotenvy import load_env, read_file
from os import environ
load_env(read_file('.env'))
openai.api_key = environ.get('OPENAI_API_KEY')
SHOP_API_TOKEN = environ.get('SHOP_API_TOKEN')


def days_to_seconds(days):
    return days*24*60*60

async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                        f"🔍 Задайте мне вопрос!\n\n"
                        f"Постарайтесь включить в поисковый запрос конкретику.\n"
                        f"Чем детальней вопрос, тем релевантней ответ")
    work_db.insert_new_user(message.from_user.id, message.from_user.username, datetime.now().strftime("%d-%m-%Y "), 0)  # Записывает пользователя ы базу данных
    await bot.delete_message(message.from_user.id, message.message_id)  # Удаляет сообщение страт



async def pay(message: types.Message):  # Функция оплаты платежа
    await bot.send_invoice(chat_id=message.from_user.id,
                           title='Оплата',
                           description='14 дневная подписка',
                           payload='14_days',
                           currency='RUB',
                           prices=[{'label': ' Руб', 'amount': 9000}],
                           provider_token=SHOP_API_TOKEN, )

@dp.pre_checkout_query_handler()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == '14_days':
        time_sub = int(time.time()) + int(days_to_seconds(14))
        sub_counter = work_db.get_sub(message.from_user.id)[0] + 1
        work_db.update_sub(message.from_user.id,time_sub, sub_counter)  # Update time sub after succes pay
        await bot.send_message(message.from_user.id,
                               f"🔍 Задайте мне вопрос!\n\n"
                               f"Постарайтесь включить в поисковый запрос конкретику.\n"
                               f"Чем детальней вопрос, тем релевантней ответ")



async def bot_answer_from_openai(message: types.Message):
    # Получить количество доступных использований
    if work_db.check_sub(message.from_user.id):
        msg_stiker = await bot.send_sticker(message.chat.id,
                                     'CAACAgIAAxkBAAEGRIFjYDB2O_zAbzSB6kCUIrfPqdk8TgACIwADKA9qFCdRJeeMIKQGKgQ')
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=message.text,
                temperature=0.5,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=0.0,
            )
            await msg_stiker.delete()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=response['choices'][0]['text'])
        except:
            await msg_stiker.delete()
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Сервер chatGPT перегружен")
    else:
        if work_db.get_sub(message.from_user.id)[1] > 0:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Ваша подписка закончилась')
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='🥸 Чтобы начать пользоваться\n'
                                  'поиском нового поколения\n'
                                  'купите подписку\n'
                                  '14 дней безлимитного поиска всего за\n 99 рублей.'
                                  'Результат удивит или мы вернем вам деньги!\n'
                                  'По административным вопросам:\n @ochulaevskii') # Выводится если у пользователя закончились использования
        await pay(message)



def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(bot_answer_from_openai)
    dp.register_message_handler(pre_checkout)
    dp.register_message_handler(process_pay, content_types='SUCCESSFULL_PAYMENT')






