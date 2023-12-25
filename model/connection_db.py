import sqlite3

class ConnectionDB:
    def __init__(self):
        self.database = 'database/movie.db'
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.commit()
        self.connection.close()