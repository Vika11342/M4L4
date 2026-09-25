import sqlite3
from config import DATABASE

predmet = [(_,) for _ in (["Информатика", "Физика", "История"])]

class DB_Manager:
    def __init__(self, database):
        self.database = database  # имя базы данных

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE predmet (
            id INTEGER PRIMARY KEY,
            predmet TEXT
            )''') 
            conn.execute('''CREATE TABLE tema(
            tema_id INTEGER PRIMARY KEY,
            tema TEXT,
            FOREIGN KEY(predmet_id) REFERENCES predmet(id)
            )''')
            conn.commit()

    def __executemany(self, sql, data):
            conn = sqlite3.connect(self.database)
            with conn:
                conn.executemany(sql, data)
                conn.commit()
        
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    def default_insert(self):
            sql = 'INSERT OR IGNORE INTO predmet(predmet) values(?)'
            data = predmet
            self.__executemany(sql, data)

    def insert_tema(self, data):
            sql = """INSERT INTO tema (tema, predmet_id) 
            values(?,?)""" # Запиши сюда правильный SQL запрос
            self.__executemany(sql, data)

    def get_predmet(self):
            sql = "SELECT predmet from predmet"  # Запиши сюда правильный SQL запрос
            return self.__select_data(sql)

    def get_tema(self):
            sql = "SELECT tema from tema"  # Запиши сюда правильный SQL запрос
            return self.__select_data(sql)

    def get_predmet_id(self, predmet_name):
            sql = 'SELECT id FROM predmet WHERE predmet = ?'
            res = self.__select_data(sql, (predmet_name,))
            if res: return res[0][0]
            else: return None

    def delete_tema(self, tema_id):
            sql = """DELETE FROM tema 
    WHERE tema_id = ? """ # Запиши сюда правильный SQL запрос
            self.__executemany(sql, [(tema_id,)])

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()