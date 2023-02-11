# Файл для работы с базой данных

import pymysql
import cryptography
import time
import sqlite3


def connect():  # Подключаемся к базе данных
    try:
        conn = pymysql.connect(
            host="81.200.144.220",
            user="gen_user",
            passwd="1ly8czoqk6",
            db="default_db",
            port=3306
        )
        cursor = conn.cursor()
    except Exception as err:
        print(err, 'Неудалось подключиться к базе данных')
    else:
        return cursor, conn

def insert_new_user(first_name, last_name, username, id):
    """Добавляет пользователя в базу данных"""
    try:
        cursor = connect()
        cursor[0].execute(
            """INSERT INTO Users(id, first_name, last_name, nickname, user_id) VALUES(%s, %s, %s, %s, %s)""",
            (None, first_name, last_name, username, id))
        cursor[1].commit()
        return 1  # if the user was added
    except Exception as err:
        return 2  # if the user wasn't added


def update_subscription(user_id, expired_date, price):
    '''Возвращает время подписки и счетчик купленных подписок конкретного пользователя'''
    try:
        cursor = connect()
        cursor[0].execute(f"""UPDATE Transactions SET expired_date={expired_date}, price={price} WHERE user_id={user_id}""")
        cursor[1].commit()
    except Exception as err:
        print(err)
        return 2  #


def insert_subscription(user_id, expired_date, trial_request, price):
    '''Добавить подписку'''
    try:
        cursor = connect()
        cursor[0].execute(f"""INSERT INTO Transactions(id, user_id, expired_date, trial_request, price) VALUES(%s, %s, %s, %s, %s)""",
                          (None, user_id, expired_date, trial_request, price))
        cursor[1].commit()
    except Exception as err:
        return err


def check_subscription(user_id):
    '''Проверяем есть у пользователя активная подписка'''
    try:
        cursor = connect()
        cursor[0].execute(f"""SELECT expired_date, trial_request FROM Transactions WHERE user_id={user_id}""",)
        all =  cursor[0].fetchone()
        if int(all[0]) > int(time.time()):  # Есть ли подписка
            return True  # У пользователя есть подписка
        elif int(all[0]) > 0:
            return 3  # Была но закончилась
        else:
            return False  # У пользователя нет подписки
    except Exception as err:  # Пользователь не зарегестриован
        return 2  # if the user wasn't added

