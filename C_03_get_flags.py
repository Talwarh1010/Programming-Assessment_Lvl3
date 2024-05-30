import csv

# Open the CSV file containing country flags data
with open("Country_Flags/country_flags.csv", "r", encoding="utf-8") as file:
    # Read the contents of the CSV file and convert them into a list of lists
    # Each inner list represents a row in the CSV file
    var_all_flags = list(csv.reader(file, delimiter=","))
# Close the file after reading its contents
file.close()
# Print the contents of the list containing flag data
print(var_all_flags)
# Print the length of the list (number of rows in the CSV file)
print("Length: {}".format(len(var_all_flags)))
