from tkinter import *
import pygame
import csv
import random
from PIL import Image, ImageTk

# Loop 20 times to create multiple instances of the Tkinter window
for item in range(0, 20):
    # Create a new Tkinter window
    root = Tk()
    root.geometry("600x400")  # Set the size of the window
    pygame.mixer.init()  # Initialize pygame for audio playback

    # Create a label to display the flag image
    flag_label = Label(root)
    flag_label.grid(row=2)

    # Open the CSV file containing country flags data
    with open("Country_Flags/country_flags.csv", "r", encoding="utf-8") as file:
        # Read the contents of the CSV file and convert them into a list of lists
        # Each inner list represents a row in the CSV file
        var_all_flags = list(csv.reader(file, delimiter=","))
    file.close()  # Close the file after reading its contents

    # Randomly select 4 country flags from the list of all flags
    question_flags = random.sample(var_all_flags, 4)

    # Randomly select one of the 4 flags as the correct answer
    current_correct_answer = random.randint(0, 3)

    # Open the image corresponding to the correct answer flag
    flag_image = Image.open(f"Country_Flags/flag_images/{question_flags[current_correct_answer][3]}")

    # Resize the flag image
    resized_flag_image = flag_image

    # Convert the resized image to a format compatible with Tkinter
    resized_image = ImageTk.PhotoImage(resized_flag_image)

    # Configure the flag label to display the resized image
    flag_label.config(image=resized_image)
    flag_label.image = resized_image

    # Set the title of the Tkinter window
    root.title("Guess The Flag!")

    # Start the Tkinter event loop to display the window
    root.mainloop()
