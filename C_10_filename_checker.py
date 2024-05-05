from datetime import date
import re


def make_file(filename):
    date_part = get_date()
    if filename == "":
        # Get date and create default filename
        filename_ok = ""
        filename = f"{date_part}_flagquiz"

    else:
        # Check that filename is valid
        filename_ok = check_filename(filename)

    if filename_ok == "":
        filename += ".txt"

    else:
        filename = filename_ok

    return filename


def get_date():
    today = date.today()
    return today.strftime("%Y_%m_%d")


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


test_filenames = ["", "Test.txt", "Test It", "test"]

for item in test_filenames:
    checked = make_file(item)
    print(checked)
    print()
