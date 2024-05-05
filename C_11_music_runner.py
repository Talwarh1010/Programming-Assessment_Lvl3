import tkinter
from tkinter import *
import pygame
from functools import partial  # To prevent unwanted windows
import csv
import random
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import date
import re


def play_music():
    pygame.mixer.music.load("2 (online-audio-converter.com).mp3")
    pygame.mixer.music.play(loops=100)


if __name__ == "__main__":
    root = Tk()
    root.geometry("720x540")
    pygame.mixer.init()
    root.title("Guess The Flag!")

    play_music()  # Call the play method

    root.mainloop()
