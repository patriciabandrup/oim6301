"""Mini Project 2: Town Tax Finder."""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import csv

    import altair as alt
    import polars as pl
    import requests

    return alt, pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Town Tax Finder
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    Who would use this tool, and what decision would it help them make? Answer in two or three sentences, using words somebody outside this course would understand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *In this case, a couple looking for an "affordable" ($700,000) single family house in Middlesex county would use this tool. If we scaled the tool to expand our search to other counties or price ranges, we could easily adjust the input parameters so other potential homebuyers could use it. Through this tool, the couple can make informed decisions on which towns to focus their home search on, based on reported average home prices and the property tax bills that come along with homeownership, allowing them to move forward in the home search process knowing they have accounted for both the upfront cost of the home and the ongoing expenses associated with property taxes.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    Before asking your agent anything, open the API address in your browser and read the response. Then describe your solution in at least five lines, in order and in plain words. Answer these questions:

    - Which functions will your tool need? For each function, what goes in and what comes out?
    - Which addresses will the functions request?
    - How will you know you have every record?
    - Which check will you use in section 6, and which two numbers should agree?

    Commit this plan with the message `mp2: plan before AI`.
    """)
    return


@app.cell
def _(requests):
    ma_endpoints = requests.get("https://oim.zhili.dev/ma", timeout=10).json()
    ma_endpoints 
    return


@app.cell
def _(mo):
    mo.md(r"""
    *First I will call the API's Massachusetts endpoints, which gives current, updated data. I will then write a .get function  to request and return every town in a given county -- even though we are specifically looking at Middlesex. Next, I will write a .get function with dor_code and fiscal_year parameters to request the API for that fiscal year and return the towns' figures for the year. I will then write a function that checks each town's year data and keeps only the towns whose average single-family home value is no larger than the budget (\$700,000) and whose average bill is below the tax limit (\$8,000), returning the town name, home value, and the residential tax bill. I will sort those towns by average single family value, lowest to highest. I will print the results as a table, then print one sentence naming the towns that passed the filter. To make sure my numbers are right I will check that the number of towns collected for Middlesex matches pagination.total from the API response before filtering, so I can confirm no towns were dropped.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Put every input in one code cell. Changing an input should update the results that depend on it.
    """)
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Put your functions and the code that uses them here. Add cells as needed.
    """)
    return


@app.cell
def _(county, requests):
    def get_towns(county):
        reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "per_page": 100},
            timeout=10,
        )
        return reply.json()

    towns_reply = get_towns(county)
    middlesex_towns = towns_reply["items"]
    towns_total = towns_reply["pagination"]["total"]
    len(middlesex_towns), towns_total
    return middlesex_towns, towns_total


@app.cell
def _(requests):
    def get_town_history(dor_code, fiscal_year):
        reply = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
            params={"from_year": fiscal_year, "to_year": fiscal_year},
            timeout=10,
        )
        return reply.json()

    return (get_town_history,)


@app.cell
def _(fiscal_year, get_town_history, middlesex_towns):
    town_year_records = []
    missing_count = 0
    for _town in middlesex_towns:
        _history = get_town_history(_town["dor_code"], fiscal_year)
        _year_data = None
        for _year in _history["years"]:
            if _year["fiscal_year"] == fiscal_year:
                _year_data = _year
        if _year_data is None:
            missing_count = missing_count + 1
        else:
            town_year_records.append({
                "name": _town["name"],
                "average_single_family_value_dollars": _year_data["average_single_family_value_dollars"],
                "residential_rate_per_thousand": _year_data["residential_rate_per_thousand"],
                "average_single_family_bill_dollars": _year_data["average_single_family_bill_dollars"],
            })

    len(town_year_records), missing_count
    return (town_year_records,)


@app.cell
def _(budget_dollars, tax_limit_dollars, town_year_records):
    affordable_towns = []
    for _record in town_year_records:
        _fits_budget = _record["average_single_family_value_dollars"] <= budget_dollars
        _fits_tax_limit = _record["average_single_family_bill_dollars"] < tax_limit_dollars
        if _fits_budget and _fits_tax_limit:
            affordable_towns.append(_record)

    def get_total(end_record):
        return end_record["average_single_family_bill_dollars"]
    affordable_towns = sorted(affordable_towns, key=get_total)

    len(affordable_towns)
    return (affordable_towns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    Print your result table with `print` and f-strings, with the columns lined up. Then use an f-string to print one sentence that answers section 1 and includes the numbers from your results.
    """)
    return


@app.cell
def _(affordable_towns):
    print(f"{'Town':<15}{'Home Value':>15}{'Tax Rate':>12}{'Avg Bill':>12}")
    for _r in affordable_towns:
        print(f"{_r['name']:<15}{_r['average_single_family_value_dollars']:>15,}{_r['residential_rate_per_thousand']:>12}{_r['average_single_family_bill_dollars']:>12,}")
    return


@app.cell
def _(
    affordable_towns,
    budget_dollars,
    county,
    tax_limit_dollars,
    towns_total,
):
    _town_names = []
    for _r in affordable_towns:
        _town_names.append(_r["name"])
    _names_text = ", ".join(_town_names)
    print(f"For a budget of ${budget_dollars:,} and a tax limit of ${tax_limit_dollars:,}, {len(affordable_towns)} of {towns_total} towns in {county} County qualify, cheapest bill first: {_names_text}.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    Reach at least one result a second way in this notebook and show that the two results agree. At least one check must run as code and show both numbers. For example, compare the number of records you collected with the total reported by the API, or check one result against the raw API response in your browser.
    """)
    return


