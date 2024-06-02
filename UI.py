# Code by Luann Pascucci
# initially starting out by following https://tkdocs.com/tutorial/intro.html
# and then modifying as needed

# This is part of a project for CS361 at Oregon State University.

import tkinter as tk
# from tkinter import *
from tkinter import ttk
import json
import zmq

context = zmq.Context()

# sockets for the conversion microservice functions
butter_socket = context.socket(zmq.REQ)
butter_socket.connect("tcp://localhost:4444")
flour_socket = context.socket(zmq.REQ)
flour_socket.connect("tcp://localhost:3333")
sugar_socket = context.socket(zmq.REQ)
sugar_socket.connect("tcp://localhost:2222")

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
# quick conversion info
with open('quick_conversion_list.txt', 'r') as shortcut_list:
    quick_ingr_list = shortcut_list.read()


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
        close_button = tk.Button(self, text="Close Program", command=self.master.quit)
        quick_list = tk.Button(self, text="Get Quick List", command=self.open_quick_list)

        # layout
        Intro_label.grid(column=1, row=0, columnspan=5)
        copyright_label.grid(column=1, row=5)
        privacy_label.grid(column=1, row=4)
        start_button.grid(column=1, row=1)
        quick_list.grid(column=1, row=2)
        close_button.grid(column=1, row=3)

    def open_quick_list(self):
        new_window = tk.Toplevel()
        content = tk.Label(new_window, text=quick_ingr_list)
        content.grid()

class IngrChoose(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.input_frame = tk.LabelFrame(self, text="Add Ingredient to List")
        self.button_frame = tk.LabelFrame(self)
        self.list_to_convert = ttk.Treeview(self, columns=(1, 2, 3), show="headings")
        self.output_frame = tk.LabelFrame(self, text="Your Converted Ingredients")
        self.converted_output = ttk.Treeview(self, columns=(1, 2), show="headings")

        self.ingredients_and_units = []
        self.converted_ingredients = []

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
        self.converted_output.heading(1, text="Ingredient")
        self.converted_output.heading(2, text="Grams")
        self.converted_output.column("1", stretch=True)
        self.converted_output.column("2", stretch=False)

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

        # buttons: delete, add new ingredient, convert, close
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_entry)
        self.add_ingr_button = tk.Button(self.button_frame, text="Add Ingredient", command=self.add_entry)
        self.convert_button = tk.Button(self.button_frame, text="Convert", command=self.convert_all)
        self.close_button = tk.Button(self.button_frame, text="Close Program", command=self.master.quit)
        self.back_button = tk.Button(self.button_frame, text="Previous", command=lambda: controller.show_frame(StartPage))
        
        # layout
        self.instructions.grid(column=0, row=0)
        self.input_frame.grid(row=1, column=0, rowspan=3, columnspan=5)
        self.button_frame.grid(column=0, row=4)
        self.list_to_convert.grid(column=0, row=7)
        self.output_frame.grid(column=0, row=20)
        self.converted_output.grid(column=0)

        self.ingr_list_label.grid(column=0, row=1)
        self.ingr_drop.grid(column=0, row=1)
        self.convert_from_label.grid(column=1, row=1)
        self.unit_drop.grid(column=2, row=1)
        self.amount_to_convert_label.grid(column=3, row=1)
        self.amount_enter.grid(column=4, row=1)

        self.delete_button.grid(column=3, row=1)
        self.add_ingr_button.grid(column=1, row=1)
        self.convert_button.grid(column=2, row=1)
        self.close_button.grid(column=4, row=1)
        self.back_button.grid(column=0, row=1)

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

    def update_everything(self):
        self.save_json_to_file()
        self.load_json_from_file()
        self.load_ingredients_window_with_json()
        self.reset_all_fields()

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
            self.update_everything()

    def delete_entry(self):
        id_num = self.list_to_convert.focus()

        row = self.find_selected_row_in_list(id_num)
        if row >= 0:
            del self.ingredients_and_units[row]
            self.update_everything()

    def convert_all(self):
        # go through each json list item in order - for loop does this
        # send to conversion microservices
        # get back and put in same order as before - for loop does this

        for item in self.ingredients_and_units:
            # check ingredient type
            if item["Ingredient"] == "Butter":
                sent_item = json.dumps(item)
                butter_socket.send_string(sent_item)
                converted_butter = butter_socket.recv_string()
                self.converted_ingredients.append(json.loads(converted_butter))
            if item["Ingredient"] == "Flour: AP":


        with open("converted_info.json", "w") as file_handler:
            json.dump(self.converted_ingredients, file_handler, indent=4)
        file_handler.close
        self.display_conversions()
   
    def display_conversions(self):
        with open("converted_info.json", "r") as file_handler:
            self.converted_ingredients = json.load(file_handler)
        file_handler.close
        
        for item in self.converted_output.get_children():
            self.converted_output.delete(item)

        rowIndex = 1
        for item in self.converted_ingredients:
            for key, value in item.items():
                self.converted_output.insert('', index="end", iid=rowIndex, text='', values=(key, value))
                rowIndex += 1


class InputMeasurements(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.input_frame = tk.LabelFrame(self, text="Enter a number for each ingredient")
        self.button_frame = tk.LabelFrame(self)


root = BakingConversionApp()
root.mainloop()
