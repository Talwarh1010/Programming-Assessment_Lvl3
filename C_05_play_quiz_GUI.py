from tkinter import *
import pygame
from functools import partial  # To prevent unwanted windows
import csv
import random
from PIL import Image, ImageTk

class Flags:
    def __init__(self):
        self.to_play(5)

    def to_play(self, num_questions):
        Play(5)  # Create an instance of Play with the entered number of rounds
        root.withdraw()  # Hide start_window window (i.e., hide rounds choice window).

    def play_music(self):
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)


class Play:
    def __init__(self, how_many):
        # Create a new window for playing the game
        self.play_box = Toplevel(width=600, height=400)
        # Define behavior when the window's close button is clicked
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_play))
        # Variable to store the number of questions to be asked
        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)
        # Variable to keep track of the number of questions played
        self.questions_played = IntVar()
        self.questions_played.set(0)
        # Variable to keep track of the number of correct answers
        self.questions_correct = IntVar()
        self.questions_correct.set(0)
        # List to store user's answers
        self.user_answers = []

        # Load all flags from the CSV file
        self.all_flags = self.get_all_flags()
        # Create a frame to hold the game elements
        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()
        # Update the round heading initially
        self.update_round_heading()

        # Instructions for the game
        instructions = "Look at the flag and choose one of the countries below. When you choose " \
                       "a country, the results of the question will be revealed."

        # Label to display instructions
        self.instructions_label = Label(self.play_frame, text=instructions,
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)
        # Label to display the flag image
        self.flag_label = Label(self.play_frame)
        self.flag_label.grid(row=2)

        self.button_flag_list = []

        # Frame to hold the choice buttons
        self.choice_frame = Frame(self.play_frame)
        self.choice_frame.grid(row=4)
        self.choice_button_ref = []
        # Frame to hold control buttons
        self.control_frame = Frame(self.play_frame)
        self.control_frame.grid(row=6)
        # Control buttons configuration
        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]]

        self.control_button_ref = []

        # Create control buttons
        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))

            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)  # Update row to 0

            self.control_button_ref.append(self.make_control_button)

        # Disable help button initially
        self.to_help_btn = self.control_button_ref[0]
        self.to_stats_btn = self.control_button_ref[1]
        self.to_stats_btn.config(state=DISABLED)
        # Create choice buttons
        self.choice_buttons = []
        for item in range(0, 4):
            self.choice_button = Button(self.choice_frame, text="",
                                        width=28, height=3,
                                        command=lambda i=item: self.check_answer(self.choice_buttons[i]["text"]))
            self.choice_buttons.append(self.choice_button)
            self.choice_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)
        # Load the question flags
        self.get_question_flags()

        # Frame to display scores and next question button
        self.score_frame = Frame(self.play_frame)
        self.score_frame.grid(row=5, pady=5)
        # Label to display round results
        self.round_results_label = Label(self.score_frame, text=f"Answers Correct: Questions Answered:",
                                         width=36, bg="#FFF2CC",
                                         font=("Arial", 10),
                                         pady=5)
        self.round_results_label.grid(row=0, column=0, padx=5)
        # Button to move to the next question
        self.next_button = Button(self.score_frame, text="Next Question",
                                  fg="#FFFFFF", bg="#008BFC",
                                  font=("Arial", 11, "bold"),
                                  width=14, command=self.next_question, state=DISABLED)
        self.next_button.grid(row=0, column=1)
        self.questions_wanted = 5

    def update_round_heading(self):
        # Update round heading
        rounds_heading = f"Choose - Question 1 of 5"
        self.choose_heading = Label(self.play_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

    def close_play(self):
        # Close the play window and show the start window
        root.deiconify()
        self.play_box.destroy()

    def get_all_flags(self):
        # Load all flags from the CSV file
        with open("Country_Flags/country_flags.csv", "r", encoding="utf-8") as file:
            var_all_flags = list(csv.reader(file, delimiter=","))
        file.close()
        # Remove the header row
        return var_all_flags

    def get_question_flags(self):
        # Get flags for the current question
        self.question_flags = random.sample(self.all_flags, 4)
        self.current_correct_answer = random.randint(0, 3)

        # Set the text for choice buttons
        for i, flag in enumerate(self.question_flags):
            self.choice_buttons[i]['text'] = flag[0]

        # Load the flag image for the current question
        flag_image = Image.open(f"Country_Flags/flag_images/{self.question_flags[self.current_correct_answer][3]}")
        resized_flag_image = flag_image.resize((390, 250), Image.LANCZOS)
        resized_image = ImageTk.PhotoImage(resized_flag_image)
        self.flag_label.config(image=resized_image)
        self.flag_label.image = resized_image
        # Create the clue text outside the loop to avoid overlap
        self.clue_frame = Frame(self.play_frame)
        self.clue_frame.grid(row=3)

        self.clue_label = Label(self.clue_frame, text="", wrap=350)
        self.clue_label.grid(row=3)
        clue = f"Clue: The capital is {self.question_flags[self.current_correct_answer][1]}!"
        self.clue_label.config(text=clue)

    def next_question(self):
        # Reset the background color of all buttons to white
        for button in self.choice_buttons:
            button.config(bg="#FFFFFF", state=NORMAL)

        # Load next question if not reached the desired number of questions
        if self.questions_played.get() < self.questions_wanted:
            self.get_question_flags()
            how_many = self.questions_wanted
            current_round = self.questions_played.get()
            new_heading = "Choose - Question {} of " \
                          "{}".format(current_round + 1, how_many)
            self.choose_heading.config(text=new_heading)

            # Disable the Next button
            self.next_button.config(state=DISABLED)

    def check_answer(self, selected_country):
        self.questions_played.set(self.questions_played.get() + 1)
        self.correct_country = self.all_flags[self.current_correct_answer][0]
        self.user_answers.append((self.question_flags[self.current_correct_answer][0], selected_country))
        self.to_stats_btn.config(state=NORMAL)

        # Disable all buttons to prevent further clicks
        for button in self.choice_buttons:
            button.config(state=DISABLED)

        if selected_country == self.question_flags[self.current_correct_answer][0]:
            # Correct answer
            self.questions_correct.set(self.questions_correct.get() + 1)

            # Update the background color of the results label to green
            self.round_results_label.config(bg="#4CAF50", text=f"Answers Correct: {self.questions_correct.get()} / "
                                                               f"Questions Answered: {self.questions_played.get()}")  # Green color

            self.choice_buttons[self.current_correct_answer].config(bg="#4CAF50")  # Green color
        else:
            # Incorrect answer
            # Update the background color of the results label to red
            self.round_results_label.config(bg="#FF5252")  # Red color

            for i, button in enumerate(self.choice_buttons):
                if self.all_flags[i][0] == self.correct_country:
                    button.config(bg="#4CAF50")  # Green color
                else:
                    button.config(bg="#FF5252")  # Red color

        # Update the text of the results label after each answer
        self.round_results_label.config(text=f"Answers Correct: {self.questions_correct.get()} / "
                                             f"Questions Answered: {self.questions_played.get()}")

        # Enable the Next button after answering
        if self.questions_played.get() < self.questions_wanted:
            self.next_button.config(state=NORMAL)
        else:
            # Disable the Next button
            self.next_button.config(state=DISABLED)

    def to_do(self, action):
        if action == "get help":
            print("You chose to get help")
        elif action == "get stats":
            print("You chose to get the statistics")
        else:
            self.close_play()


if __name__ == "__main__":
    root = Tk()
    root.title("Guess The Flag!")
    Play(5)  # Pass start_window as an argument

    root.mainloop()