@app.cell
def _(affordable_towns, pl):
    affordable_table = pl.DataFrame(affordable_towns)
    affordable_table.sort("average_single_family_bill_dollars")
    return


@app.cell
def _(town_year_records, towns_total):
    len(town_year_records), towns_total
    return


@app.cell
def _(county, requests, town_year_records):
    _check_reply = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": county, "per_page": 100},
        timeout=10,
    )
    _api_total = _check_reply.json()["pagination"]["total"]

    len(town_year_records), _api_total
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    Describe one piece of AI output you did not accept as-is: what it gave you, what you changed, and how you knew. Point to the commit or cell. If the agent got it right the first time, explain how you verified it; the check in section 6 is enough.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    *When I was trying to sort the new set of towns that passed our filters, which we had labeled `affordable_towns`, I needed to first show the towns starting from the smallest `average_single_family_bill_dollars`. When my agent edited my code, it gave me a return using `lambda town: town["average_single_family_bill_dollars"]`. Trying to understand the term "lambda," I learned it is a shorthand, unnamed function for calling every record and returning the number to sort by. This is similar to writing `def get_total():`, a more familiar line of syntax. I switched the code to use `def` instead, and redid that section myself, because I was able to track and see each element of the code I used, and could easily trace back my steps and function names.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back

    Pick two functions the agent wrote or helped write. For each, explain in your own words what goes in, what comes out, and one line you had to ask about.

    Choose one change to what the tool does, such as another town or another rule. You can change one value in your Inputs cell. Write what you expect to change, commit with the message `mp2: prediction`, make the change, run the notebook, and record what happened and whether it matched your prediction.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    1. When converting my affordable housing table from Python to Polars, I initially used pl.read_csv(town_year_records) because I thought I needed to upload a CSV file. However, pl.read_csv is used for actual CSV files or CSV-formatted text, while what I had made as town_year_records is a list of dictionaries could be used. Since my data was already written in Python, I should use pl.DataFrame, which converts the list of records directly into a table.This works because pl.DataFrame is designed to turn a list of dictionaries into a table, with the dictionary keys becoming column names. pl.read_csv would only be appropriate if I were reading an actual CSV file.
    2. When setting up my initial empty lists for town-year records, my agent also created a running total called missing_count. I was confused about why we needed a separate count instead of a list to track missing town-year combinations. After asking my agent, I learned that missing_count is a simple tally of how many records are missing or incomplete, without storing the records themselves. A list would store each missing record for later inspection. Since I only needed to know how many were missing, a counter was more efficient. This helped me understand that counters are useful for tracking quantities, while lists are better when I need to retain the actual data.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **Input Change Prediction:**

    By changing the input value of `budget_dollars` from 700000 to 500000, I would expect that fewer towns would have an `average_single_family_value_dollars` that falls under this lower budget, and the couple would have fewer towns as options to live in.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **Input Change Reflection:**

    After changing budget_dollars from $700,000 to $500,000, the number of affordable towns in Middlesex County dropped from 12 to only 4. This matches my prediction: lowering the budget made the filter stricter, so fewer towns' average home values fell under the new, lower limit, leaving the couple with fewer options.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    Describe what you tried beyond the main task, what you found, and where it appears in the notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Rank the same towns by tax rate in place of the bill. Does the order change, and why?
    """)
    return


@app.cell
def _(affordable_towns, pl):
    affordable_tax_table = pl.DataFrame(affordable_towns)
    affordable_tax_table.sort("residential_rate_per_thousand")
    return (affordable_tax_table,)


@app.cell
def _(affordable_tax_table, alt):
    affordable_tax_chart = alt.Chart(affordable_tax_table).mark_bar().encode(
        x=alt.X("residential_rate_per_thousand", title="Tax Rate"),
        y=alt.Y("name", sort="x", title="Town"),
        tooltip=["name", "average_single_family_value_dollars", "residential_rate_per_thousand", "average_single_family_bill_dollars"],
    ).properties(
        title="Affordable Middlesex Towns, Lowest Rate First",
        width=500,
        height=300,
    )
    affordable_tax_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In sorting the towns by their tax rate (`residential_rate_per_thousand`), we see a shift in the chart. Initially, when they were sorted and ranked by cheapest bill (`average_single_family_bill_dollars`), we valued the impact of the amount of money spent per year on property taxes. By looking at towns in terms of their tax rate, we can see which towns impose a higher tax burden despite the value of the property. For example, Ashby was in the middle of the first list in regards to having the cheapest bill; however, now it is at the very bottom of the list with a 15.76 tax rate per thousand dollars, making it one of the towns with the highest tax burden relative to property values. When we only looked at the bill in dollars, we didn't necessarily put too much importance on this, since `average_single_family_value_dollars` was low and offset that high rate. This matters because the value of a house can appreciate over time, while the tax rate stays relatively high, meaning residents in these towns may face a growing tax burden even if their initial bill seemed low or moderate compared to other towns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent

    Enter about how many hours this project took outside class, as one number. This is not graded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4.5 hours
    """)
    return


if __name__ == "__main__":
    app.run()
