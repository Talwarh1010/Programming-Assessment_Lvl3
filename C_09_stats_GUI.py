from tkinter import *
from functools import partial
import pygame

class Flags:
    def __init__(self):
        # Initialize the game with 5 questions
        self.to_play(5)

    def to_play(self, num_questions):
        # Create an instance of Play with the entered number of questions
        Play(num_questions)
        # Hide the main window (rounds choice window)
        root.withdraw()

    def play_music(self):
        # Load and play background music
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)

class Play:
    def __init__(self, how_many):
        # Create a new window for the game
        self.play_box = Toplevel(width=600, height=400)
        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

        # Create a frame for control buttons
        self.control_frame = Frame(self.play_frame)
        self.control_frame.grid(row=6)

        # Define control buttons with colors, text, and actions
        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        self.control_button_ref = []

        # Create control buttons and bind actions to them
        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)
            self.control_button_ref.append(self.make_control_button)

        # Disable the help button initially
        self.to_help_btn = self.control_button_ref[0]

    def close_play(self):
        # Show the main window (rounds choice window) and destroy the game window
        root.deiconify()
        self.play_box.destroy()

    def to_do(self, action):
        # Handle button actions
        if action == "get help":
            pass
        elif action == "get stats":
            # Disable stats button and open statistics window
            self.control_button_ref[1].config(state=DISABLED)
            DisplayStats(self)
        else:
            # Close the game window
            self.close_play()

class DisplayStats:
    def __init__(self, partner):
        self.partner = partner  # Store the instance of Play class

        # Simulated data for statistics
        questions_answered = 11
        correct_numbers = 6
        user_answers = [('Sudan', 'Qatar'), ('\ufeffAruba', '\ufeffAruba'), ('Somalia', 'Suriname'), ('Libya', 'Kosovo')
            , ('Moldova', 'Moldova'), ('Montenegro', 'Montenegro'), ('Andorra', 'Andorra'),
                        ('Seychelles', 'Marshall Islands'), ('Cameroon', 'Cameroon'), ('Ivory Coast', 'Ivory Coast'), ('China', 'Vietnam')]

        # Setup dialogue box and background color
        stats_bg_colour = "#DAE8FC"
        self.stats_box = Toplevel()
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats))

        # Create a frame for displaying statistics
        self.stats_frame = Frame(self.stats_box, width=700, height=400, bg=stats_bg_colour)
        self.stats_frame.grid()

        # Add heading for statistics
        self.stats_heading_label = Label(self.stats_frame, bg=stats_bg_colour, text="Statistics", font=("Arial", "14", "bold"))
        self.stats_heading_label.grid(row=0, columnspan=4, pady=5)

        # Add text to inform about game statistics
        stats_text = "Here are your game statistics"
        self.stats_text_label = Label(self.stats_frame, bg=stats_bg_colour, text=stats_text, wrap=350, justify="left")
        if len(user_answers) > 10:
            self.stats_text_label.config(text="Here are your game statistics (Note: The question history only shows your first 10 questions)")
        self.stats_text_label.grid(row=1, columnspan=4, padx=10, pady=5)

        # Create a frame for displaying question data
        self.data_frame = Frame(self.stats_frame, bg=stats_bg_colour, borderwidth=1, relief="solid")
        self.data_frame.grid(row=2, columnspan=4, padx=10, pady=10)

        # Add labels for column headings
        headings = ["Question Number", "Flag Shown", "User Answer", "Result"]
        for i, heading in enumerate(headings):
            heading_label = Label(self.data_frame, text=heading, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour, width=20, height=2, anchor="w")
            heading_label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

        # Populate data for each question
        for i, answer in enumerate(user_answers[:10]):
            question_number = i + 1
            flag_shown = answer[0]
            user_answer = answer[1]
            result = "Correct" if user_answer == flag_shown else "Incorrect"

            # Display data for each question
            question_number_label = Label(self.data_frame, text=question_number, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour, width=20, anchor="w")
            question_number_label.grid(row=i + 1, column=0, padx=5, pady=5, sticky="w")

            flag_shown_label = Label(self.data_frame, text=flag_shown, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour, width=20, anchor="w")
            flag_shown_label.grid(row=i + 1, column=1, padx=5, pady=5, sticky="w")

            user_answer_label = Label(self.data_frame, text=user_answer, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour, width=20, anchor="w")
            user_answer_label.grid(row=i + 1, column=2, padx=5, pady=5, sticky="w")

            result_label = Label(self.data_frame, text=result, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour, width=20, anchor="w")
            result_label.grid(row=i + 1, column=3, padx=5, pady=5, sticky="w")

        # Create a frame for displaying numeric statistics
        self.numbers_frame = Frame(self.stats_frame, bg=stats_bg_colour, borderwidth=1, relief="solid")
        self.numbers_frame.grid(row=3, column=0, padx=10, pady=10)

        row_names = ["Correct answers", "Total questions", "Percentage", "Feedback"]
        data_values = [correct_numbers, questions_answered,
                       "{:.2f}%".format(
                           (correct_numbers / questions_answered) * 100 if questions_answered != 0 else 0),
                       "Excellent!" if (correct_numbers / questions_answered) * 100 >= 70 else "Keep Practicing!"]

        for i, name in enumerate(row_names):
            heading_label = Label(self.numbers_frame, text=name, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                                  width=15,
                                  height=2, anchor="w")
            heading_label.grid(row=i, column=0, padx=5, pady=1, sticky="w")

            data_label = Label(self.numbers_frame, text=data_values[i], bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                               width=20, height=1, anchor="w")
            data_label.grid(row=i, column=1, padx=5, pady=5, sticky="w")

        self.filename_entry_frame = Frame(self.stats_frame, bg=stats_bg_colour, relief="solid")
        self.filename_entry_frame.grid(row=3, column=2, columnspan=5, padx=10, pady=10)

        save_text = "Either choose a custom file name (and push " \
                    "<Export>) or simply push <Export> to save your " \
                    "statistics in a text file. If the " \
                    "filename already exists, it will be overwritten!"
        self.save_instructions_label = Label(self.filename_entry_frame,
                                             text=save_text,
                                             wraplength=300,
                                             justify="left", width=40,
                                             padx=10, pady=10)
        self.save_instructions_label.grid(row=2, column=4)

        self.filename_entry = Entry(self.filename_entry_frame,
                                    font=("Arial", "23"),
                                    bg="#ffffff", width=18)
        self.filename_entry.grid(row=4, column=4, padx=10, pady=10)
        self.button_frame = Frame(self.stats_frame, bg=stats_bg_colour)
        self.button_frame.grid(row=4, columnspan=5, )
        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export", bg="#004C99",
                                    fg="#FFFFFF", width=12,
                                    command="")
        self.export_button.grid(row=6, column=3, padx=5, pady=5)

        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF", width=12,
                                     command=self.close_stats)
        self.dismiss_button.grid(row=6, column=4, padx=5, pady=5)

    def close_stats(self):
        # Put stats button back to normal...
        self.partner.control_button_ref[1].config(state=NORMAL)  # Enable stats button
        self.stats_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Guess the Flag!")
    Play(10)
    root.mainloop()
