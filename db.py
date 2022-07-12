import sqlite3
import time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    #_____________users_____________#

    # проверка есть ли пользователь в db(users)
    def user_is(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    # добавление пользователя users
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

     # получение всех юзеров, которые писали боту
    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, active FROM 'users'").fetchall()



    #____________users_chat____________#

    # проверка есть ли пользователь в db(users_chat)
    def user_chat_is(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users_chat' WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    # добавление пользователя users_chat
    def add_user_chat(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users_chat' ('user_id') VALUES (?)", (user_id,))

    # проверка наличия мута
    def mute_is(self, user_id):
        with self.connection:
            user = self.cursor.execute("SELECT * FROM 'users_chat' WHERE user_id = ?", (user_id,)).fetchone()
            return int(user[2]) >= time.time()

    # добавление мута
    def add_mute(self, user_id, mute):
        with self.connection:
            return self.cursor.execute("UPDATE 'users_chat' SET 'mute' = ? WHERE 'user_id' = ?", (int(time.time()) + int(mute), user_id,))

    #____________other___________#

    # изменение активности
    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET 'active' = ? WHERE 'user_id' = ?", (active, user_id,))


    def add_fsm_message(self, photo, name, description):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'fsm_message' ('photo', 'name', 'description') VALUES (?, ?, ?)",
                                       (photo, name, description,))
