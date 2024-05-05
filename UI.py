# Code by Luann Pascucci
# initially starting out by following https://tkdocs.com/tutorial/intro.html
# and then modifying as needed

# This is part of a project for CS361 at Oregon State University.

import tkinter as tk
# from tkinter import *
from tkinter import ttk
from dropdown_ingredients import dropdown_ingredients

# UI introduction explanation
with open('ui_intro_message.txt', 'r') as intro_message:
    intro_text = intro_message.read()
# Privacy information
with open('privacy_message.txt', 'r') as privacy_message:
    privacy_text = privacy_message.read()
# Ingredient selection instructions
with open('ingr_choose_instructions.txt', 'r') as ingr_choose:
    ingr_instructions = ingr_choose.read()

class BakingConversionApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.title("Baking Ingredients Converter")

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # text labels
        Intro_label = tk.Label(self, text=intro_text)
        copyright_label = tk.Label(self, text="Copyright: Luann Pascucci 2024")
        privacy_label = tk.Label(self, text=privacy_text)
        
        # buttons
        start_button = tk.Button(self, text="Start")
        close_button = tk.Button(self, text="Close Program")

        # layout
        Intro_label.grid(column=1, row=0)
        copyright_label.grid(column=1, row=4)
        privacy_label.grid(column=1, row=3)
        start_button.grid(column=1, row=1)
        close_button.grid(column=1, row=2)

class IngrChoose(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # text labels : instructions, list items: ("Ingredient:", "Convert From:")
        instructions = tk.Label(self, text=ingr_instructions)
        ingr_list_label = tk.Label(self, text="Ingredient:")
        convert_from_unit = tk.Label(self, text="Convert From:")
        
        # dropdown boxes: ingredient list and unit types

        # buttons: delete, add new ingredient, next, close
        delete_button = tk.Button(self, text="Delete")
        add_ingr_button = tk.Button(self, text="Add Ingredient")
        next_button = tk.Button(self, text="Next")
        close_button = tk.Button(self, text="Close Program")

        # layout
        instructions.grid(column=0, row=0)




root = BakingConversionApp()
root.mainloop()


# input practice
#e = Entry(Toplevel, width=25)

# functionalities
def start():
    ingred_select = Toplevel()
    ingred_select.title("Baking Ingredients Converter: Select Ingredients")
    clicked = StringVar()
    drop = OptionMenu(Toplevel, clicked, *dropdown_ingredients).pack()

# title of software/main application window
#root.title("Baking Ingredients Converter")
#root.geometry("300x300")

# # setting up layout/content frame of interface
# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# text labels
#Intro_label = Label(mainframe, text=intro_text).grid(column=1, row=1, sticky=W)
#copyright_label = Label(mainframe, text="Copyright: Luann Pascucci 2024").grid(column=2, row=4, sticky=W)

# interactive buttons
#start_button = Button(root, text="Start", command=start).grid(column=3, row=2)
#close_button = Button(root, text="Close", command=root.quit).grid(column=3, row=3)
