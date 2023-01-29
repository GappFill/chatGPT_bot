import logging
import openai
from dotenvy import load_env, read_file
from os import environ

load_env(read_file('.env'))

from aiogram import Bot, Dispatcher, executor, types



API_TOKEN = environ.get('API_TOKEN')
openai.api_key = environ.get('OPENAI_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Приветствую тебя !")



@dp.message_handler(lambda _: True)
async def bot_answer_from_openai(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="ChatGPT генерирут ответ на Ваше сообщение, подождите...")
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
    await msg_stiker.delete()
    await bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

