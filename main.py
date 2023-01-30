from aiogram.utils import executor
from create_bot import dp
from handlers import client, filter   # Импортируем модули

# Обрабатываем сообщения
client.register_handlers_client(dp)
filter.register_handlers_client(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

