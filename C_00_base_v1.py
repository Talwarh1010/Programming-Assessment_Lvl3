from tkinter import *
import pygame
from functools import partial  # To prevent unwanted windows
import csv
import random
from PIL import Image, ImageTk
from datetime import date
import re


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
        self.background_canvas.create_window(365, 330, window=self.question_entry)
        self.start_button = Button(root, font=("Arial", "18"), width=21, text="Start!",
                                   command=self.validate_and_start)  # Updated command to call validation function
        self.background_canvas.create_window(369, 395, window=self.start_button)

    def validate_and_start(self):
        num_questions = self.question_entry.get()
        if num_questions.isdigit() and int(num_questions) > 0:
            self.to_play(int(num_questions))
        else:
            text = "Please enter a valid integer greater than 0."
            self.question_entry.config(bg="#F8CECC")
            error_label = Label(root, text=text, font=("Arial", "10"), fg="red", bg="white")
            error_label.place(x=243, y=350)

    def to_play(self, num_questions):
        Play(num_questions)  # Create an instance of Play with the entered number of rounds
        root.withdraw()  # Hide start_window window (i.e., hide rounds choice window).

    def play_music(self):
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)


class Play:
    def __init__(self, how_many):
        self.play_box = Toplevel(width=600, height=400)
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_play))
        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)
        self.questions_played = IntVar()
        self.questions_played.set(0)
        self.questions_correct = IntVar()
        self.questions_correct.set(0)
        self.user_answers = []

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
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))

            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)  # Update row to 0

            self.control_button_ref.append(self.make_control_button)

        # disable help button
        self.to_help_btn = self.control_button_ref[0]
        self.to_stats_btn = self.control_button_ref[1]
        self.to_stats_btn.config(state=DISABLED)
        self.choice_buttons = []
        for item in range(0, 4):
            self.choice_button = Button(self.choice_frame, text="",
                                        width=28, height=3,
                                        command=lambda i=item: self.check_answer(self.choice_buttons[i]["text"]))
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
                                  width=14, command=self.next_question, state=DISABLED)
        self.next_button.grid(row=0, column=5)

    def update_round_heading(self):
        rounds_heading = f"Choose - Round 1 of {self.questions_wanted.get()}"
        self.choose_heading = Label(self.play_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

    def close_play(self):
        # reshow start_window (ie: choose rounds) and end current
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
        self.question_flags = random.sample(self.all_flags, 4)
        self.current_correct_answer = random.randint(0, 3)

        for i, flag in enumerate(self.question_flags):
            self.choice_buttons[i]['text'] = flag[0]

        flag_image = Image.open(f"Country_Flags/flag_images/{self.question_flags[self.current_correct_answer][3]}")
        resized_flag_image = flag_image.resize((390, 250), Image.LANCZOS)
        resized_image = ImageTk.PhotoImage(resized_flag_image)
        self.flag_label.config(image=resized_image)
        self.flag_label.image = resized_image

        # Create the clue text outside the loop to avoid overlap
        self.clue_frame = Frame(self.play_frame)
        self.clue_frame.grid(row=3)

        self.clue_label = Label(self.clue_frame, text="", wraplength=350)
        self.clue_label.grid(row=3)
        clue = f"                Clue: The capital is {self.question_flags[self.current_correct_answer][1]}!                       "
        self.clue_label.config(text=clue)

    def next_question(self):
        # Reset the background color of all buttons to white
        for button in self.choice_buttons:
            button.config(bg="#FFFFFF", state=NORMAL)

        # Load next question if not reached the desired number of questions
        if self.questions_played.get() < self.questions_wanted.get():
            self.get_question_flags()
            how_many = self.questions_wanted.get()
            current_round = self.questions_played.get()
            new_heading = "Choose - Round {} of " \
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
                                                               f"Questions Answered: {self.questions_played.get()}")

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
        if self.questions_played.get() < self.questions_wanted.get():
            self.next_button.config(state=NORMAL)
        else:
            # Disable the Next button
            self.next_button.config(state=DISABLED, bg="#808080", text="Goodbye")

    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats":
            DisplayStats(self, self.question_flags[self.current_correct_answer][0], self.questions_correct.get(),
                         self.questions_played.get(),
                         self.user_answers)
        else:
            self.close_play()


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
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)
        help_text = ("""You'll be presented with a flag and four country options; select the country you believe 
matches the flag. Earn a point for each correct answer, displayed as 'Answers Correct / Questions Answered'. 
Remember to see the clue which is the capital of the country flag given!\nClick 'Statistics' to track your 
overall performance and export it as a text file. The game ends after answering all questions, and you can 
proceed to the next question by clicking 'Next Question'.\nHave fun testing your flag knowledge!" Good luck! 
Choose carefully.""")

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))

        self.dismiss_button.grid(row=2, padx=10, pady=10)

    def close_help(self, partner):
        # Put help button back to normal...
        partner.to_help_btn.config(state=NORMAL)
        self.help_box.destroy()


