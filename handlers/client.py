import useful
from create_bot import bot, dp
from aiogram import types, Dispatcher
from datetime import datetime
import openai
import work_db
from keyboard import kb
from useful import days_to_seconds, chatGPT_response, create_mask
import time

from dotenvy import load_env, read_file
from os import environ
load_env(read_file('.env'))
openai.api_key = environ.get('OPENAI_API_KEY')
SHOP_API_TOKEN = environ.get('SHOP_API_TOKEN')


start_message = 'Привет! \n' \
           'Меня зовут Алиса и я помогу тебе иметь постоянный доступ к ChatGPT ⚡️\n\n' \
           '- кто ты, ChatGPT?\n\n' \
           'Я являюсь системой искусственного интеллекта, которая была обучена на огромном количестве данных, включая код, документацию и различные примеры. Я использую это обучение, чтобы генерировать ответы на вопросы, которые мне задают. Если у вас есть какие-то конкретные вопросы или проблемы с кодом, я буду стараться помочь вам как можно лучше.\n\n' \
           'Преимущества использовать наш бот: \n' \
           '1. Поиск через ChatGPT гражданам СНГ (регистрация из СНГ на сайте недоступна)\n' \
           '2. Через бот получайте ответы даже тогда, когда веб-сайт закрыт из-за высокой нагрузки \n\n' \
           'По административным вопросам обращайтесь к @ochulaevskii'

pay_text = '🥸  Чтобы начать пользоваться поиском нового поколения купите подписку \n\n14 дней безлимитного поиска всего за 99 рублей. Результат удивит или мы вернем вам деньги! \n\nПо административным вопросам: @ochulaevskii'
question_text =f"<b>🔍 Задайте мне вопрос!</b>\n\nПостарайтесь включить в поисковый запрос конкретику.\nЧем детальней вопрос, тем релевантней ответ"




async def start(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)  # Удаляет сообщение страт
    await bot.send_message(message.from_user.id,
                        start_message,
                        parse_mode='html',)

    await bot.send_message(message.from_user.id,
                           question_text,
                           parse_mode='html', )

    work_db.insert_new_user(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.id)  # Записывает пользователя ы базу данных
    work_db.insert_subscription(message.from_user.id, 0, True, 0)


async def pay(message: types.Message):  # Функция оплаты платежа
    await bot.send_invoice(chat_id=message.from_user.id,
                           title='Разблокировка поиска нового поколения',
                           description=pay_text,
                           payload='14_days',
                           currency='RUB',
                           prices=[{'label': ' Руб', 'amount': 9900}],
                           photo_width=1250,
                           photo_height=725,
                           photo_url='https://avatars.mds.yandex.net/get-images-cbir/6930134/zCjOsx7CdGkw7Y9WL_Lzdw118/ocr',
                           provider_token=SHOP_API_TOKEN,
    )

@dp.pre_checkout_query_handler()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == '14_days':
        time_sub = int(time.time()) + int(days_to_seconds(14))
        work_db.update_subscription(message.from_user.id, time_sub, 99)  # Update time sub after succes pay
        await bot.send_message(message.from_user.id,question_text,
                        parse_mode='html')



async def bot_answer_from_openai(message: types.Message):
    response = work_db.check_subscription(message.from_user.id)
    if response == 1:
        msg_stiker = await bot.send_sticker(message.chat.id,
                                     'CAACAgIAAxkBAAEGRIFjYDB2O_zAbzSB6kCUIrfPqdk8TgACIwADKA9qFCdRJeeMIKQGKgQ')
        await bot.send_message(chat_id=message.from_user.id,
                               text=chatGPT_response(message.text))
        await msg_stiker.delete()

    elif response == 0:
        msg_stiker = await bot.send_sticker(message.chat.id,
                                            'CAACAgIAAxkBAAEGRIFjYDB2O_zAbzSB6kCUIrfPqdk8TgACIwADKA9qFCdRJeeMIKQGKgQ')
        await bot.send_message(chat_id=message.from_user.id,
                               text=useful.create_mask(chatGPT_response(message.text)))
        await msg_stiker.delete()

    elif response == 3:
        await bot.send_message(message.from_user.id, '🥸 Ваша подписка закончилась!\n Продлите подписку, чтобы пользоваться поиском нового поколения',
                               parse_mode='html')
        await pay(message)

    elif response == 2:
        await start(message)





def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(bot_answer_from_openai)
    dp.register_message_handler(pre_checkout)
    dp.register_message_handler(process_pay, content_types='SUCCESSFULL_PAYMENT')






