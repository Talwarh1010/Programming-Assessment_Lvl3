# To create all GUI
from tkinter import *
# Load background music
import pygame
from functools import partial  # To prevent unwanted windows
# Get all data from Excel file
import csv
# To choose random flag image to be shown
import random
# Resize flag image
from PIL import Image, ImageTk
# Get date for file name
from datetime import date
# For regular expressions
import re


class Flags:
    def __init__(self, start_screen):
        # Load background image
        self.background_image = PhotoImage(file="flags2.png")

        # Create canvas to display the background image
        self.background_canvas = Canvas(start_screen, width=720, height=540)
        self.background_canvas.grid(row=1, column=0, sticky="nsew")
        self.background_canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Create a white rectangle as background for the main frame
        self.background_canvas.create_rectangle(120, 180, 600, 420, fill="white")

        # Set up GUI frame
        self.background_canvas.create_text(350, 220, text=" Guess The Flag!", font=("Arial", "45", "bold"))
        self.background_canvas.create_text(360, 280,
                                           text="\tWelcome to Guess The Flag!\nEnter the amount of questions you "
                                                "would like to play", font=("Arial", "12"))

        # Entry widget for the user to input the number of questions
        self.question_entry = Entry(start_screen, font=("Arial", "20"))
        self.background_canvas.create_window(365, 330, window=self.question_entry)

        # Button to start the flag quiz.
        self.start_button = Button(start_screen, font=("Arial", "18"), width=21, text="Start!",
                                   command=self.validate_and_start)
        self.background_canvas.create_window(369, 395, window=self.start_button)

    def validate_and_start(self):
        # Retrieve the number of questions entered by the user
        num_questions = self.question_entry.get()

        # Create an error label widget with empty text
        error_label = Label(root, bg="white", text="                                                           "
                                                   "                                                                 ")

        if num_questions.isdigit() and int(num_questions) > 0:
            # If the input is a valid integer greater than 0, start the quiz
            self.start_quiz(int(num_questions))
            self.question_entry.config(bg="white")
            self.question_entry.delete(0, END)
        else:
            # If the input is invalid, display an error message
            error_text = "Please enter a valid integer greater than 0."
            self.question_entry.config(bg="#F8CECC")
            error_label.config(text=error_text, font=("Arial", "10"), fg="red", bg="white")

        # Place the error label widget below the question entry
        error_label.place(x=243, y=350)

    @staticmethod
    def start_quiz(num_questions):
        # Start the quiz with the entered number of questions
        Play(num_questions)
        root.withdraw()  # Hide the start window

    @staticmethod
    def play_music():
        # Load and play background music
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=-1)


