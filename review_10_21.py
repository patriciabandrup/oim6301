import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    def compute_bmi(height, weight):
        # height = float(input("Height in meters: "))
        # weight = float(input("Weight in kilograms: "))
        return weight / height ** 2
    
    compute_bmi(1.75, 70) # supposed to get the result immediately BUT WE NEED TO SUPPLY AGAIN 
    # when we comment out height and weight section because then this runs before compute_bmi(1.75, 70)
    return


@app.cell
def _():
    people = [
        {"name": "Carla", "bmi": 27.1},
        {"name": "Hiro", "bmi": 22.4},
    ]
    # {} is a dictionary 
    for person in people:
        print(person) # --> {'name': 'Carla', 'bmi': 27.1} I WAS CORRECT!!!
    return


@app.cell
def _():
    # What is abstraction? 
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
