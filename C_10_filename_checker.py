from datetime import date
import re


def make_file(filename):
    """
    Function to create a filename for the quiz results file.

    Parameters:
        filename (str): The proposed filename entered by the user.

    Returns:
        str: The validated and formatted filename for the quiz results file.
    """
    date_part = get_date()

    # Check if filename is empty
    if filename == "":
        # Get date and create default filename
        filename_ok = ""
        filename = f"{date_part}_flagquiz"

    else:
        # Check that filename is valid
        filename_ok = check_filename(filename)

    # If filename is still empty after validation, add default extension
    if filename_ok == "":
        filename += ".txt"

    else:
        # Use validated filename
        filename = filename_ok

    return filename


def get_date():
    """
    Function to get the current date and format it.

    Returns:
        str: The formatted current date.
    """
    today = date.today()
    return today.strftime("%Y_%m_%d")


def check_filename(filename):
    """
    Function to check if a filename contains valid characters.

    Parameters:
        filename (str): The proposed filename entered by the user.

    Returns:
        str: An error message if the filename contains invalid characters, otherwise an empty string.
    """
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


# Test the function with different filenames
test_filenames = ["", "Test.txt", "Test It", "test"]

for item in test_filenames:
    checked = make_file(item)
    print(checked)
    print()
