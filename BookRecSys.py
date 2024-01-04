from Recommender import Recommender
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import requests
from io import BytesIO

# working app

root = tk.Tk()
root.title('Book RecSys')

recommender = Recommender() # recommender logic

def submit():
    """
    display book recommendations for 
    book_title on submit
    """
    recs = recommender.recommend(book_title.get())
    createRecsDisplay(recs)

# top portion of content
# search function is bound to container frame
container = ttk.Frame(root)
container.grid(row = 0, column = 0)

book_title = tk.StringVar() # book title input variable

lab1 = ttk.Label(container, text = "Book Title") # input box label
lab1.grid(row = 0, column = 0)

entry = ttk.Entry(container, textvariable = book_title) # entry box
entry.grid(row = 0, column = 1) #.focus_set()

btn = ttk.Button(container, text = 'Get Recs', command = submit) # submit button
btn.grid(row = 0, column = 2)

# main content area
# content (popular/recs) are bound to content frame
content = ttk.Frame(root)
content.grid(row = 1, column = 0)

def getImage(url):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'})
    response = session.get(url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    return img


def createBookFrame(parent,rec):
    # create frame
    container = ttk.Frame(parent)
    # title label
    title = rec[0]
    ttk.Label(container, text = title).grid(row = 0, column = 0)
    # author label
    author = rec[1]
    ttk.Label(container, text = author).grid(row = 1, column = 0)
    # get image
    img_URL = rec[2]
    img = getImage(img_URL)
    # add book image
    cover = ttk.Label(container, image = img)
    cover.image = img
    cover.configure(image = img)
    cover.grid(row = 2, column = 0)
    return container

def createPopularDisplay():
    test = ttk.Label(content, text = "Popular")
    test.grid(row = 0, column = 0)
    pop = recommender.getPopular()
    most_pop = createBookFrame(content,pop[0])
    most_pop.grid(row = 1, column = 0)
    others = ttk.Frame(content)
    others.grid(row = 2, column = 0)
    idx = 1
    for i in range(3):
        for j in range(3):
            book = createBookFrame(others,pop[idx])
            book.grid(row = i, column = j)
            idx += 1

createPopularDisplay() 

def createRecsDisplay(recs):
    # highlight top recommendation
    top_book = createBookFrame(content, recs[0])
    top_book.grid(row = 0, column = 0)
    # next best
    other_books = ttk.Frame(content)
    other_books.grid(row = 1, column = 0)
    idx = 1
    for i in range(3):
        for j in range(3):
            book = createBookFrame(other_books,recs[idx])
            book.grid(row = i, column = j)
            idx += 1

root.mainloop()