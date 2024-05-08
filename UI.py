# Code by Luann Pascucci
# initially starting out by following https://tkdocs.com/tutorial/intro.html
# and then modifying as needed

# This is part of a project for CS361 at Oregon State University.

import tkinter as tk
# from tkinter import *
from tkinter import ttk
import json


from dropdown_ingredients import dropdown_ingredients
from unit_types import unit_types

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

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, IngrChoose, InputMeasurements):

            frame = F(container, self)

            self.frames[F] = frame

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
        start_button = tk.Button(self, text="Start", command=lambda: controller.show_frame(IngrChoose))
        close_button = tk.Button(self, text="Close Program")

        # layout
        Intro_label.grid(column=1, row=0, columnspan=5)
        copyright_label.grid(column=1, row=4)
        privacy_label.grid(column=1, row=3)
        start_button.grid(column=1, row=1)
        close_button.grid(column=1, row=2)


class IngrChoose(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.input_frame = tk.LabelFrame(self, text="Add Ingredient to List")
        self.button_frame = tk.LabelFrame(self)
        self.list_to_convert = ttk.Treeview(self, columns=(1, 2, 3), show="headings")

        self.ingredients_and_units = []

        # text labels : instructions, list items: ("Ingredient:", "Convert From:")
        self.instructions = tk.Label(self, text=ingr_instructions)
        self.ingr_list_label = tk.Label(self.input_frame, text="Ingredient:")
        self.convert_from_label = tk.Label(self.input_frame, text="Convert From:")
        self.amount_to_convert_label = tk.Label(self.input_frame, text="Amount to convert:")
        self.list_to_convert.heading(1, text="Ingredient")
        self.list_to_convert.heading(2, text="Convert From")
        self.list_to_convert.heading(3, text="Amount to convert")
        self.list_to_convert.column("1", stretch=True)
        self.list_to_convert.column("2", stretch=False)
        self.list_to_convert.column("3", stretch=False)

        # dropdown & input boxes: ingredient list and unit types
        self.ingr_default = "Choose Ingredient"
        self.ingr_chosen = tk.StringVar(value=self.ingr_default)
        self.ingr_drop = tk.OptionMenu(self.input_frame, self.ingr_chosen,
                                       *dropdown_ingredients)
        self.unit_default = "Choose Unit"
        self.unit_chosen = tk.StringVar(value=self.unit_default)
        self.unit_drop = tk.OptionMenu(self.input_frame, self.unit_chosen,
                                       *unit_types)
        self.amount_default = "0"
        self.amount_to_convert = tk.StringVar()
        self.amount_enter = tk.Entry(self.input_frame)

        # buttons: delete, add new ingredient, next, close
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_entry)
        self.add_ingr_button = tk.Button(self.button_frame, text="Add Ingredient", command=self.add_entry)
        self.next_button = tk.Button(self, text="Next", command=lambda: controller.show_frame(InputMeasurements))
        self.close_button = tk.Button(self, text="Close Program")

        # layout
        self.instructions.grid(column=0, row=0)
        self.input_frame.grid(row=1, column=0, rowspan=3, columnspan=5)
        self.button_frame.grid(column=0, row=4)
        self.list_to_convert.grid(column=0, row=7)

        self.ingr_list_label.grid(column=0, row=1)
        self.ingr_drop.grid(column=0, row=1)
        self.convert_from_label.grid(column=1, row=1)
        self.unit_drop.grid(column=2, row=1)
        self.amount_to_convert_label.grid(column=3, row=1)
        self.amount_enter.grid(column=4, row=1)

        self.delete_button.grid(column=4, row=1)
        self.add_ingr_button.grid()
        self.next_button.grid(column=3, row=3)
        self.close_button.grid(column=3, row=4)

    # methods
    # json stuff
    def load_json_from_file(self):
        with open("preconverted_info.json", "r") as file_handler:
            self.ingredients_and_units = json.load(file_handler)
        file_handler.close

    def save_json_to_file(self):
        with open("preconverted_info.json", "w") as file_handler:
            json.dump(self.ingredients_and_units, file_handler, indent=4)
        file_handler.close

    # treeview/list of ingredients window stuff
    def remove_all_from_list(self):
        for item in self.list_to_convert.get_children():
            self.list_to_convert.delete(item)

    def load_ingredients_window_with_json(self):
        self.remove_all_from_list()

        rowIndex = 1
        for item in self.ingredients_and_units:
            ingred = item["Ingredient"]
            unit = item["Unit"]
            amount = item["Amount"]
            self.list_to_convert.insert('', index="end", iid=rowIndex, text='', values=(ingred, unit, amount))
            rowIndex += 1

    def find_selected_row_in_list(self, id_num):
        row = 0
        found = False

        for list_item in self.list_to_convert.get_children():
            if list_item == id_num:
                found = True
                break
            row += 1
        if found is True:
            return row

        return -1

    # input field stuff
    def reset_all_fields(self):
        self.ingr_chosen.set(self.ingr_default)
        self.unit_chosen.set(self.unit_default)
        #self.amount_enter.delete()

    # button command stuff

    def add_entry(self):
        ingr_to_add = self.ingr_chosen.get()
        unit_to_add = self.unit_chosen.get()
        amount_to_add = float(self.amount_enter.get())
        if ingr_to_add == self.ingr_default or unit_to_add == self.unit_default or amount_to_add == 0:
            return
        else:
            temp_dict = {"Ingredient": ingr_to_add,
                         "Unit": unit_to_add,
                         "Amount": amount_to_add}
            self.ingredients_and_units.append(temp_dict)
            self.save_json_to_file()
            self.load_json_from_file()
            self.load_ingredients_window_with_json()
            self.reset_all_fields()

    def delete_entry(self):
        id_num = self.list_to_convert.focus()

        row = self.find_selected_row_in_list(id_num)
        if row >= 0:
            del self.ingredients_and_units[row]
            self.save_json_to_file()
            self.load_json_from_file()
            self.load_ingredients_window_with_json()
            self.reset_all_fields()

    # def proceed(self):
    #     if len(self.ingredients_and_units) > 0:
    #         self.controller.show_frame(InputMeasurements)


class InputMeasurements(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.input_frame = tk.LabelFrame(self, text="Enter a number for each ingredient")
        self.button_frame = tk.LabelFrame(self)

root = BakingConversionApp()
root.mainloop()