class DisplayStats:
    def __init__(self, partner, correct_answers, correct_numbers, questions_answered, user_answers):
        # Other initialization code remains the same...
        self.correct_answers = correct_answers
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

        stats_text = "Here are your game statistics"
        self.stats_text_label = Label(self.stats_frame, bg=stats_bg_colour,
                                      text=stats_text, wraplength=350,
                                      justify="left")
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

        self.numbers_frame = Frame(self.stats_frame, bg=stats_bg_colour, borderwidth=1, relief="solid")
        self.numbers_frame.grid(row=3, column=0, padx=10, pady=10)

        # Create labels for headings and corresponding information
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
        self.button_frame = Frame(self.stats_frame)
        self.button_frame.grid(row=5, columnspan=5)
        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export", bg="#004C99",
                                    fg="#FFFFFF", width=12,
                                    command=self.make_file)
        self.export_button.grid(row=6, column=3, padx=5, pady=5)

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
            success = f"Success! Your game statistics have been saved as {filename}"
            # Write data to file
            self.write_to_file(filename)
            # Provide feedback to user
            self.stats_text_label.config(text=success, fg="dark green")
        else:
            error_message = f"Error: {filename_ok}. Use letters / numbers / underscores only."
            self.stats_text_label.config(text=error_message, fg="dark red")

    def get_date(self):
        today = date.today()
        return today.strftime("%Y_%m_%d")

    @staticmethod
    def check_filename(filename):
        problem = ""
        # Regular expression to check filename is valid
        valid_char = "[A-Za-z0-9_]"
        # Iterate through filename and check each character
        for letter in filename:
            if re.match(valid_char, letter):
                continue
            elif letter == " ":
                problem = "Sorry, no spaces allowed."
            else:
                problem = f"Sorry, no '{letter}'s allowed."
            break
        return problem

    def write_to_file(self, filename):
        # Retrieve data
        correct_numbers = self.correct_numbers
        questions_answered = self.questions_answered
        user_answers = self.user_answers

        # Prepare content to write to file
        heading = "**** Game Statistics ****"
        generated_date = self.get_date()
        generated = f"Generated: {generated_date}"
        sub_heading = "Here are your game statistics:"
        data = f"{'Correct answers:':<20} {correct_numbers}\n" \
               f"{'Total questions:':<20} {questions_answered}\n" \
               f"{'Percentage:':<20} {'{:.2f}%'.format((correct_numbers / questions_answered) * 100 if questions_answered != 0 else 0)}\n" \
               f"{'Feedback:':<20} {'Excellent!' if (correct_numbers / questions_answered) * 100 >= 70 else 'Keep Practicing!'}\n" \
               "\nUser Answers:\n"

        for i, answer in enumerate(user_answers, start=1):
            question_number = f"Question {i}:"
            flag_shown = f"Flag Shown: {answer[0]}"
            user_answer = f"User Answer: {answer[1]}"
            result = "Result: Correct" if answer[0] == answer[1] else "Result: Incorrect"
            data += f"{question_number:<20} {flag_shown:<40} {user_answer}\n{result}\n"

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
    root = Tk()
    root.geometry("720x540")
    pygame.mixer.init()
    root.title("Guess The Flag!")

    flags_app = Flags(root)  # Pass start_window as an argument
    flags_app.play_music()  # Call the play method

    root.mainloop()
