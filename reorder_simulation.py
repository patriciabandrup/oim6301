# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

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
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *The coffee shop manager would use this analysis to forecast milk demand and determine how much milk to order. It would help them avoid ordering too much milk too early, which can lead to waste, while also reducing the risk of running out and losing sales. By identifying demand patterns, the manager can make purchasing decisions that balance cost efficiency with customer satisfaction.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    *I would need to create a new list that stores the stock carrying over from each day in addition to the starting stock. For each day, I would take the previous day's ending stock, add any new units that arrived, and subtract the units sold that day to get the new ending stock. I would repeat this process every day, updating the running stock, so each day's ending stock becomes the next day's starting stock. I would also need to track each order’s delivery status, since orders take three days to be delivered. This would allow me to add the ordered cartons to the available stock on the correct day. Finally, I would see if daily demand is met by the current stock. If there is not enough stock, there will be a loss of sales because we cannot satisfy those customers.*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*

    *The loop carries the ending stock of milk from one day to the next as the starting stock for the following day, after taking into account the gain of new cartons, and the use of cartons during the day.*


    - *Which check will you use in section 6, and which two numbers should agree?*

    *To check that my numbers are correct I would compare the total cartons received (starting stock plus all deliveries) against the total cartons accounted for (ending stock plus all cartons sold). These two totals should be equal, since every carton that comes in must either be sold or remain in stock.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    starting_stock = 60
    order_quantity = 100
    lead_time_days = 3
    reorder_points = [20, 30, 40, 50]
    daily_demand = [12, 15, 9, 14, 18, 11, 10, 16, 13, 17, 8, 12, 20, 14, 11,
                    9, 15, 13, 16, 12, 10, 14, 19, 11, 13, 15, 9, 12, 17, 14]
    return (
        daily_demand,
        lead_time_days,
        order_quantity,
        reorder_points,
        starting_stock,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(daily_demand, lead_time_days, order_quantity, starting_stock):
    reorder_point = 40
    stock = starting_stock
    pending_orders = []
    daily_table = []

    for day in range(1, 31):
        starting_stock_today = stock
        todays_demand = daily_demand[day - 1]

        arrived = 0
        if day in pending_orders:
            arrived = order_quantity
            stock = stock + arrived
            pending_orders.remove(day)

        sold = min(stock, todays_demand)
        lost = todays_demand - sold
        stock = stock - sold

        units_ordered = 0
        pending_total = len(pending_orders) * order_quantity
        if stock + pending_total <= reorder_point:
            arrival_day = day + lead_time_days
            pending_orders.append(arrival_day)
            units_ordered = order_quantity

        daily_table.append({
            "day": day,
            "starting_stock": starting_stock_today,
            "arrived": arrived,
            "demand": todays_demand,
            "sold": sold,
            "lost": lost,
            "ending_stock": stock,
            "units_ordered": units_ordered,
        })

    daily_table
    return


@app.cell
def _(daily_demand, lead_time_days, order_quantity, starting_stock):
    def run_simulation(reorder_point):
        stock = starting_stock
        pending_orders = []
        daily_table = []

        for day in range(1, 31):
            starting_stock_today = stock
            todays_demand = daily_demand[day - 1]

            arrived = 0
            if day in pending_orders:
                arrived = order_quantity
                stock = stock + arrived
                pending_orders.remove(day)

            sold = min(stock, todays_demand)
            lost = todays_demand - sold
            stock = stock - sold

            units_ordered = 0
            pending_total = len(pending_orders) * order_quantity
            if stock + pending_total <= reorder_point:
                arrival_day = day + lead_time_days
                pending_orders.append(arrival_day)
                units_ordered = order_quantity

            daily_table.append({
                "day": day,
                "starting_stock": starting_stock_today,
                "arrived": arrived,
                "demand": todays_demand,
                "sold": sold,
                "lost": lost,
                "ending_stock": stock,
                "units_ordered": units_ordered,
            })

        return daily_table

    return (run_simulation,)


@app.cell
def _(run_simulation):
    table_40 = run_simulation(40)
    table_40
    return (table_40,)


@app.cell
def _(reorder_points, run_simulation):
    comparison_table = []

    for rp in reorder_points:
        result = run_simulation(rp)

        total_lost = 0
        days_with_lost_sale = 0
        total_orders_placed = 0
        total_ending_stock = 0

        for row in result:
            total_lost = total_lost + row["lost"]
            if row["lost"] > 0:
                days_with_lost_sale = days_with_lost_sale + 1
            if row["units_ordered"] > 0:
                total_orders_placed = total_orders_placed + 1
            total_ending_stock = total_ending_stock + row["ending_stock"]

        average_ending_stock = total_ending_stock / len(result)

        stock_cost = total_ending_stock * 0.5
        delivery_fee = total_orders_placed * 40
        lost_margin_cost = total_lost * 8

        total_cost = stock_cost + delivery_fee + lost_margin_cost

        comparison_table.append({
            "reorder_point": rp,
            "units_lost": total_lost,
            "days_with_lost_sale": days_with_lost_sale,
            "orders_placed": total_orders_placed,
            "average_ending_stock": round(average_ending_stock, 2),
            "total_cost": round(total_cost, 2),
        })

    comparison_table
    return (comparison_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(comparison_table):
    for summary in comparison_table:
        print(f"Reorder point {summary['reorder_point']:3}: "
              f"lost {summary['units_lost']:4}, "
              f"lost-sale days {summary['days_with_lost_sale']:2}, "
              f"orders {summary['orders_placed']:2}, "
              f"avg stock {summary['average_ending_stock']:6.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *I reccomend a reorder point of 40 units to maintain adequate stock levels. When comparing the reorder points, 40 and 50, both with 0 units lost and 0 days with lost sales, the average ending inventory is lower at point 40 than at point 50, resulting in a reduced holding costs.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(starting_stock, table_40):
    final_total_arrived = 0
    final_total_sold = 0
    final_total_lost = 0

    for _row in table_40:
        final_total_arrived = final_total_arrived + _row["arrived"]
        final_total_sold = final_total_sold + _row["sold"]
        final_total_lost = final_total_lost + _row["lost"]

    final_ending_stock = table_40[-1]["ending_stock"]
    # [-1] grabs the last day's row 

    finalCheck_arrived= starting_stock + final_total_arrived
    finalCheck_left = final_total_sold + final_total_lost + final_ending_stock

    finalCheck_arrived, finalCheck_left
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *To check that my numbers were right, I compared the total cartons that came in (starting stock plus all deliveries) against the total cartons accounted for (units sold, units lost, and the final ending stock). Both totals came to 460, confirming the simulation didn't lose or create any cartons.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *One recurring issue with the AI's output was reusing loop-variable names that were already defined in an earlier cell. For example, writing for order in orders: when order was already a loop variable in another cell. Marimo only allows a name to be defined once across the whole notebook, so each time this happened, the cell raised a "multiple-defs" error and had to be renamed before it would run. I caught each of these by running the notebook and reading the exact error message, which named the conflicting cell directly. Although this task was annoying, it helped me keep better track these looping variables interaction throughout the simulation in relation to other created and labeled variables.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _():
    new_reorder_points = list(range(10, 81, 10))
    print(new_reorder_points)
    return (new_reorder_points,)


@app.cell
def _(new_reorder_points, run_simulation):
    cost_table = []

    for new_rp in new_reorder_points:
        _result2 = run_simulation(new_rp)

        _total_lost2 = 0
        _total_orders_placed2 = 0
        _total_ending_stock2 = 0

        for _row2 in _result2:
            _total_lost2 = _total_lost2 + _row2["lost"]
            if _row2["units_ordered"] > 0:
                _total_orders_placed2 = _total_orders_placed2 + 1
            _total_ending_stock2 = _total_ending_stock2 + _row2["ending_stock"]

        _stock_cost2 = _total_ending_stock2 * 0.5
        _delivery_fee2 = _total_orders_placed2 * 40
        _lost_margin_cost2 = _total_lost2 * 8
        _total_cost2 = _stock_cost2 + _delivery_fee2 + _lost_margin_cost2

        cost_table.append({
            "reorder_point": new_rp,
            "total_cost": round(_total_cost2, 2),
        })

    cost_table
    return (cost_table,)


@app.cell
def _(cost_table):
    cheapest = cost_table[0]
    for entry in cost_table:
        if entry["total_cost"] < cheapest["total_cost"]:
            cheapest = entry
    cheapest
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *When I first began adding cost to the simulation, I tried creating new cost variables inside the existing loop by just multiplying stock, orders, and lost units by their respective rates, but this didn't fully capture the cost requirements on its own. My agent suggested building the new cost variables directly within the original loop, using my set reorder point of 40, which gave correct results for one reorder point at a time.*

    *From there, I tried extending the simulation to test the full range of reorder points, but I made a mistake: I accidentally changed the range the simulation used to count days, instead of changing the list of reorder points being tested. My agent caught this, explaining that the simulation always needs to run over the same 30 days regardless of which reorder point is being tested — only the list of reorder points itself should change. Once I corrected that, I was able to set a new list of reorder points from 10 to 80.*

    *This let me compare the original simulation against the new one that accounted for cost across the full range of reorder points. I did have to run the loop again for this wider range, but I didn't need to rebuild the table's structure — I was able to reuse the same function and add new cost calculations (holding cost, delivery fee, and lost-margin cost) for each reorder point in the extended range.*
    """)
    return


if __name__ == "__main__":
    app.run()
