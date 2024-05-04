import csv
import random
import tkinter
from tkinter import *
import pygame
from functools import partial  # To prevent unwanted windows
import csv
import random
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import date
import re

play_box = Toplevel(width=600, height=400)
self.flag_label = Label(self.play_frame)
        self.flag_label.grid(row=2)

with open("Country_Flags/country_flags.csv", "r", encoding="utf-8") as file:
    var_all_flags = list(csv.reader(file, delimiter=","))
file.close()
# buttons for play GUI)
print(var_all_flags)
print("Length: {}".format(len(var_all_flags)))

question_flags = random.sample(var_all_flags, 4)
current_correct_answer = random.randint(0, 3)
flag_image = Image.open(f"Country_Flags/flag_images/{question_flags[current_correct_answer][3]}")
resized_flag_image = flag_image.resize((390, 250), Image.LANCZOS)
resized_image = ImageTk.PhotoImage(resized_flag_image)
flag_label.config(image=resized_image)
flag_label.image = resized_image