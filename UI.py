# Code by Luann Pascucci
# initially starting out by following https://tkdocs.com/tutorial/intro.html
# and then modifying as needed

# This is part of a project for CS361 at Oregon State University.

from tkinter import *
from tkinter import ttk

# UI introduction explanation
with open('ui_intro_message.txt', 'r') as intro_message:
    intro_text = intro_message.read()


root = Tk()

# title of software/main application window
root.title("Baking Ingredients Converter")

# setting up layout/content frame of interface
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# text labels
ttk.Label(mainframe, text=intro_text).grid(column=2, row=1, sticky=S)

ttk.Button(root, text="Hello World").grid()

root.mainloop()
