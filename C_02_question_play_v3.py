import tkinter
from tkinter import *
import pygame
from functools import partial  # To prevent unwanted windows


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
        self.error_label = Label(root, bg="white",
                                 text="                                                                               ")
        if num_questions.isdigit() and int(num_questions) > 0:
            self.to_play(int(num_questions))
            self.question_entry.config(bg="white")
            self.question_entry.delete(0, END)


        else:
            text = "Please enter a valid integer greater than 0."
            self.question_entry.config(bg="#F8CECC")
            self.error_label.config(text=text, font=("Arial", "10"), fg="red", bg="white")
        self.error_label.place(x=243, y=350)

    def to_play(self, num_questions):
        Play(num_questions)  # Create an instance of Play with the entered number of rounds
        root.withdraw()  # Hide root window (i.e., hide rounds choice window).

    def play_music(self):
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)


class Play:
    def __init__(self, how_many):
        self.play_box = Toplevel(width=600, height=400)
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_play))
        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)
        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()
        self.update_round_heading()

        self.start_over_button = Button(self.play_frame,
                                        fg="#FFFFFF",
                                        bg="#808080",
                                        text="Start Over",
                                        width=11, font=("Arial", "12", "bold"),
                                        command=self.close_play)

        self.start_over_button.grid(row=1, padx=5, pady=5, columnspan=5)

    def update_round_heading(self):
        rounds_heading = f"Choose - Question 1 of {self.questions_wanted.get()}"
        self.choose_heading = Label(self.play_frame, text=rounds_heading,
                                    font=("Arial", "16", "bold")
                                    )
        self.choose_heading.grid(row=0)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.geometry("720x540")
    pygame.mixer.init()
    root.title("Guess The Flag!")

    flags_app = Flags(root)  # Pass root as an argument
    flags_app.play_music()  # Call the play method

    root.mainloop()
