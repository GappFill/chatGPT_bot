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

def insert_new_user(user_id, user_name, date):
    """Добавляет пользователя в базу данных"""
    try:
        with sqlite3.connect(r'database/users.db') as db:
            cursor = db.cursor()
            cursor.execute(
                """INSERT INTO users(id, user_id, user_name, count, date) VALUES(?, ?, ?, ?, ?)""",
                (None, user_id, user_name, 5, date))
            return 1  # if the user was added
    except Exception as err:
        print(err)
        return 2  # if the user wasn't added


def check_count(user_id):
    '''Смотрим сколько у пользователя использований доступно'''
    try:
        with sqlite3.connect(r'database/users.db') as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT count FROM users WHERE user_id={user_id}""",)
            return cursor.fetchone()  # if the user was added
    except Exception as err:
        print(err)
        return 2  # if the user wasn't added

def update_count(user_id, new_count):
    '''Обновляем количество использований'''
    try:
        with sqlite3.connect(r'database/users.db') as db:
            cursor = db.cursor()
            cursor.execute(f"""UPDATE users SET count={new_count} WHERE user_id={user_id}""",)
    except Exception as err:
        print(err)
        return 2  # if the user wasn't added


def check_date(user_id):
    '''Смотрим сколько у пользователя использований доступно'''
    try:
        with sqlite3.connect(r'database/users.db') as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT date FROM users WHERE user_id={user_id}""",)
            return cursor.fetchone()  # if the user was added
    except Exception as err:
        print(err)
        return 2  # if the user wasn't added

