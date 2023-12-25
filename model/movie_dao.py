from .connection_db import ConnectionDB
from tkinter import messagebox

title_create = 'Create record'
title_delete = 'Delete record'
title_connection = 'Connection'

def create_table():
    connection = ConnectionDB()

    sql = '''
    CREATE TABLE movies(
        id_movie INTEGER,
        title VARCHAR(100),
        director VARCHAR(100),
        year INTEGER,
        rating VARCHAR(10),
        genre VARCHAR(100),
        country VARCHAR(30),
        PRIMARY KEY(id_movie AUTOINCREMENT)
    )
    '''

    try:
        connection.cursor.execute(sql)
        connection.close()
        message = 'The table was created successfully.'
        messagebox.showinfo(title_create, message)
    except:
        message = 'The table is already created.'
        messagebox.showwarning(title_create, message)

def delete_table():
    connection = ConnectionDB()

    sql = 'DROP TABLE movies'

    try:
        connection.cursor.execute(sql)
        connection.close()
        message = 'The table was deleted successfully.'
        messagebox.showinfo(title_delete, message)
    except:
        message = 'There is no table to delete.'
        messagebox.showwarning(title_delete, message)

class Movie:
    def __init__(self, title, director, year, rating, genre, country):
        self.id_movie = None
        self.title = title
        self.director = director
        self.year = year
        self.rating = rating
        self.genre = genre
        self.country = country

    def __str__(self):
        return f'Movie[{self.title}, {self.director}, {self.year}, {self.rating}, {self.genre}, {self.country}]'

def save(movie):
    connection = ConnectionDB()

    sql = f"""INSERT INTO movies (title, director, year, rating, genre, country)
    VALUES('{movie.title}', '{movie.director}', '{movie.year}', '{movie.rating}', '{movie.genre}', '{movie.country}')"""

    try:
        connection.cursor.execute(sql)
        connection.close()
    except:
        message = 'The movie table is not created in the database.'
        messagebox.showerror(title_connection, message)

def list_movies():
    connection = ConnectionDB()

    movie_list = []
    sql = 'SELECT * FROM movies'

    try:
        connection.cursor.execute(sql)
        movie_list = connection.cursor.fetchall()
        connection.close()
    except:
        message = 'Create the table in the database.'
        messagebox.showwarning(title_connection, message)

    return movie_list

def edit_movie(movie, id_movie):
    connection = ConnectionDB()

    # Update the movie in the database
    sql = f"""UPDATE movies
              SET title = '{movie.title}',
                  director = '{movie.director}',
                  year = {movie.year},
                  rating = '{movie.rating}',
                  genre = '{movie.genre}',
                  country = '{movie.country}'
              WHERE id_movie = {id_movie}"""

    try:
        connection.cursor.execute(sql)
        connection.close()
    except:
        message = 'Error updating movie.'
        messagebox.showerror(title_connection, message)

def remove_movie(id_movie):
    connection = ConnectionDB()

    sql = f'DELETE FROM movies WHERE id_movie = {id_movie}'

    try:
        connection.cursor.execute(sql)
        connection.close()
    except:
        message = 'Could not delete record.'
        messagebox.showerror(title_delete, message)
