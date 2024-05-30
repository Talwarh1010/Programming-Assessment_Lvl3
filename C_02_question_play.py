import tkinter
from tkinter import *
import pygame
from functools import partial  # To prevent unwanted windows


class Flags:
    def __init__(self, root):
        # Load background image
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

        # Entry field for entering the number of questions
        self.question_entry = Entry(root, font=("Arial", "20"))
        self.background_canvas.create_window(365, 330, window=self.question_entry)

        # Button to start the quiz
        self.start_button = Button(root, font=("Arial", "18"), width=21, text="Start!",
                                   command=self.validate_and_start)  # Updated command to call validation function
        self.background_canvas.create_window(369, 395, window=self.start_button)

        # Label to display error messages
        self.error_label = Label(root, bg="white", text=" " * 79)

    def validate_and_start(self):
        # Validate the number of questions entered and start the game
        num_questions = self.question_entry.get()

        try:
            num_questions = int(num_questions)
            if num_questions > 0:
                self.to_play(num_questions)
                self.question_entry.delete(0, END)
            else:
                text = "Please enter an integer greater than 0."
                self.display_error(text)
        except ValueError:
            text = "Please enter a valid integer greater than 0."
            self.display_error(text)

    def to_play(self, num_questions):
        Play(num_questions)  # Create an instance of Play with the entered number of questions
        root.withdraw()  # Hide the main window (i.e., hide the questions entry window).

    def play_music(self):
        # Play background music
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)

    def display_error(self, text):
        # Display error message
        self.error_label.config(text=text, font=("Arial", "10"), fg="red", bg="white")
        self.error_label.place(x=243, y=350)


class Play:
    def __init__(self, how_many):
        # Create a new window for playing the game
        self.play_box = Toplevel(width=600, height=400)
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_play))

        # Initialize the number of questions to be played
        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)

        # Create the main frame for the game window
        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

        # Button to start over the game
        self.start_over_button = Button(self.play_frame,
                                        fg="#FFFFFF",
                                        bg="#808080",
                                        text="Start Over",
                                        width=11, font=("Arial", "12", "bold"),
                                        command=self.close_play)
        self.start_over_button.grid(row=1, padx=5, pady=5, columnspan=5)

    def update_round_heading(self):
        # Update the heading to show the current question number
        rounds_heading = f"Choose - Question 1 of {self.questions_wanted.get()}"
        self.choose_heading = Label(self.play_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

    def close_play(self):
        # Close the play window and show the main window again
        root.deiconify()
        self.play_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.geometry("720x540")
    # Initialize pygame mixer
    pygame.mixer.init()
    root.title("Guess The Flag!")
    # Create instance of Flags class
    flags_app = Flags(root)
    # Start playing background music
    flags_app.play_music()
    root.mainloop()
