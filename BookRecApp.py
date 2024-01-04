from Recommender import Recommender
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import requests
from io import BytesIO

class BookRecApp(tk.Tk):

    recommender = Recommender()

    def __init__(self):
        tk.Tk.__init__(self)
        self.book_title = tk.StringVar() 
        self.configureRoot()
        self.configurePrompt()


    def configureRoot(self):
        # window title
        self.title('Book Recommender')
        # window geometry
        window_width = 700
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def configurePrompt(self):
        container = ttk.Frame(self)
        label = ttk.Label(container, text = "Book Title")
        entry = ttk.Entry(container, textvariable = self.book_title)
        entry.focus_set()
        btn = ttk.Button(container, text = "Get Recs")
        container.grid(row = 0, column = 0)
        label.grid(row = 0, column = 0)
        entry.grid(row = 0, column = 1)
        btn.grid(row = 0, column = 2)

class PopularFrame():

    def __init__(self):
        pass

class RecsFrame():

    def __init__(self):
        pass



def main():
    app = BookRecApp()
    app.mainloop()

if __name__ == "__main__":
    main()