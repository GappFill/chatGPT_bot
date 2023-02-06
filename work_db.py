# Файл для работы с базой данных

# import pymysql
# import cryptography
import time
import sqlite3


def connect():  # Подключаемся к базе данных
    try:
        conn = pymysql.connect(
            host="188.225.25.80",
            user="gen_user",
            passwd="ix8i9u9ab2",
            db="default_db",
            port=3306
        )
        cursor = conn.cursor()
    except Exception as err:
        print(err, 'Неудалось подключиться к базе данных')
    else:
        return cursor, conn

def insert_new_user(user_id, user_name, date, sub_counter):
    """Добавляет пользователя в базу данных"""
    try:
        with sqlite3.connect(r'database/users.db') as db:
            cursor = db.cursor()
            cursor.execute(
                """INSERT INTO users(id, user_id, user_name, count, date, sub_counter) VALUES(?, ?, ?, ?, ?, ?)""",
                (None, user_id, user_name, 0, date, sub_counter))
            return 1  # if the user was added
    except Exception as err:
        print(err)
        return 2  # if the user wasn't added


def get_sub(user_id):
    '''ПРоверяем подписку'''
    try:
        with sqlite3.connect(r'database/users.db') as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT count, sub_counter  FROM users WHERE user_id={user_id}""",)
            return cursor.fetchone()  # if the user was added
    except Exception as err:
        print(err)
        return 2  # if the user wasn't added

def update_sub(user_id, new_count, sub_counter):
    '''Обновляем время подписки'''
    try:
        with sqlite3.connect(r'database/users.db') as db:
            cursor = db.cursor()
            cursor.execute(f"""UPDATE users SET count={new_count},sub_counter={sub_counter} WHERE user_id={user_id}""",)
    except Exception as err:
        print(err)
        return 2


def check_sub(user_id):
    '''Смотрим сколько у пользователя использований доступно'''
    try:
        with sqlite3.connect(r'database/users.db') as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT count FROM users WHERE user_id={user_id}""",)
            if int(cursor.fetchone()[0]) > int(time.time()):
                return True
            else: return False

    except Exception as err:
        print(err)
        return 2  # if the user wasn't added

