
result_data = ["Correct", "Wrong", "Correct", "Correct", "Wrong", "Correct",
               "Wrong", "Wrong", "Correct", "Correct"]

questions_answered = len(result_data)
correct_numbers = result_data.count('Correct')

row_names = ["Correct answers", "Total questions", "Percentage", "Feedback"]
data_values = [correct_numbers, questions_answered,
               "{:.2f}%".format(
                   (correct_numbers / questions_answered) * 100 if questions_answered != 0 else 0),
               "Excellent!" if (correct_numbers / questions_answered) * 100 >= 70 else "Keep Practicing!"]
print(data_values)