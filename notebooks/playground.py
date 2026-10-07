import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    # Review of Session 5
    # Dictionaries take {}
    # Lists take []
    # Q1
    orders = [
        {"OrderID": 10248, "ShipCountry": "France"},
        {"OrderID": 10249, "ShipCountry": "Germany"},
    ]
    type(orders)
    return (orders,)


@app.cell
def _(orders):
    orders[0]["ShipCountry"]
    return


@app.cell
def _(orders):
    # orders["ShipCountry"] --> Key Error 
    orders[1]["OrderID"]
    return


@app.cell
def _():
    #countries = []
    #for order in orders: 
        # print (type(order))
    #    print(order{'OrderID'}, order({'Shipcountry'})
    #         countries.append
    return


@app.cell
def _():
    bmi = 27
    if bmi >= 18.5:
        category = "Normal"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 30:
        category = "Obese"
    else:
        category = "Underweight"

    print(category)
    # prints normal because the first matching condition is checked first, after it satisfies the first condition, it skips the rest. 
    return


@app.cell
def _():
    # data[1]{'models'}[0]{'name'} --> Sonnet 5 (Babason)
    # Nested Example: list inside of dictionary
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    charge = 10 
    return (charge,)


@app.cell
def _(charge):
    print(charge)
    return


@app.cell
def _():
    total = 90 

    discount = 0

    if total >= 100:
        discount = 0.05
    elif total >= 200:
        discount = 0.10

    discount
    return


@app.cell
def _():
    total_ = 0
    for charge in [10, 20, 30]:
        total_ = total_ + charge
    print(total_)
    return (charge,)


@app.cell
def _():
    max(["9.50","16.75","22.25"])
    # it does this because "9" is greater than "1" and "2"
    return


@app.cell
def _():
    ord("v")
    return


@app.cell
def _():
    order_lines = ["notebook", "pen"]
    order_lines.append(["stapler", "tape"])
    order_lines
    return


@app.cell
def _():
    labels = []
    for score in [95, 72, 55]:
        if score >= 90:
            labels.append("A")
        elif score >= 60:
            labels.append("Pass")
        else:
            labels.append("Fail")
    print(labels)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
