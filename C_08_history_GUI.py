from tkinter import *
import pygame


class Flags:
    def __init__(self):
        # Initialize the Flags class
        self.to_play(5)  # Call the to_play method with 5 as the number of questions

    def to_play(self, num_questions):
        # Initialize the game with the specified number of questions
        Play(5)  # Create an instance of Play with the entered number of rounds
        root.withdraw()  # Hide start_window window (i.e., hide choose question window).

    def play_music(self):
        # Load and play background music
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)


class Play:
    def __init__(self, how_many):
        # Initialize the play window
        self.play_box = Toplevel(width=600, height=400)

        # Create a frame to contain play elements
        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

        # Create control buttons frame
        self.control_frame = Frame(self.play_frame)
        self.control_frame.grid(row=6)

        # Define control buttons
        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        self.control_button_ref = []

        # Create and place control buttons
        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))

            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            self.control_button_ref.append(self.make_control_button)

        # Disable help button
        self.to_help_btn = self.control_button_ref[0]

    def close_play(self):
        # Close the play window and restore the main window
        root.deiconify()
        self.play_box.destroy()

    def to_do(self, action):
        # Execute actions based on button clicks
        if action == "get help":
            pass  # Placeholder for displaying help
        elif action == "get stats":
            DisplayStats()  # Display statistics
        else:
            self.close_play()  # Close the play window


class DisplayStats:
    def __init__(self):
        # Retrieve data for game statistics
        result_data = ["Correct", "Wrong", "Correct", "Correct", "Wrong", "Correct",
                       "Wrong", "Wrong", "Correct", "Correct"]

        questions_answered = len(result_data)
        correct_numbers = result_data.count('Correct')
        user_answers = [('Sudan', 'Qatar'), ('\ufeffAruba', '\ufeffAruba'), ('Somalia', 'Suriname'), ('Libya', 'Kosovo')
            , ('Moldova', 'Moldova'), ('Montenegro', 'Montenegro'), ('Andorra', 'Andorra'),
                        ('Seychelles', 'Marshall Islands'), ('Cameroon', 'Cameroon'), ('Ivory Coast', 'Ivory Coast'),
                        ('Sudan', 'Qatar'), ('\ufeffAruba', '\ufeffAruba'), ('Somalia', 'Suriname'), ('Libya', 'Kosovo')
            , ('Moldova', 'Moldova'), ('Montenegro', 'Montenegro'), ('Andorra', 'Andorra'),
                        ('Seychelles', 'Marshall Islands'), ('Cameroon', 'Cameroon'), ('Ivory Coast', 'Ivory Coast')]

        # Setup dialogue box for displaying statistics
        stats_bg_colour = "#DAE8FC"
        self.stats_box = Toplevel()
        self.stats_box.protocol('WM_DELETE_WINDOW', self.close_stats)

        # Create frame for statistics display
        self.stats_frame = Frame(self.stats_box, width=700, height=400, bg=stats_bg_colour)
        self.stats_frame.grid()

        # Create label for statistics heading
        self.stats_heading_label = Label(self.stats_frame, bg=stats_bg_colour, text="Statistics",
                                         font=("Arial", "14", "bold"))
        self.stats_heading_label.grid(row=0, columnspan=4, pady=5)

        # Display text explaining statistics
        stats_text = "Here are your game statistics"
        self.stats_text_label = Label(self.stats_frame, bg=stats_bg_colour, text=stats_text, wrap=350,
                                      justify="left")
        self.stats_text_label.grid(row=1, columnspan=4, padx=10, pady=5)

        # Create frame for displaying data
        self.data_frame = Frame(self.stats_frame, bg=stats_bg_colour, borderwidth=1, relief="solid")
        self.data_frame.grid(row=2, columnspan=4, padx=10, pady=10)

        # Create headings for data table
        headings = ["Question Number", "Flag Shown", "User Answer", "Result"]
        for i, heading in enumerate(headings):
            heading_label = Label(self.data_frame, text=heading, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                                  width=20, height=2, anchor="w")
            heading_label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

        # Populate data table with statistics
        for i, answer in enumerate(user_answers):
            question_number = i + 1
            flag_shown = answer[0]
            user_answer = answer[1]
            result = "Correct" if user_answer == flag_shown else "Incorrect"

            question_number_label = Label(self.data_frame, text=question_number,
                                          bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                                          width=20, anchor="w")
            question_number_label.grid(row=i + 1, column=0, padx=5, pady=5, sticky="w")

            flag_shown_label = Label(self.data_frame, text=flag_shown, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                                     width=20, anchor="w")
            flag_shown_label.grid(row=i + 1, column=1, padx=5, pady=5, sticky="w")

            user_answer_label = Label(self.data_frame, text=user_answer,
                                      bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                                      width=20, anchor="w")
            user_answer_label.grid(row=i + 1, column=2, padx=5, pady=5, sticky="w")

            result_label = Label(self.data_frame, text=result, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                                 width=20, anchor="w")
            result_label.grid(row=i + 1, column=3, padx=5, pady=5, sticky="w")

            # Create frame for the buttons and filename entry
        self.numbers_frame = Frame(self.stats_frame, bg=stats_bg_colour, borderwidth=1, relief="solid")
        self.numbers_frame.grid(row=3, column=0, padx=10, pady=10)

        self.filename_entry_frame = Frame(self.stats_frame, bg=stats_bg_colour, relief="solid")
        self.filename_entry_frame.grid(row=3, column=2, columnspan=5, padx=10, pady=10)

        # Display instructions for saving statistics
        save_text = "Either choose a custom file name (and push <Export>) or simply push <Export> to save your " \
                    "statistics in a text file. If the filename already exists, it will be overwritten!"
        self.save_instructions_label = Label(self.filename_entry_frame,
                                             text=save_text,
                                             wraplength=300,
                                             justify="left", width=40,
                                             padx=10, pady=10)
        self.save_instructions_label.grid(row=2, column=4)

        # Entry widget for custom filename
        self.filename_entry = Entry(self.filename_entry_frame,
                                    font=("Arial", "23"),
                                    bg="#ffffff", width=18)
        self.filename_entry.grid(row=4, column=4, padx=10, pady=10)

        # Export button to save statistics
        self.button_frame = Frame(self.stats_frame, bg=stats_bg_colour)
        self.button_frame.grid(row=4, columnspan=5)

        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export", bg="#004C99",
                                    fg="#FFFFFF", width=12,
                                    command="")
        self.export_button.grid(row=6, column=3, padx=5, pady=5)

        # Dismiss button to close the statistics window
        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF", width=12,
                                     command="")
        self.dismiss_button.grid(row=6, column=4, padx=5, pady=5)

    def close_stats(self):
        # Close the statistics window
        self.stats_box.destroy()

    # Main program starts here


if __name__ == "__main__":
    root = Tk()
    root.title("Guess the Flag!")
    Play(10)  # Initialize the game with 10 questions
    root.mainloop()
