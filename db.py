import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # проверка есть ли пользователь в db
    def user_is(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    # добавление пользователя
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

    # изменение активности
    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET 'active' = ? WHERE 'user_id' = ?", (active, user_id,))

    # получение всех юзеров
    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, active FROM 'users'").fetchall()


    def add_fsm_message(self, photo, name, description):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'fsm_message' ('photo', 'name', 'description') VALUES (?, ?, ?)", (photo, name, description,))



