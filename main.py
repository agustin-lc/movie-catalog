import customtkinter
import tkinter as tk
from client.gui_app import Frame, create_menu

def main():
    app = customtkinter.CTk()
    app.title('Movie Catalog')
    customtkinter.set_appearance_mode("dark")
    create_menu(app)

    app.resizable(0,0)  
    frame_app = Frame(root=app)
    
    app.mainloop()

if __name__ == '__main__':
    main()