class Play:
    def __init__(self, num_questions):
        # Initialize the quiz play window
        self.play_box = Toplevel(width=600, height=400)
        # Close play box when close button or "X" button in the top-right corner of the window is pressed.
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_play))

        # Initialize variables to keep track of quiz progress
        self.num_questions_wanted = IntVar()
        self.num_questions_wanted.set(num_questions)
        self.questions_answered = IntVar()
        self.questions_answered.set(0)
        self.questions_correct = IntVar()
        self.questions_correct.set(0)
        # List to hold user answers
        self.user_response_history = []

        # Load all flag data from CSV file
        self.all_flags = self.get_all_flags()

        # Create the main quiz frame
        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

        # Starting heading of the quiz
        question_heading = f"Choose - Question 1 of {self.num_questions_wanted.get()}"
        self.choose_heading = Label(self.play_frame, text=question_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

        # Display quiz instructions
        instructions = "Look at the flag and choose one of the countries below. When you choose " \
                       "a country, the results of the question will be revealed."
        self.instructions_label = Label(self.play_frame, text=instructions,
                                        wraplength=350, justify="left")
        self.instructions_label.grid(row=1)
        self.flag_label = Label(self.play_frame)
        self.flag_label.grid(row=2)

        # Create buttons for flag choices
        self.choice_frame = Frame(self.play_frame)
        self.choice_frame.grid(row=4)
        self.choice_button_ref = []
        self.control_frame = Frame(self.play_frame)
        self.control_frame.grid(row=6)
        # Create list for control buttons. Info includes colour, text and function name.
        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]]

        # Create control buttons (Help, Statistics, Start Over)
        self.control_button_ref = []
        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))

            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            self.control_button_ref.append(self.make_control_button)

        # Disable the "Help" button and store a reference to it
        self.to_help_btn = self.control_button_ref[0]
        # Store a reference to the "Statistics" button
        self.to_stats_btn = self.control_button_ref[1]
        # Disable the "Statistics" button
        self.to_stats_btn.config(state=DISABLED)

        # Initialize an empty list to store the choice buttons
        self.answer_choice_buttons = []

        # Create four choice buttons for the user to select their answer
        for item in range(0, 4):
            # Create a Button widget for each choice
            self.choice_button = Button(self.choice_frame, text="",
                                        width=28, height=3,
                                        command=lambda i=item: self.check_answer(self.answer_choice_buttons[i]["text"]))

            # Append the created Button to the answer_choice_buttons list
            self.answer_choice_buttons.append(self.choice_button)

            # Place the Button in the choice_frame grid
            self.choice_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

        # Get the flags for the current question
        self.get_question_flags()

        # Create a frame to display the score information
        self.score_frame = Frame(self.play_frame)
        self.score_frame.grid(row=5, pady=5)

        # Label to display the current score information
        self.question_results_label = Label(self.score_frame, text=f"Answers Correct: Questions Answered:",
                                            width=36, bg="#FFF2CC",
                                            font=("Arial", 10),
                                            pady=5)
        self.question_results_label.grid(row=0, column=0, padx=5)

        # Button to proceed to the next question (disabled at the start of each question
        self.next_button = Button(self.score_frame, text="Next Question",
                                  fg="#FFFFFF", bg="#008BFC",
                                  font=("Arial", 11, "bold"),
                                  width=14, command=self.next_question, state=DISABLED)
        self.next_button.grid(row=0, column=1)

    @staticmethod
    def get_all_flags():
        # Read all flag data from the CSV file
        with open("Country_Flags/country_flags.csv", "r", encoding="utf-8") as file:
            var_all_flags = list(csv.reader(file, delimiter=","))
        # removes first entry in list (ie: the header row).
        return var_all_flags

    def get_question_flags(self):
        # Randomly select flags for the current question
        self.question_flags = random.sample(self.all_flags, 4)
        self.current_correct_answer = random.randint(0, 3)

        # Display flag images and country choices
        for i, flag in enumerate(self.question_flags):
            self.answer_choice_buttons[i]['text'] = flag[0]

        # resize flag image so that it fits in play GUI
        flag_image = Image.open(f"Country_Flags/flag_images/{self.question_flags[self.current_correct_answer][3]}")
        flag_image = ImageTk.PhotoImage(flag_image)
        self.flag_label.config(image=flag_image)
        self.flag_label.image = flag_image

        # Display clue for the correct country
        self.clue_frame = Frame(self.play_frame)
        self.clue_frame.grid(row=3)

        self.clue_label = Label(self.clue_frame,
                                text=f"Clue: The capital is {self.question_flags[self.current_correct_answer][1]}")
        self.clue_label.grid(row=3)

    def next_question(self):
        # Load next question if not reached the desired number of questions
        self.clue_label.config(text="")
        # Reset the background color of all buttons to white
        for button in self.answer_choice_buttons:
            button.config(bg="#FFFFFF", state=NORMAL)
        # Change heading of the question if the number of questions played has not exceeded the questions answered.
        if self.questions_answered.get() < self.num_questions_wanted.get():
            # Display flag and clue
            self.get_question_flags()
            new_heading = "Choose - Question {} of " \
                          "{}".format(self.questions_answered.get() + 1, self.num_questions_wanted.get())
            self.choose_heading.config(text=new_heading)

            # Disable the Next button
            self.next_button.config(state=DISABLED)

    def check_answer(self, selected_country):
        # Check the selected answer and update quiz statistics
        self.questions_answered.set(self.questions_answered.get() + 1)
        self.correct_country = self.all_flags[self.current_correct_answer][0]
        self.user_response_history.append((self.question_flags[self.current_correct_answer][0], selected_country))
        self.to_stats_btn.config(state=NORMAL)

        if selected_country == self.question_flags[self.current_correct_answer][0]:
            # Correct answer (add 1 point)
            self.questions_correct.set(self.questions_correct.get() + 1)

            # Update the background color of the results label to green
            self.question_results_label.config(bg="#4CAF50", text=f"Answers Correct: {self.questions_correct.get()} / "
                                                                  f"Questions Answered: {self.questions_answered.get()}")
            # Make correct answer green
            self.answer_choice_buttons[self.current_correct_answer].config(bg="#4CAF50")  # Green color
        else:
            # Incorrect answer
            # Update the background color of the results label to red
            self.question_results_label.config(bg="#FF5252")  # Red color
            for i, button in enumerate(self.answer_choice_buttons):
                # Make correct answer green
                if self.all_flags[i][0] == self.correct_country:
                    button.config(bg="#4CAF50")  # Green color
                    # Make all incorrect choices red
                else:
                    button.config(bg="#FF5252")  # Red color
        # Disable all buttons to prevent further clicks
        [button.config(state=DISABLED) for button in self.answer_choice_buttons]

        # Update the text of the results label after each answer
        self.question_results_label.config(text=f"Answers Correct: {self.questions_correct.get()} / "
                                                f"Questions Answered: {self.questions_answered.get()}")

        # Enable the Next button after answering
        if self.questions_answered.get() < self.num_questions_wanted.get():
            self.next_button.config(state=NORMAL)
        else:
            # Disable the Next button and change its text.
            self.next_button.config(state=DISABLED, bg="#808080", text="Goodbye")
            # Change text and colour of Start Over button after quiz has finished
            self.control_button_ref[2].config(text="New Quiz", bg="#009900")

    def to_do(self, action):
        # Perform actions based on button clicks (Help, Statistics, Start Over)
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats":
            DisplayStats(self, self.questions_correct.get(), self.questions_answered.get(), self.user_response_history)
        else:
            self.close_play()

    def close_play(self):
        # Close the play window and show the start window
        root.deiconify()
        self.play_box.destroy()


