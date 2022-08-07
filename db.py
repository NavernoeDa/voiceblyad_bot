import sqlite3


class DataBase:
    def __init__(self, file_db='DataBase.db'):
        self.connection = sqlite3.connect(file_db)
        self.cursor = self.connection.cursor()

    def add_voice(self, username):
        with self.connection:
            self.cursor.execute('SELECT username FROM Voices WHERE username = ?', [username])
            if self.cursor.fetchone() is None:
                self.cursor.execute('INSERT INTO Voices(username, count) VALUES(?, ?)', [username, 1])
            else:
                self.update_count(username)

    def update_count(self, username):
        self.cursor.execute('SELECT count FROM Voices WHERE username = ?', [username])
        count = self.cursor.fetchone()[0]
        self.cursor.execute('UPDATE Voices SET count = ? WHERE username = ?', [count + 1, username])

    def get_voices(self, id_=None):
        with self.connection:
            if id_ is None:
                self.cursor.execute('SELECT * FROM Voices')
                return self.cursor.fetchall()
            else:
                self.cursor.execute('SELECT count FROM Voices WHERE username = ?', [id_])
                return self.cursor.fetchone()
