from tkinter import *
import pygame
from functools import partial  # To prevent unwanted windows


class Flags:
    def __init__(self):
        self.to_play(5)

    def to_play(self, num_questions):
        Play(5)  # Create an instance of Play with the entered number of rounds
        root.withdraw()  # Hide root window (i.e., hide rounds choice window).

    def play_music(self):
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)


class Play:
    def __init__(self, how_many):
        self.play_box = Toplevel(width=600, height=400)

        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

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

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats":
            pass
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
                                        font=("Arial", "14", "bold"), wrap=300)
        self.help_heading_label.grid(row=0)
        help_text = ("""You'll be presented with a flag and four country options; select the country you believe 
matches the flag. Earn a point for each correct answer, displayed as 'Answers Correct / Questions Answered'. 
Remember to see the clue which is the capital of the country flag given!\nClick 'Statistics' to track your 
overall performance and export it as a text file. The game ends after answering all questions, and you can 
proceed to the next question by clicking 'Next Question'.\nHave fun testing your flag knowledge!" Good luck! 
Choose carefully.""")

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wrap=350,
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


if __name__ == "__main__":
    root = Tk()
    root.title("Guess The Flag!")
    Play(5)  # Pass root as an argument

    root.mainloop()
