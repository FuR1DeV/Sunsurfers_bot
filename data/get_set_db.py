import logging
from data.create_db import Database


class GlobalGetDB(Database):
    logger = logging.getLogger("bot.data.global_get_db")

    def all_users(self):
        self.logger.info('Функция выгрузки всех пользователей')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users"
            )
            return cursor.fetchall()


class UserGetDB(Database):
    logger = logging.getLogger("bot.data.user_get_db")

    def user_exists(self, user_id: int):
        self.logger.info('Пользователь проверяет себя на наличие в БД')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE user_id = %(user_id)s;", {
                    'user_id': user_id,
                }
            )
            return cursor.fetchone()

    def user_ban(self, user_id):
        self.logger.info('Пользователь проверяет себя на БАН')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT ban FROM users WHERE user_id = %(user_id)s", {
                    'user_id': user_id,
                }
            )
            return cursor.fetchone()


class UserSetDB(Database):
    logger = logging.getLogger("bot.data.user_set_db")

    def user_add(self, user_id, username, telephone, first_name, last_name):
        self.logger.info('Заказчик добавляет себя в БД')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (user_id, username, telephone, first_name, last_name) "
                "VALUES (%(user_id)s, %(username)s, %(telephone)s, %(first_name)s, %(last_name)s);", {
                    'user_id': user_id,
                    'username': username,
                    'telephone': telephone,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            self.connection.commit()


global_get_db_obj = GlobalGetDB()
user_get_db_obj = UserGetDB()
user_set_db_obj = UserSetDB()
