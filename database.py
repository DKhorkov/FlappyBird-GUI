import sqlite3
import hashlib
import pickle


class DataBase:

    def __init__(self):
        self._user_id = None
        self._difficulty_id = None
        self._resolution_id = None
        self._main_id = None
        self._record_id = None
        self._config_id = None
        self.__open_connection()

    def __open_connection(self):
        self.__connection = sqlite3.connect("FlappyBirdDatabase.db", check_same_thread=False)
        self.__cursor = self.__connection.cursor()
        self.__create_tables_if_not_exists()

    def close_connection(self):
        self.__cursor.close()
        self.__connection.close()

    def __create_tables_if_not_exists(self):
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY, 
        username TEXT NOT NULL, hashed_password INTEGER NOT NULL)''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS difficulty (id INTEGER NOT NULL PRIMARY KEY, 
        difficulty_level TEXT NOT NULL)''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS screen_resolution (id INTEGER NOT NULL PRIMARY KEY, 
        resolution TEXT NOT NULL)''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS main (id INTEGER NOT NULL PRIMARY KEY, 
        user_id INTEGER NOT NULL, difficulty_id INTEGER NOT NULL, screen_resolution_id INTEGER NOT NULL, 
        lives INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id), 
        FOREIGN KEY (difficulty_id) REFERENCES difficulty (id), 
        FOREIGN KEY (screen_resolution_id) REFERENCES screen_resolution (id) )''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS records (id INTEGER NOT NULL PRIMARY KEY, 
        main_id INTEGER NOT NULL, record INTEGER NOT NULL, FOREIGN KEY (main_id) REFERENCES main (id) )''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS last_configs (id INTEGER NOT NULL PRIMARY KEY, 
        user_id INTEGER NOT NULL, configs BLOB NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id) )''')

    def check_user_existence(self, username, password):
        self.__cursor.execute('''SELECT EXISTS (SELECT id FROM users WHERE username=?)''',
                              (username,))
        exist = bool(self.__cursor.fetchone()[0])
        if exist:
            self.__cursor.execute('''SELECT id, hashed_password FROM users WHERE username=?''',
                                  (username,))
            user_id, hashed_password = self.__cursor.fetchone()
            if password == hashed_password:
                self._user_id = user_id
                return True, True
            else:
                return True, False
        else:
            return False, False  # Второй False, чтобы всегда возвращался кортеж и не было ошибок индекса

    def upload_users(self, username, password):
        self.__cursor.execute('''INSERT INTO users (username, hashed_password) VALUES (?, ?) RETURNING id''',
                              (username, password))
        self._user_id = self.__cursor.fetchone()[0]
        self.__connection.commit()

    def upload_difficulty(self, difficulty_level):
        self.__cursor.execute('''SELECT EXISTS (SELECT id FROM difficulty WHERE difficulty_level=?)''',
                              (difficulty_level, ))
        exist = bool(self.__cursor.fetchone()[0])
        if not exist:
            self.__cursor.execute('''INSERT INTO difficulty (difficulty_level) VALUES (?) RETURNING id''',
                                  (difficulty_level, ))
            self._difficulty_id = self.__cursor.fetchone()[0]
            self.__connection.commit()
        else:
            self.__cursor.execute('''SELECT id FROM difficulty WHERE difficulty_level=?''',
                                  (difficulty_level, ))
            self._difficulty_id = self.__cursor.fetchone()[0]

    def upload_screen_resolution(self, screen_resolution):
        self.__cursor.execute('''SELECT EXISTS (SELECT id FROM screen_resolution WHERE resolution=?)''',
                              (screen_resolution,))
        exist = bool(self.__cursor.fetchone()[0])
        if not exist:
            self.__cursor.execute('''INSERT INTO screen_resolution (resolution) VALUES (?) RETURNING id''',
                                  (screen_resolution,))
            self._resolution_id = self.__cursor.fetchone()[0]
            self.__connection.commit()
        else:
            self.__cursor.execute('''SELECT id FROM screen_resolution WHERE resolution=?''',
                                  (screen_resolution,))
            self._resolution_id = self.__cursor.fetchone()[0]

    def upload_main(self, lives):
        self.__cursor.execute('''SELECT EXISTS (SELECT id FROM main WHERE user_id=? AND difficulty_id=? AND 
        screen_resolution_id=? AND lives=?)''', (self._user_id, self._difficulty_id, self._resolution_id, lives))
        exist = bool(self.__cursor.fetchone()[0])
        if not exist:
            self.__cursor.execute('''INSERT INTO main (user_id, difficulty_id, screen_resolution_id, lives) 
            VALUES (?, ?, ?, ?) RETURNING id''', (self._user_id, self._difficulty_id, self._resolution_id, lives))
            self._main_id = self.__cursor.fetchone()[0]
            self.__connection.commit()
        else:
            self.__cursor.execute('''SELECT id FROM main WHERE user_id=? AND difficulty_id=? AND 
            screen_resolution_id=? AND lives=?''', (self._user_id, self._difficulty_id, self._resolution_id, lives))
            self._main_id = self.__cursor.fetchone()[0]

    def check_record_existence(self):
        self.__cursor.execute('''SELECT EXISTS (SELECT id FROM records WHERE main_id=?)''',
                              (self._main_id,))
        exist = bool(self.__cursor.fetchone()[0])
        if exist:
            self.__cursor.execute('''SELECT record FROM records WHERE main_id=?''',
                                  (self._main_id,))
            record = self.__cursor.fetchone()[0]
            return record
        else:
            return 0

    def upload_record(self, record):
        self.__cursor.execute('''SELECT EXISTS (SELECT id FROM records WHERE main_id=?)''',
                              (self._main_id,))
        exist = bool(self.__cursor.fetchone()[0])
        if not exist:
            self.__cursor.execute('''INSERT INTO records (main_id, record) VALUES (?, ?)''',
                                  (self._main_id, record))
            self.__connection.commit()
        else:
            self.__cursor.execute('''UPDATE records SET record=? WHERE main_id=?''',
                                  (record, self._main_id))
            self.__connection.commit()

    def check_configs_existence(self):
        self.__cursor.execute('''SELECT EXISTS (SELECT id FROM last_configs WHERE user_id=?)''',
                              (self._user_id,))
        exist = bool(self.__cursor.fetchone()[0])
        if exist:
            self.__cursor.execute('''SELECT configs FROM last_configs WHERE user_id=?''',
                                  (self._user_id,))
            configs = self.__cursor.fetchone()[0]
            return True, configs
        else:
            return False, False  # Второй False, чтобы всегда возвращался кортеж и не было ошибок индекса

    def upload_last_config(self, configs):
        self.__cursor.execute('''SELECT EXISTS (SELECT id FROM last_configs WHERE user_id=?)''',
                              (self._user_id,))
        exist = bool(self.__cursor.fetchone()[0])
        if not exist:
            self.__cursor.execute('''INSERT INTO last_configs (user_id, configs) VALUES (?, ?)''',
                                  (self._user_id, configs))
            self.__connection.commit()
        else:
            self.__cursor.execute('''UPDATE last_configs SET configs=? WHERE user_id=?''',
                                  (configs, self._user_id))
            self.__connection.commit()
