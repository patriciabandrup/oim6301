# import random

# print(random.randint(1,6))

import bmi

# == mean equality = means assignment
# result = bmi.compute_bmi(70, 1.75)
# print(f'Your BMI is {result:.2f}.')

people = [
    {"name": "Alice", "weight": 70, "height": 1.75},
    {"name": "Bob", "weight": 80, "height": 1.80},
    {"name": "Charlie", "weight": 65, "height": 1.70},
    {"name": "Dana", "weight": 72, "height": 1.68},
    {"name": "Ethan", "weight": 85, "height": 1.82},
    {"name": "Fiona", "weight": 58, "height": 1.65}
]
for Bob in people: 
    weight = Bob["weight"]
    height = Bob["height"]
    bmi_value = bmi.compute_bmi(weight, height)
    category = bmi.classify_bmi(bmi_value)
    print(f'{Bob["name"]} has a BMI of {bmi_value:.2f} and is classified as {category}.')


