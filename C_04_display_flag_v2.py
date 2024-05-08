from tkinter import *
import pygame
import csv
import random
from PIL import Image, ImageTk

for item in range(0, 20):
    root = Tk()
    root.geometry("600x400")
    pygame.mixer.init()
    flag_label = Label(root)
    flag_label.grid(row=2)

    with open("Country_Flags/country_flags.csv", "r", encoding="utf-8") as file:
        var_all_flags = list(csv.reader(file, delimiter=","))
    file.close()

    question_flags = random.sample(var_all_flags, 4)
    current_correct_answer = random.randint(0, 3)
    flag_image = Image.open(f"Country_Flags/flag_images/{question_flags[current_correct_answer][3]}")
    resized_flag_image = flag_image.resize((390, 250), Image.LANCZOS)
    resized_image = ImageTk.PhotoImage(resized_flag_image)
    flag_label.config(image=resized_image)
    flag_label.image = resized_image
    clue_label = Label(root, text=f"Clue: The capital is {question_flags[current_correct_answer][1]}!", wrap=350)
    clue_label.grid(row=3)

    if __name__ == "__main__":
        root.title("Guess The Flag!")
        root.mainloop()
