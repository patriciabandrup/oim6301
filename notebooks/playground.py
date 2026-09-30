import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


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
