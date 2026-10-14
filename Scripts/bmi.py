bmi_value = 18

# wrap the code in a function 

def classify_bmi(bmi):
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"
    # print(category)
    return category
# bmi in this function is created when the function is created 

# moving bmi-value to be after the function is ok because it is not defined in the function 

classify_bmi(bmi_value)
# this bmi in () refers to bmi = 27 --> line 1

result = classify_bmi(bmi_value)
print(f'Your category is {result}.')

#compute bmi with weight and height
def compute_bmi(weight, height): 
    bmi = weight / (height ** 2)
    return bmi

def classify_bmi(bmi):
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"
    # print(category)
    return category

def main():
    weight_kg = float(input("Enter weight in kg: "))
    height_m = float(input("Enter height in meters: "))
    bmi_value = compute_bmi(weight_kg, height_m)
    result = classify_bmi(bmi_value)
    print(f'Your BMI is {bmi_value:.2f} and your category is {result}.')

main()
if __name__ == "__main__":
    main()