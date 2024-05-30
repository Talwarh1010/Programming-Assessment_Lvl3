from tkinter import *
import pygame


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

        # Button to start the game
        self.start_button = Button(root, font=("Arial", "18"), width=21, text="Start!",
                                   command=self.validate_and_start)  # Updated command to call validation function
        self.background_canvas.create_window(369, 395, window=self.start_button)

    def validate_and_start(self):
        # Get number of questions user wants and print it out. (question validation function will be created later)
        num_questions = self.question_entry.get()
        print(f"You chose to play {num_questions} questions")

    def play_music(self):
        # Play background music
        pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
        pygame.mixer.music.play(loops=100)


if __name__ == "__main__":
    root = Tk()
    # Adjust size of tk window
    root.geometry("720x540")
    # Initialize pygame mixer
    pygame.mixer.init()
    # Create title for flag window
    root.title("Guess The Flag!")
    # Use flag window
    flags_app = Flags(root)
    # Start playing background music
    flags_app.play_music()
    root.mainloop()
