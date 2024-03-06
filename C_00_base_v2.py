import tkinter
from tkinter import *
import pygame
from functools import partial  # To prevent unwanted windows
import csv
import random
from PIL import Image, ImageTk


class Flags:
    def __init__(self, root):
        self.bg = PhotoImage(file="flags2.png")

        # Show image using canvas
        background_canvas = Canvas(root, width=720, height=540)
        background_canvas.grid(row=1, column=0, sticky="nsew")
        background_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        background_canvas.create_rectangle(120, 180, 600, 420, fill="white")
        # Set GUI Frame
        background_canvas.create_text(350, 220, text=" Guess The Flag!", font=("Arial", "45", "bold"))
        background_canvas.create_text(360, 280, text="\tWelcome to Guess The Flag!\nEnter the amount of questions you "
                                                     "would like to play", font=("Arial", "12"))
        self.question_entry = Entry(root, font=("Arial", "20"))
        background_canvas.create_window(365, 335, window=self.question_entry)
        response = self.question_entry.get()
        self.start_button = Button(root, font=("Arial", "18"), width=21, text="Start!",
                                   command=lambda: self.to_play(response))
        background_canvas.create_window(369, 390, window=self.start_button)

    def to_play(self, num_rounds):
        Play(num_rounds)
        # Hide root window (ie: hide rounds choice window).
        root.withdraw()

    def play_music(self):
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)


class Play:
    def __init__(self, how_many):
        self.play_box = Toplevel(width=600, height=400)
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))
        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)

        self.all_flags = self.get_all_flags()
        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()
        rounds_heading = f"Choose - Round 1 of {how_many}"
        self.choose_heading = Label(self.play_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)
        instructions = "Look at the flag and choose one of the countries below. When you choose " \
                       "a country, the results of the question will be revealed."

        self.instructions_label = Label(self.play_frame, text=instructions,
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)
        self.flag_label = Label(self.play_frame)
        self.flag_label.grid(row=2)

        self.button_flag_list = []

        # create colour buttons (in choice_frame)!
        self.choice_frame = Frame(self.play_frame)
        self.choice_frame.grid(row=3)
        self.choice_button_ref = []
        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]]

        self.control_button_ref = []

        for item in range(0, ):
            self.make_control_button = Button(self.play_box,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"))

            self.make_control_button.grid(row=5, column=item, padx=5, pady=5)

            self.control_button_ref.append(self.make_control_button)

        # disable help button
        self.to_help_btn = self.control_button_ref[0]
        self.to_stats_btn = self.control_button_ref[1]
        self.to_stats_btn.config(state=DISABLED)

        for item in range(0, 4):
            self.choice_button = Button(self.choice_frame,
                                        width=28, height=3,
                                        command=lambda i=item: self.to_compare(self.button_flag_list[i]))
            self.choice_button_ref.append(self.choice_button)
            self.choice_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)
        self.get_question_flags()

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def get_all_flags(self):
        file = open("Country_Flags/country_flags.csv", "r")
        var_all_flags = list(csv.reader(file, delimiter=","))
        file.close()
        # removes first entry in list (ie: the header row).
        return var_all_flags

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

                resized = flag.resize((300, 225), Image.LANCZOS)

                # Convert the resized image to a PhotoImage object and store a reference
                resized_image = ImageTk.PhotoImage(resized)

                # Set the resized image as the flag label's image
                self.flag_label.config(image=resized_image)
                self.flag_label.image = resized_image

        # Create the clue text outside the loop to avoid overlap
        self.clue_frame = Frame(self.play_frame)
        self.clue_frame.grid(row=4)
        self.clue_label = Label(self.clue_frame, text=f"Clue: The capital is {chosen_flag[1]}!", wrap=350)
        self.clue_label.grid(row=1)

        return question_flags_list


if __name__ == "__main__":
    root = Tk()
    root.geometry("720x540")
    pygame.mixer.init()
    root.title("Guess The Flag!")

    flags_app = Flags(root)  # Pass root as an argument
    flags_app.play_music()  # Call the play method

    root.mainloop()
