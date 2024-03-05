import tkinter as tk
from tkinter import PhotoImage, Button, Frame, Label, Entry, Toplevel, DISABLED
import pygame
from functools import partial
import csv
import random
from PIL import Image, ImageTk


class Flags:
    def __init__(self, root):
        self.bg = PhotoImage(file="flags2.png")

        # Set background image
        background_label = Label(root, image=self.bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Set GUI Frame
        main_frame = Frame(root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = Label(main_frame, text=" Guess The Flag!", font=("Arial", "45", "bold"))
        title_label.grid(row=0, column=0, columnspan=2)

        instructions_label = Label(main_frame,
                                   text="\tWelcome to Guess The Flag!\nEnter the amount of questions you would like "
                                        "to play",
                                   font=("Arial", "12"))
        instructions_label.grid(row=1, column=0, columnspan=2)

        self.question_entry = Entry(main_frame, font=("Arial", "20"))
        self.question_entry.grid(row=2, column=0, columnspan=2)

        self.start_button = Button(main_frame, font=("Arial", "18"), width=21, text="Start!", command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=2)

    def start_game(self):
        num_rounds = self.question_entry.get()
        play_window = Play(num_rounds)
        play_window.show()

    def play_music(self):
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)


class Play:
    def __init__(self, how_many):
        self.play_window = Toplevel(width=600, height=400)
        self.play_window.protocol('WM_DELETE_WINDOW', self.close_play)
        self.questions_wanted = how_many

        self.all_flags = self.get_all_flags()

        # Main frame
        self.main_frame = Frame(self.play_window)
        self.main_frame.pack()

        self.round_label = Label(self.main_frame, text="Round 1 of " + str(how_many), font=("Arial", "16", "bold"))
        self.round_label.grid(row=0, column=0, columnspan=2)

        instructions = "Look at the flag and choose one of the countries below. When you choose " \
                       "a country, the results of the question will be revealed."
        self.instructions_label = Label(self.main_frame, text=instructions, wraplength=350, justify="left")
        self.instructions_label.grid(row=1, column=0, columnspan=2)

        # Create flag label
        self.flag_label = Label(self.main_frame)
        self.flag_label.grid(row=2, column=0, columnspan=2)

        # Get and display question flags
        self.get_question_flags()

        # Frame for choice buttons
        choice_frame = Frame(self.main_frame)
        choice_frame.grid(row=3, column=0, columnspan=2)

        self.button_flag_list = []
        for item in range(0, 4):
            choice_button = Button(choice_frame, width=28, height=3,
                                   command=lambda i=item: self.to_compare(self.button_flag_list[i]))
            choice_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)
            self.button_flag_list.append(choice_button)

        # Control buttons frame
        control_frame = Frame(self.main_frame)
        control_frame.grid(row=4, column=0, columnspan=2)

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]]

        for i, (bg_color, text, command) in enumerate(control_buttons):
            button = Button(control_frame, fg="#FFFFFF", bg=bg_color, text=text, width=11, font=("Arial", "12", "bold"))
            button.grid(row=0, column=i, padx=5, pady=5)
            if i == 1:
                button.config(state=DISABLED)

    def show(self):
        self.play_window.mainloop()

    def close_play(self):
        self.play_window.destroy()

    def get_all_flags(self):
        with open("Country_Flags/country_flags.csv", "r") as file:
            return list(csv.reader(file, delimiter=","))

    def get_question_flags(self):
        question_flags_list = []
        flag_codes = []
        flag_list = self.get_all_flags()

        # Get four unique flags
        while len(question_flags_list) < 4:
            # Choose a flag
            chosen_flag = random.choice(flag_list)
            index_chosen = flag_list.index(chosen_flag)

            # Check if the flag code is not already in the list
            if chosen_flag[2] not in flag_codes:
                # Add the flag to the question flags list
                question_flags_list.append(chosen_flag)
                flag_codes.append(chosen_flag[2])

                # Remove the flag from the master list
                self.all_flags.pop(index_chosen)

                # Open the flag image
                flag = Image.open(f"Country_Flags/flag_images/{chosen_flag[3]}")

                # Resize the flag image
                resized = flag.resize((300, 225), Image.LANCZOS)

                # Convert the resized image to a PhotoImage object and store a reference
                resized_image = ImageTk.PhotoImage(resized)

                # Set the resized image as the flag label's image
                self.flag_label.config(image=resized_image)
                self.flag_label.image = resized_image

        return question_flags_list


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("720x540")
    pygame.mixer.init()
    root.title("Guess The Flag!")

    flags_app = Flags(root)
    flags_app.play_music()

    root.mainloop()
