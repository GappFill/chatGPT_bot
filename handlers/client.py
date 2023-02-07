from create_bot import bot, dp
from aiogram import types, Dispatcher
from datetime import datetime
import openai
import work_db
from keyboard import kb
from useful import days_to_seconds, chatGPT_response
import time

from dotenvy import load_env, read_file
from os import environ
load_env(read_file('.env'))
openai.api_key = environ.get('OPENAI_API_KEY')
SHOP_API_TOKEN = environ.get('SHOP_API_TOKEN')

lets_meet_bot = '📌 Давайте познакомимся. Нажмите кнопку ниже'
lets_meet_chatGPT = '📌 Теперь нейронка GPT расскажет о себе'
pay_text = '🥸  Чтобы начать пользоваться поиском нового поколения купите подписку \n\n14 дней безлимитного поиска всего за 99 рублей. Результат удивит или мы вернем вам деньги! \n\nПо административным вопросам: @ochulaevskii'
question_text =f"<b>🔍 Задайте мне вопрос!</b>\n\nПостарайтесь включить в поисковый запрос конкретику.\nЧем детальней вопрос, тем релевантней ответ"




async def start(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)  # Удаляет сообщение страт
    await bot.send_message(message.from_user.id,
                        lets_meet_bot,
                        parse_mode='html',
                        reply_markup=kb.about_bot_line)
    work_db.insert_new_user(message.from_user.id, message.from_user.username, datetime.now().strftime("%d-%m-%Y "), 0)  # Записывает пользователя ы базу данных


@dp.callback_query_handler(text='/about_bot')
async def about_bot(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id,
                     text='здесь сообщение о боте (захардкожено)',
                           )
    await bot.send_message(chat_id=callback.from_user.id,
                           text=lets_meet_chatGPT,
                           reply_markup=kb.about_chatGPT_line)




@dp.callback_query_handler(text='/about_chatGPT')
async def about_chatGPT(callback: types.CallbackQuery):
    msg_stiker = await bot.send_sticker(callback.from_user.id,
                                        'CAACAgIAAxkBAAEGRIFjYDB2O_zAbzSB6kCUIrfPqdk8TgACIwADKA9qFCdRJeeMIKQGKgQ')
    await bot.send_message(chat_id=callback.from_user.id,
                           text=chatGPT_response('Что такое chatGPT?'),)
    await bot.send_message(chat_id=callback.from_user.id,
                           text=question_text,
                           parse_mode='html')
    await msg_stiker.delete()



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
        sub_counter = work_db.get_subcribe(message.from_user.id)[0] + 1
        work_db.update_subcribe(message.from_user.id,time_sub, sub_counter)  # Update time sub after succes pay
        await bot.send_message(message.from_user.id,question_text,
                        parse_mode='html')



async def bot_answer_from_openai(message: types.Message):
    response = work_db.check_subcribe(message.from_user.id)
    if response == 1:
        msg_stiker = await bot.send_sticker(message.chat.id,
                                     'CAACAgIAAxkBAAEGRIFjYDB2O_zAbzSB6kCUIrfPqdk8TgACIwADKA9qFCdRJeeMIKQGKgQ')
        await bot.send_message(chat_id=message.from_user.id,
                               text=chatGPT_response(message.text))
        await msg_stiker.delete()
    elif response == 2:
        await start(message)
    else:
        if work_db.get_subcribe(message.from_user.id)[1] > 0:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Ваша подписка закончилась')
        else:
            await pay(message)





def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(bot_answer_from_openai)
    dp.register_message_handler(about_chatGPT)
    dp.register_message_handler(about_bot)
    dp.register_message_handler(pre_checkout)
    dp.register_message_handler(process_pay, content_types='SUCCESSFULL_PAYMENT')






