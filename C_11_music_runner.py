from tkinter import *
import pygame


def play_music():
    """
    Function to play background music for the game.

    This function loads the music file and plays it in a loop.

    """
    pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
    pygame.mixer.music.play(loops=100)


if __name__ == "__main__":
    # Initialize Tkinter window
    root = Tk()
    root.geometry("720x540")
    root.title("Guess The Flag!")

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Call the function to play music
    play_music()

    # Start the Tkinter event loop
    root.mainloop()
