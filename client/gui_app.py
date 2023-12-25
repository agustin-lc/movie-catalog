import customtkinter
from PIL import Image
from tkinter import ttk, messagebox
import tkinter as tk
from model.movie_dao import create_table, delete_table
from model.movie_dao import Movie, save, list_movies, edit_movie, remove_movie

def show_about():
    info = '     Agustín\n♥   ♡   ♥   ♡   ♥'
    messagebox.showinfo('About', info)

def create_menu(root):
    menu_bar = tk.Menu(root) 
    root.config(menu=menu_bar)
    menu_bar.config(font=('Arial', 10))
    
    start_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='Start', menu=start_menu)
    start_menu.config(font=('Arial', 10))
    
    start_menu.add_command(label='Create DB', command=create_table)
    start_menu.add_command(label='Delete DB', command=delete_table)
    start_menu.add_command(label='Exit', command=root.destroy)
    
    about_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='Help', menu=about_menu)

    about_menu.add_command(label='About', command=show_about)
    about_menu.config(font=('Arial', 10))
    
class Frame(customtkinter.CTkFrame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.configure(fg_color='#1D1C1C', border_color='#FFCC70', border_width=2)
        self.pack()
        self.id_movie = None
        self.movie_fields()
        self.movie_table()

    def movie_fields(self):
        self.entry_fields = [] 

        fields = [
            ('Title: ', 'Title'),
            ('Director: ', 'Director'),
            ('Year: ', 'Year'),
            ('Rating: ', 'Rating'),
            ('Genre: ', 'Genre'),
            ('Country: ', 'Country')
        ]

        for i, (label_text, entry_placeholder) in enumerate(fields):
            label = customtkinter.CTkLabel(self, text=label_text, fg_color='transparent')
            label.grid(row=i, column=0, padx=3, pady=3)
            
            entry = customtkinter.CTkEntry(self, placeholder_text=entry_placeholder)
            entry.grid(row=i, column=1, padx=3, pady=3)
            entry.configure(state='disabled')
            self.entry_fields.append(entry)

        self.new_button = self.create_button('New', 'img/new.png', row=7, column=0, command=self.enable_buttons)
        self.new_button.configure(fg_color='#204021', hover_color='#308241')
        self.save_button = self.create_button('Save', 'img/save.png', row=7, column=1, state='disabled', command=self.save_data)
        self.cancel_button = self.create_button('Cancel', 'img/cancel.png', row=7, column=2, state='disabled', command=self.disable_buttons)

        # Remove cursor from entries
        self.focus_widget = customtkinter.CTkLabel(self, text='')
        self.focus_widget.grid(row=8, column=0)

    def create_button(self, text, image_path, row, column, command=None, state='normal'):
        img = Image.open(image_path)

        if text != 'New':
            entry = customtkinter.CTkEntry(self, placeholder_text=text)
            entry.grid(row=row, column=column, padx=3, pady=3)
            entry.configure(state='disabled')
            self.entry_fields.append(entry)

        button = customtkinter.CTkButton(self, text=text, command=command, state=state)
        button.grid(row=row, column=column, padx=3, pady=3)
        button.configure(corner_radius=15, fg_color='#454647', hover_color='#181919', image=customtkinter.CTkImage(light_image=img))

        return button

    def enable_buttons(self):
        self.save_button.configure(state='normal')
        self.cancel_button.configure(state='normal')

        # Clear entries
        for entry in self.entry_fields:
            entry.configure(state='normal')

    def disable_buttons(self):
        self.id_movie = None

        self.save_button.configure(state='disabled')
        self.cancel_button.configure(state='disabled')

        # Clear entries and set placeholders
        for entry, placeholder_text in zip(self.entry_fields, ['Title', 'Director', 'Year', 'Rating', 'Genre', 'Country']):
            if entry.get() == "":
                entry.insert(0, placeholder_text)
            else:
                entry.delete(0, 'end')

        # Remove cursor from entries
        self.focus_widget.focus_set()

    def save_data(self):
        # Insert movies
        title = self.entry_fields[0].get()
        director = self.entry_fields[1].get()
        year = self.entry_fields[2].get()
        rating = self.entry_fields[3].get()
        genre = self.entry_fields[4].get()
        country = self.entry_fields[5].get()

        movie = Movie(title, director, year, rating, genre, country)
        if self.id_movie is None:
            save(movie)
        else:
            edit_movie(movie, self.id_movie)

        # update table after inserting movie
        self.movie_table()

        self.disable_buttons()
        self.focus_widget.focus_set()

    def movie_table(self):
        self.movie_list = list_movies()
        self.movie_list.reverse()

        edit_img = Image.open('img/edit.png')
        remove_img = Image.open('img/remove.png')
        self.table = ttk.Treeview(self, column = ('Name', 'Director', 'Year', 'Rating', 'Genre', 'Country'))
        self.table.grid(row=0, column=2, rowspan=6, columnspan=4, sticky='nse')

        # Scrollbar
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.table.yview)
        self.scroll.grid(row=0, column=6, rowspan=6, sticky='nsw')
        self.table.configure(yscrollcommand=self.scroll.set)

        self.table.heading('#0', text='ID')
        self.table.heading('#1', text='Name')
        self.table.heading('#2', text='Director')
        self.table.heading('#3', text='Year')
        self.table.heading('#4', text='Rating')
        self.table.heading('#5', text='Genre')
        self.table.heading('#6', text='Country')

        self.table.column('#0', width=50)
        self.table.column('#1', width=150, anchor='center')
        self.table.column('#2', width=130, anchor='center')
        self.table.column('#3', width=50, anchor='center')
        self.table.column('#4', width=50, anchor='center')
        self.table.column('#5', width=100, anchor='center')
        self.table.column('#6', width=110, anchor='center')

        edit_button = customtkinter.CTkButton(self, text='Edit', command=self.edit_data)
        edit_button.grid(row=7, column=3, padx=3, pady=3)
        edit_button.configure(corner_radius=15, fg_color='#454647', hover_color='#181919', image=customtkinter.CTkImage(light_image=edit_img))
        
        remove_button = customtkinter.CTkButton(self, text='Remove', command=self.remove_data)
        remove_button.grid(row=7, column=4, padx=3, pady=3)
        remove_button.configure(corner_radius=15, fg_color='#b93e06', hover_color='#e1652e', image=customtkinter.CTkImage(light_image=remove_img))

        # Add movie to list
        for m in self.movie_list:
            self.table.insert('',0, text=m[0], values = (m[1], m[2], m[3], m[4], m[5], m[6]))


    def edit_data(self):

        try:
            # Gets the selected values ​​of the row in the table
            self.id_movie = self.table.item(self.table.selection())['text']
            self.title_movie = self.table.item(self.table.selection())['values'][0]
            self.director_movie = self.table.item(self.table.selection())['values'][1]
            self.year_movie = self.table.item(self.table.selection())['values'][2]
            self.rating_movie = self.table.item(self.table.selection())['values'][3]
            self.genre_movie = self.table.item(self.table.selection())['values'][4]
            self.country_movie = self.table.item(self.table.selection())['values'][5]

            # Enable buttons
            self.enable_buttons()

            # Updates the Entry with the selected values
            values_to_set = [self.title_movie, self.director_movie, self.year_movie, self.rating_movie, self.genre_movie, self.country_movie]

            for entry, value in zip(self.entry_fields, values_to_set):
                entry.delete(0, 'end')
                entry.insert(0, value)
        except:
            title = 'Data editing'
            message = 'You have not selected any record.'
            messagebox.showerror(title, message)

    def remove_data(self):
        try:
            self.id_movie = self.table.item(self.table.selection())['text']
            remove_movie(self.id_movie)

            # update table after inserting movie
            self.movie_table()
            self.id_movie = None
        except:
            title = 'Delete record'
            message = 'Could not delete record.'
            messagebox.showerror(title, message)