class DisplayHelp:
    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()
        # disable help button
        partner.to_help_btn.config(state=DISABLED)
        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))
        self.help_frame = Frame(self.help_box, width=300,
                                height=200,
                                bg=background)
        self.help_frame.grid()
        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Help / Hints",
                                        font=("Arial", "14", "bold"), wraplength=300)
        self.help_heading_label.grid(row=0)
        # Instructions text
        help_text = (
            "Welcome to Guess The Flag! You'll be presented with a flag and four country options. "
            "Select the country you believe matches the flag. Earn a point for each correct answer, "
            "displayed as 'Answers Correct / Questions Answered'. Don't forget to check the clue, "
            "which is the capital of the country flag given!\n\n"
            "Click 'Statistics' to track your overall performance and export it as a text file. "
            "The quiz ends after answering all questions, and you can proceed to the next question "
            "by clicking 'Next Question'.\n\n"
            "Have fun testing your flag knowledge! Good luck! Choose carefully."
        )

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        # Create dismiss button to exit help window
        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))

        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # Close help window.
    def close_help(self, partner):
        # Put help button back to normal...
        partner.to_help_btn.config(state=NORMAL)
        self.help_box.destroy()


class DisplayStats:
    def __init__(self, partner, correct_numbers, questions_answered, user_answers):
        # Initialise variables
        self.correct_numbers = correct_numbers
        self.questions_answered = questions_answered
        self.user_answers = user_answers

        # setup dialogue box and background colour
        stats_bg_colour = "#DAE8FC"
        self.stats_box = Toplevel()
        # disable stats button
        partner.to_stats_btn.config(state=DISABLED)
        # If users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))
        self.stats_frame = Frame(self.stats_box, width=700,
                                 height=400,
                                 bg=stats_bg_colour)
        self.stats_frame.grid()
        self.stats_heading_label = Label(self.stats_frame,
                                         bg=stats_bg_colour,
                                         text="Statistics",
                                         font=("Arial", "14", "bold"))
        self.stats_heading_label.grid(row=0, columnspan=4, pady=5)

        stats_text = "Here are your quiz statistics"
        self.stats_text_label = Label(self.stats_frame, bg=stats_bg_colour,
                                      text=stats_text, wraplength=350,
                                      justify="left")
        # If the user answers more than 10 questions, display a note
        if len(user_answers) > 10:
            self.stats_text_label.config(text="Here are your quiz statistics (Note: The question history only shows "
                                              "your first 10 questions")
        self.stats_text_label.grid(row=1, columnspan=4, padx=10, pady=5)
        self.data_frame = Frame(self.stats_frame, bg=stats_bg_colour, borderwidth=1, relief="solid")
        self.data_frame.grid(row=2, columnspan=4, padx=10, pady=10)

        # Create labels for headings and corresponding information
        headings = ["Question Number", "Flag Shown", "User Answer", "Result"]
        for i, heading in enumerate(headings):
            heading_label = Label(self.data_frame, text=heading, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                                  width=20, height=2, anchor="w")
            heading_label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

        # Populate the data for each question
        for i, answer in enumerate(user_answers[:10]):
            question_number = i + 1
            flag_shown = answer[0]
            user_answer = answer[1]
            result = "Correct" if user_answer == flag_shown else "Incorrect"
            # Creating labels to create a table of question history (Question number, flag, user answer, and result)
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

        # Create frame for scores and percentages
        self.scores_frame = Frame(self.stats_frame, bg=stats_bg_colour, borderwidth=1, relief="solid")
        self.scores_frame.grid(row=3, column=0, padx=10, pady=10)

        # Create labels for headings and scores (Correct answers, total questions, percentage and feedback)
        row_names = ["Correct answers", "Total questions", "Percentage", "Feedback"]
        # If percentage is more than or equal to 70%, display 'Excellent!' otherwise 'Keep Practicing'
        data_values = [correct_numbers, questions_answered,
                       "{:.2f}%".format(
                           (correct_numbers / questions_answered) * 100 if questions_answered != 0 else 0),
                       "Excellent!" if (correct_numbers / questions_answered) * 100 >= 70 else "Keep Practicing!"]
        # Create table to display scores and percentage
        for i, name in enumerate(row_names):
            heading_label = Label(self.scores_frame, text=name, bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                                  width=15,
                                  height=2, anchor="w")
            heading_label.grid(row=i, column=0, padx=5, pady=1, sticky="w")

            data_label = Label(self.scores_frame, text=data_values[i], bg="#C9D6E8" if i % 2 == 0 else stats_bg_colour,
                               width=20, height=1, anchor="w")
            data_label.grid(row=i, column=1, padx=5, pady=5, sticky="w")

        # Create frame for export part of statistics
        self.filename_entry_frame = Frame(self.stats_frame, bg=stats_bg_colour, relief="solid")
        self.filename_entry_frame.grid(row=3, column=2, columnspan=5, padx=10, pady=10)

        # Instructions to export statistics
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

        # Create entry box so user can enter filename
        self.filename_entry = Entry(self.filename_entry_frame,
                                    font=("Arial", "23"),
                                    bg="#ffffff", width=18)
        self.filename_entry.grid(row=4, column=4, padx=10, pady=10)

        # Frame to keep dismiss and export button
        self.button_frame = Frame(self.stats_frame, bg=stats_bg_colour)
        self.button_frame.grid(row=4, columnspan=5, )
        # Export button
        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export", bg="#004C99",
                                    fg="#FFFFFF", width=12,
                                    command=self.make_file)
        self.export_button.grid(row=6, column=3, padx=5, pady=5)
        # Dismiss button
        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF", width=12,
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=6, column=4, padx=5, pady=5)

    def make_file(self):
        # Retrieve filename
        filename = self.filename_entry.get()
        filename_ok = ""
        date_part = self.get_date()
        if filename == "":
            # Get date and create default filename
            filename = f"{date_part}_flagquiz"

        else:
            # Check that filename is valid
            filename_ok = self.check_filename(filename)

        if filename_ok == "":
            filename += ".txt"
            success = f"Success! Your quiz statistics have been saved as {filename}"
            # Write data to file
            self.write_to_file(filename)
            # Provide feedback to user
            self.save_instructions_label.config(text=success, fg="dark green", bg="#DAE8FC")
            self.filename_entry.config(bg="#90ee90")

        # If user enters invalid characters in filename (change colour to dark red and display error)
        else:
            error_message = f"Error: {filename_ok}. Use letters / numbers / underscores only."
            self.save_instructions_label.config(text=error_message, fg="dark red", bg="#DAE8FC")
            self.filename_entry.config(bg="#FF7F7F")

    # Function to get the current date
    @staticmethod
    def get_date():
        today = date.today()
        return today.strftime("%Y_%m_%d")

    @staticmethod
    def check_filename(filename):
        problem = ""
        # Regular expression to check filename is valid (Only allows alphabet,numbers, and underscores)
        valid_char = "[A-Za-z0-9_]"
        # Iterate through filename and check each character
        for character in filename:
            if re.match(valid_char, character):
                continue
                # If there is spaces in text file name, then display error
            elif character == " ":
                problem = "Sorry, no spaces allowed."
                # If any other invalid characters are used, display error
            else:
                problem = f"Sorry, no '{character}'s allowed."
            break
        return problem

    # Function that writes all statistics to a text file
    def write_to_file(self, filename):
        # Retrieve data
        correct_numbers = self.correct_numbers
        questions_answered = self.questions_answered
        user_answers = self.user_answers

        # Prepare content to write to file
        heading = "**** Quiz Statistics ****"
        generated_date = self.get_date()
        generated = f"Generated: {generated_date}"
        sub_heading = "Here are your quiz statistics:"
        data = f"{'Correct answers:':<20} {correct_numbers}\n" \
               f"{'Total questions:':<20} {questions_answered}\n" \
               f"{'Percentage:':<20} " \
               f"{'{:.2f}%'.format((correct_numbers / questions_answered) * 100 if questions_answered != 0 else 0)}\n" \
               f"{'Feedback:':<20} " \
               f"{'Excellent!' if (correct_numbers / questions_answered) * 100 >= 70 else 'Keep Practicing!'}\n" \
               "\nUser Answers:\n"

        # Loop to display all question history as string to display in text file
        for i, answer in enumerate(user_answers, start=1):
            question_number = f"Question {i}:"
            flag_shown = f"Flag Shown: {answer[0]}"
            user_answer = f"User Answer: {answer[1]}"
            result = "Result: Correct" if answer[0] == answer[1] else "Result: Incorrect"
            data += f"{question_number:<20} {flag_shown:<40} {user_answer:<40} {result:<20}\n"

        # Write data to file
        with open(filename, "w") as file:
            file.write(heading + "\n")
            file.write(generated + "\n")
            file.write(sub_heading + "\n")
            file.write(data + "\n")

    # Closes stats dialogue (used by button and x at top of dialogue)
    def close_stats(self, partner):
        # Put stats button back to normal...
        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()


if __name__ == "__main__":
    root = Tk()  # Create tk window
    root.geometry("720x540")  # Size of start GUI.
    pygame.mixer.init()  # For music
    root.title("Guess The Flag!")  # Change title of GUI to this
    flags_app = Flags(root)  # Use flag window to play music
    flags_app.play_music()  # Play background music
    root.mainloop()
