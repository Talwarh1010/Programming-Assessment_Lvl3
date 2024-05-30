# List containing results of each question, either 'Correct' or 'Wrong'
result_data = ["Correct", "Wrong", "Correct", "Correct", "Wrong", "Correct",
               "Wrong", "Wrong", "Correct", "Correct"]

# Count the total number of questions answered
questions_answered = len(result_data)

# Count the number of correct answers
correct_numbers = result_data.count('Correct')

# Names of rows in the data table
row_names = ["Correct answers", "Total questions", "Percentage", "Feedback"]

# Calculate the percentage of correct answers
percentage = (correct_numbers / questions_answered) * 100 if questions_answered != 0 else 0

# Generate data values for each row in the data table
data_values = [
    correct_numbers,  # Number of correct answers
    questions_answered,  # Total number of questions
    "{:.2f}%".format(percentage),  # Percentage of correct answers formatted to 2 decimal places
    "Excellent!" if percentage >= 70 else "Keep Practicing!"  # Feedback based on percentage
]

# Print the data values
print(data_values)
