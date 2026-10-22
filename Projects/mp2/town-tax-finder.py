"""Mini Project 2: Town Tax Finder."""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


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
    ## 2. My Plan Before AI

    Before asking your agent anything, open the API address in your browser and read the response. Then describe your solution in at least five lines, in order and in plain words. Answer these questions:

    - Which functions will your tool need? For each function, what goes in and what comes out?
    - Which addresses will the functions request?
    - How will you know you have every record?
    - Which check will you use in section 6, and which two numbers should agree?

    Commit this plan with the message `mp2: plan before AI`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Put every input in one code cell. Changing an input should update the results that depend on it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Put your functions and the code that uses them here. Add cells as needed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    Print your result table with `print` and f-strings, with the columns lined up. Then use an f-string to print one sentence that answers section 1 and includes the numbers from your results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    Reach at least one result a second way in this notebook and show that the two results agree. At least one check must run as code and show both numbers. For example, compare the number of records you collected with the total reported by the API, or check one result against the raw API response in your browser.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    Describe one piece of AI output you did not accept as-is: what it gave you, what you changed, and how you knew. Point to the commit or cell. If the agent got it right the first time, explain how you verified it; the check in section 6 is enough.
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
    ## 10. Time Spent

    Enter about how many hours this project took outside class, as one number. This is not graded.
    """)
    return


if __name__ == "__main__":
    app.run()
