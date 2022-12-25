import sqlite3
import hashlib


class DataBase:

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self.__open_connection()

    def __open_connection(self):
        self.__connection = sqlite3.connect("FlappyBirdDatabase.db", check_same_thread=False)
        self.__cursor = self.__connection.cursor()
        self.__create_tables_if_not_exists()

    def _close_connection(self):
        self.__cursor.close()
        self.__connection.close()

    def __create_tables_if_not_exists(self):
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY, username TEXT, 
        hashed_password INTEGER)''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS difficulty (id INTEGER NOT NULL PRIMARY KEY, 
        difficulty TEXT)''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS screen_resolution (id INTEGER NOT NULL PRIMARY KEY, 
        screen_resolution TEXT)''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS main (id INTEGER NOT NULL PRIMARY KEY, 
        user_id INTEGER, difficulty_id INTEGER, screen_resolution_id INTEGER, lives INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id), FOREIGN KEY (difficulty_id) REFERENCES difficulty (id), 
        FOREIGN KEY (screen_resolution_id) REFERENCES screen_resolution (id) )''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS records (id INTEGER NOT NULL PRIMARY KEY, 
        main_id INTEGER, FOREIGN KEY (main_id) REFERENCES main (id) )''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS last_configs (id INTEGER NOT NULL PRIMARY KEY, 
        user_id INTEGER, configs TEXT, FOREIGN KEY (user_id) REFERENCES users (id) )''')

    def _upload_users(self):
        self.__cursor.execute('''SELECT EXISTS (SELECT id FROM users WHERE username=? and hashed_password=?)''',
                                      (self._username, self._password))
        exist = bool(self.__cursor.fetchone()[0])
        if not exist:
            self.__cursor.execute('''INSERT INTO users (username, hashed_password) VALUES (?, ?)''',
                                  (self._username, self._password))
            self.__connection.commit()

    def _main(self):
        self.__open_connection()


if __name__ == '__main__':
    u = 'demos'
    p = hashlib.sha1(b'{u}')
    p_o = p.hexdigest()
    p2 = hashlib.sha1(b'{u}')
    p_o2 = p.hexdigest()
    p3 = hashlib.sha1(b'{u}')
    p_o3 = p.hexdigest()
    p4 = hashlib.sha1(b'{u}')
    p_o4 = p.hexdigest()
    db = DataBase(u, p_o)
    db._upload_users()


