import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    import marimo as mo
    from datetime import date

    return date, duckdb, mo


@app.cell
def _(date):
    as_of = date(2022, 12, 31)
    return


@app.cell
def _(mo):
    database = mo.notebook_dir() / "database.duckdb"
    return (database,)


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part B: The Questions

    ## The Questions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. How much did each portfolio buy and sell in the last 30 days?

    For each portfolio, show its number of trades, money spent on buys with fees added, and money received from sells with fees taken off.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 1 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Write one sentence with the numbers that answers question 1.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. How many portfolios does each member have, and how much have they bought?

    Include members with no portfolio. Show each member's portfolio count and the total value they bought across their portfolios.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 2 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Write one sentence with the numbers that answers question 2.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. What does each portfolio hold on the as_of date?

    For each portfolio and asset, calculate units bought minus units sold, keeping only holdings above zero.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 3 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Write one sentence with the numbers that answers question 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4. How did trade prices compare with closing prices over the last 90 days?

    For every trade in that period, show the closing price on the trade date and the trade price's percentage difference from it.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 4 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Write one sentence with the numbers that answers question 4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. Which assets have never been traded?

    List the assets the club follows that no portfolio has ever traded.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 5 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Write one sentence with the numbers that answers question 5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6. What was the total value traded for the asset whose ticker changed?

    Count its value traded over the year under both tickers together.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 6 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Write one sentence with the numbers that answers question 6.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7. Did every trade have a closing price for its asset on that date?

    Check every trade against this rule and identify any trades that break it. This question checks a rule.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 7 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Name any trades that break the rule, or explain the database's refusal if it prevents such a row.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8. Did any portfolio sell more of an asset than it held?

    Check every sell against this rule and identify any sells that break it. This question checks a rule.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 8 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Name the trades that break the rule, or explain the database's refusal if it prevents such a row.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9. Your manager question

    Write an original question a manager of the investment club would ask. It must not repeat the logic of one of questions 1-8.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 9 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Write one sentence with the numbers that answers question 9.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 10. Your second manager question

    Write another original manager question that uses different logic from questions 1-9.
    """)
    return


@app.cell
def _():
    # Write the SQL query for question 10 here. Leave its result as the cell's last expression.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Write one sentence with the numbers that answers question 10.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right

    Reach at least two answers a second way and show that the results agree. At least one check must run as code, show both numbers, and fail if they do not agree.
    """)
    return


@app.cell
def _():
    # Add a code check here. At least one check must compare two numbers and fail if they disagree.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **How I checked:** Explain which answers you checked a second way and whether the results agreed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent

    Pick one piece of AI output you did not accept as-is. Say what it gave you, what you changed, and how you knew. Point to the commit or cell. If the agent got it right the first time, explain how you verified it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **My response:** Write your explanation here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back

    Choose one question above that uses at least three tables. Before answering any questions, write your predicted number of joined rows before grouping and why. Commit that prediction as `db: prediction`. Keep this section here after the answers. Later, run the joins alone, count the rows, compare the result with your prediction, and explain what one row of the final result means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Question chosen and prediction:**
    What does each portfolio hold on the as_of date?
    predict the pre-grouping join row count, and explain your reasoning. Commit this before answering the questions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I chose Question 3: “What does each portfolio hold on the as_of date?” This question joins trades to portfolios and assets. Before grouping, each trade should match one portfolio and one asset, so the joins should produce one row per trade. Part A generated 502 trades, so I predict the joins will produce 502 rows. In the final grouped result, one row represents one portfolio’s positive holding in one asset on the as_of date.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Comparison and meaning:** Say whether the actual count matched your prediction, explain why, and describe what one row of the final result means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Going Further

    Try at least one thing beyond the 10 questions. It does not have to work. Describe what you tried, what you found, and where it is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **My response:** Describe your extra attempt and where to find it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Time Spent

    About how many hours did the whole project take you outside class? This is not graded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Hours:** Write one number.
    """)
    return


if __name__ == "__main__":
    app.run()
