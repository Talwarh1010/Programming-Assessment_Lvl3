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
        self.background_canvas = Canvas(root, width=720, height=540)
        self.background_canvas.grid(row=1, column=0, sticky="nsew")
        self.background_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.background_canvas.create_rectangle(120, 180, 600, 420, fill="white")
        # Set GUI Frame
        self.background_canvas.create_text(350, 220, text=" Guess The Flag!", font=("Arial", "45", "bold"))
        self.background_canvas.create_text(360, 280,
                                           text="\tWelcome to Guess The Flag!\nEnter the amount of questions you "
                                                "would like to play", font=("Arial", "12"))
        self.question_entry = Entry(root, font=("Arial", "20"))
        self.background_canvas.create_window(365, 335, window=self.question_entry)
        self.start_button = Button(root, font=("Arial", "18"), width=21, text="Start!",
                                   command=self.to_play)  # No need to pass response here
        self.background_canvas.create_window(369, 390, window=self.start_button)

    def to_play(self):
        num_rounds = self.question_entry.get()  # Get the number of rounds from the entry
        Play(num_rounds)  # Create an instance of Play with the entered number of rounds
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
        self.questions_played = IntVar()
        self.questions_played.set(0)
        self.questions_correct = IntVar()
        self.questions_correct.set(0)

        self.all_flags = self.get_all_flags()
        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()
        self.update_round_heading()  # Update round heading initially

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
        self.choice_frame.grid(row=4)
        self.choice_button_ref = []
        self.control_frame = Frame(self.play_frame)
        self.control_frame.grid(row=6)
        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]]

        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"))

            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)  # Update row to 0

            self.control_button_ref.append(self.make_control_button)

        # disable help button
        self.to_help_btn = self.control_button_ref[0]
        self.to_stats_btn = self.control_button_ref[1]
        self.to_stats_btn.config(state=DISABLED)
        self.choice_buttons = []
        for item in range(0, 4):
            self.choice_button = Button(self.choice_frame,text = "",
                                        width=28, height=3,
                                        command=lambda i=item: self.to_compare(self.button_flag_list[i]))
            self.choice_buttons.append(self.choice_button)
            self.choice_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)
        self.get_question_flags()

        self.rounds_frame = Frame(self.play_frame)
        self.rounds_frame.grid(row=5, pady=5)
        self.round_results_label = Label(self.rounds_frame, text=f"Answers Correct: Questions Answered:",
                                         width=32, bg="#FFF2CC",
                                         font=("Arial", 10),
                                         pady=5)
        self.round_results_label.grid(row=0, column=0, padx=5)

        self.next_button = Button(self.rounds_frame, text="Next Question",
                                  fg="#FFFFFF", bg="#008BFC",
                                  font=("Arial", 11, "bold"),
                                  width=10, command=self.next_question)
        self.next_button.grid(row=0, column=5)

    def update_round_heading(self):
        rounds_heading = f"Choose - Round 1 of {self.questions_wanted.get()}"
        self.choose_heading = Label(self.play_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

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
        question_flags = random.sample(self.all_flags, 4)
        self.current_correct_answer = random.randint(0, 3)

        for i, flag in enumerate(question_flags):
            self.choice_buttons[i]['text'] = flag[0]

        flag_image = Image.open(f"Country_Flags/flag_images/{question_flags[self.current_correct_answer][3]}")
        resized_flag_image = flag_image.resize((300, 225), Image.LANCZOS)
        resized_image = ImageTk.PhotoImage(resized_flag_image)
        self.flag_label.config(image=resized_image)
        self.flag_label.image = resized_image

        # Create the clue text outside the loop to avoid overlap
        self.clue_frame = Frame(self.play_frame)
        self.clue_frame.grid(row=3)
        self.clue_label = Label(self.clue_frame, text=f"Clue: The capital is {question_flags[self.current_correct_answer][1]}!", wrap=350)
        self.clue_label.grid(row=3)

    def next_question(self):
        # Update the number of questions played

        # Reset buttons
        for button in self.choice_buttons:
            button.config(state=NORMAL)

        # Load next question if not reached the desired number of questions
        if self.questions_played.get() < self.questions_wanted.get() - 1:
            self.get_question_flags()
            self.questions_played.set(self.questions_played.get() + 1)
            how_many = self.questions_wanted.get()
            current_round = self.questions_played.get()
            new_heading = "Choose - Round {} of " \
                          "{}".format(current_round + 1, how_many)
            self.choose_heading.config(text=new_heading)
            self.next_button.config(state=E)
        else:
            self.next_button.config(state = DISABLED)
            # Show game over or result message
            pass




if __name__ == "__main__":
    root = Tk()
    root.geometry("720x540")
    pygame.mixer.init()
    root.title("Guess The Flag!")

    flags_app = Flags(root)  # Pass root as an argument
    flags_app.play_music()  # Call the play method

    root.mainloop()
