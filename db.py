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
                self.cursor.execute('SELECT count FROM Voices WHERE username = ?', [username])
                count = self.cursor.fetchone()[0]
                self.cursor.execute('UPDATE Voices SET count = ? WHERE username = ?', [count + 1, username])

    def get_voices(self, all_voices=None):
        with self.connection:
            if all_voices is None:
                self.cursor.execute('SELECT * FROM Voices')
                return self.cursor.fetchall()
            else:
                self.cursor.execute('SELECT count FROM Voices WHERE username = ?', [all_voices])
                return self.cursor.fetchone()
