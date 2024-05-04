import csv

with open("Country_Flags/country_flags.csv", "r", encoding="utf-8") as file:
    var_all_flags = list(csv.reader(file, delimiter=","))
file.close()
# buttons for play GUI)
print(var_all_flags)
print("Length: {}".format(len(var_all_flags)))
