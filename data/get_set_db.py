import logging
from data.create_db import Database


class GlobalGetDB(Database):
    logger = logging.getLogger("bot.data.global_get_db")

    def all_users(self):
        self.logger.info('The function of unloading all users')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users"
            )
            return cursor.fetchall()

    def all_users_in_country(self, country):
        self.logger.info(f'The function of unloading all users in {country}')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE country = %(country)s;", {
                    'country': country,
                }
            )
            return cursor.fetchall()

    def check_user_sun_gathering(self, user_id, country):
        self.logger.info(f'The function checks if there was a person at this gathering')
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM sun_gathering_{country} "
                f"WHERE user_id = %(user_id)s;", {
                    'country': country,
                    'user_id': user_id,
                }
            )
            return cursor.fetchone()


class UserGetDB(Database):
    logger = logging.getLogger("bot.data.user_get_db")

    def user_exists(self, user_id: int):
        self.logger.info('The user checks himself for existence in the database')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE user_id = %(user_id)s;", {
                    'user_id': user_id,
                }
            )
            return cursor.fetchone()

    def user_ban(self, user_id):
        self.logger.info('User checks himself for BAN')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT ban FROM users WHERE user_id = %(user_id)s", {
                    'user_id': user_id,
                }
            )
            return cursor.fetchone()

    def user_about(self, user_id):
        self.logger.info('User uploads information about himself')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT about FROM users WHERE user_id = %(user_id)s;", {
                    'user_id': user_id,
                }
            )
            return cursor.fetchone()

    def user_get_info_username(self, user_id, username):
        self.logger.info(f'User {user_id} views user information')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username = %(username)s;", {
                    'username': username,
                }
            )
            return cursor.fetchone()

    def user_get_info_country(self, user_id, country):
        self.logger.info(f'User checks info about sun gathering in country')
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM sun_gathering_{country} "
                f"WHERE user_id = %(user_id)s;", {
                    'user_id': user_id,
                }
            )
            return cursor.fetchone()


class UserSetDB(Database):
    logger = logging.getLogger("bot.data.user_set_db")

    def user_add(self, user_id, username, first_name, last_name):
        self.logger.info('The customer adds himself to the database')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (user_id, username, first_name, last_name) "
                "VALUES (%(user_id)s, %(username)s, %(first_name)s, %(last_name)s);", {
                    'user_id': user_id,
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            self.connection.commit()

    def user_set_geo(self, user_id, country, state, province, city, town, address, latitude, longitude, updated_location):
        self.logger.info(f'The user updates his geo data')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET country = %(country)s, state = %(state)s, province = %(province)s, city = %(city)s, "
                "town = %(town)s, address = %(address)s, latitude = %(latitude)s, longitude = %(longitude)s, "
                "updated_location = %(updated_location)s WHERE user_id = %(user_id)s;", {
                    'user_id': user_id,
                    'country': country,
                    'state': state,
                    'province': province,
                    'city': city,
                    'town': town,
                    'address': address,
                    'latitude': latitude,
                    'longitude': longitude,
                    'updated_location': updated_location,
                }
            )
            self.connection.commit()

    def user_set_about_me(self, user_id, about):
        self.logger.info(f'The user updates his geo data')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET about = %(about)s "
                "WHERE user_id = %(user_id)s;", {
                    'user_id': user_id,
                    'about': about,
                }
            )
            self.connection.commit()

    def user_set_sun_gathering(self, user_id, username, first_name, last_name, sun_gathering):
        self.logger.info(f'The user set sun gathering')
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO sun_gathering_{sun_gathering} (user_id, username, first_name, last_name) "
                "VALUES (%(user_id)s, %(username)s, %(first_name)s, %(last_name)s);", {
                    'user_id': user_id,
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'sun_gathering': sun_gathering,
                }
            )
            self.connection.commit()

    def user_set_sun_gathering_about(self, user_id, country, about):
        self.logger.info(f'The user updates about SunGathering {country}')
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE sun_gathering_{country} SET about_sun_gathering = %(about)s "
                "WHERE user_id = %(user_id)s;", {
                    'user_id': user_id,
                    'about': about,
                }
            )
            self.connection.commit()

    def user_set_first_name(self, user_id, first_name):
        self.logger.info(f'The user updates his geo data')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET first_name = %(first_name)s "
                "WHERE user_id = %(user_id)s;", {
                    'user_id': user_id,
                    'first_name': first_name,
                }
            )
            self.connection.commit()

    def user_set_last_name(self, user_id, last_name):
        self.logger.info(f'The user updates his geo data')
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET last_name = %(last_name)s "
                "WHERE user_id = %(user_id)s;", {
                    'user_id': user_id,
                    'last_name': last_name,
                }
            )
            self.connection.commit()


global_get_db_obj = GlobalGetDB()
user_get_db_obj = UserGetDB()
user_set_db_obj = UserSetDB()
