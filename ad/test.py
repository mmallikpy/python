
from lib2to3.pgen2.token import NEWLINE
import random
import csv
import time

data = open("Final_CSV/Finl_Data_EightyNine.csv", "r", encoding="UTF-8")
password = open("Final_CSV/Finl_Data_EightyNine_Pass.csv", "a+", newline='')

digit = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
]
lowerCase = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
upperCase = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

special_char = ["@", "#", "%", "^", "!"]
for x in data:
    user_data = x.split(",")
    pass_list = ""
    counter = 0
    while counter < 3:
        upper_output = random.choice(upperCase)
        digit_output = random.choice(digit)
        lower_output = random.choice(lowerCase)
        special_output = random.choice(special_char)

        upper_output = str(upper_output)
        digit_output = str(digit_output)
        lower_output = str(lower_output)
        special_output = str(special_output)

        pass_list += upper_output
        pass_list += digit_output
        pass_list += lower_output
        pass_list += special_output
        counter += 1
    val = (pass_list, user_data[1], user_data[2].replace("\n", ""))
    print(val)

    writeCsv = csv.writer(password)
    writeCsv.writerow(val)

print("Password create done...............!!")