# Файл для работы с базой данных

import pymysql
import cryptography
import time


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

def insert():
    """Добавляет пользователя в базу данных"""
    pass


def check_user():
    '''Проверяем пользователя на оплату'''
     pass


def change_status():
    """Меняем статус пользователя"""
    pass
