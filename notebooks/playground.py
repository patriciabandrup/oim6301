import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Review of Session 5
    """)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Beginning of Session 6 Notes (10/14)
    """)
    return


@app.cell
def _():
    # reply = {
    #    "count": 2,
    #    "data": [
    #       {"name": "Carla", "city": "Boston", "age": 34},
    #         {"name": "Hiro", "city": "Austin", "age": 29},
    #     ],
    # }
    # len(reply["data"][0])

    # type(reply) --> dictionary 
    # len(reply["data"][0]) --> 3 because there are 3 key-value pairs (name, city, age)

    # How do you get Boston?
    # reply['data][0]['city'] --> Boston

    # how to find by name 
    # for row in data:
    #     if row['name'] =='Ethan':
    #         print(f'Found {row['name]}, {row['city']}, {row['age']}")
    return


app._unparsable_cell(
    r"""
    # bmi = 27
    # if bmi >= 30:
    #     category = "Obese"
    # elif bmi >= 25:
    #     category = "Overweight"
    # elif bmi >= 18.5:
    #     category = "Normal"
    # else:
    #     category = "Underweight"
    # print(category)

    # How to create a list + loop for many numbers, rather than just 27: 

    patients = [20,25,16,30]

    # wrap the folling to a function 
    for bmi in patients: 
        if bmi >= 30: 
            category = "Overweight"
        elif bmi >= 18.5:
            category = "Normal"
        else:
            category = "Underweight"
     print(category)
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 5 (interesting codes)
    """)
    return


@app.cell
def _():
    # BEGINNING OF SETUP 
    import csv

    import altair as alt
    import polars as pl
    import requests

    return alt, csv, pl, requests


@app.cell
def _(requests):
    ma_counties = requests.get("https://oim.zhili.dev/ma/counties", timeout=10).json()
    ma_counties[0], len(ma_counties)
    return (ma_counties,)


@app.cell
def _(requests):
    def get_towns(county):
        towns_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "per_page": 100},
            timeout=10,
        )
        return towns_reply.json()["items"]

    return (get_towns,)


@app.cell
def _(get_towns, ma_counties):
    ma_towns = []
    for _county in ma_counties:
        for _town in get_towns(_county["name"]):
            ma_towns.append(_town)
    len(ma_towns)
    return (ma_towns,)


@app.cell
def _(csv, ma_towns, mo):
    csv_columns = [
        "name",
        "county",
        "population",
        "income_per_capita_dollars",
        "average_single_family_value_dollars",
        "average_single_family_bill_dollars",
    ]

    ma_towns_csv = mo.notebook_dir().parent / "data" / "ma-towns.csv"
    ma_towns_csv.parent.mkdir(exist_ok=True)

    with open(ma_towns_csv, "w", newline="", encoding="utf-8") as _file:
        _writer = csv.DictWriter(_file, fieldnames=csv_columns, extrasaction="ignore") #each row is a dictionary
        _writer.writeheader()
        _writer.writerows(ma_towns)

    ma_towns_csv.name
    return (ma_towns_csv,)


@app.cell
def _(ma_towns_csv, pl):
    town_table = pl.read_csv(ma_towns_csv)
    town_table
    return (town_table,)


@app.cell
def _(town_table):
    # Which 
    higest_income = (
        town_table.sort("income_per_capita_dollars", descending=True)
        .head(10)
        .select("name", "county", "income_per_capita_dollars")
    )
    higest_income
    return (higest_income,)


@app.cell
def _(alt, higest_income, mo):
    higest_income_chart = mo.ui.altair_chart(
        higest_income.plot.bar(
            y=alt.Y("name", sort="-x", title="Town"),
            x=alt.X("income_per_capita_dollars", title="Income per capita (dollars)"),
            color=alt.Color("county", title="County"),
            tooltip=["name", "county", "income_per_capita_dollars"],
        ).properties(title="The 10 Massachusetts towns with the highest income per capita")
    )
    higest_income_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # THIS CODE MAKES THE CHART LOOK GOOD!!
    # color=alt.Color("county", title="County"),
    #        tooltip=["name", "county", "income_per_capita_dollars"],
    """)
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

    return (mo,)


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
