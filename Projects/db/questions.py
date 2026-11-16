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
    return (as_of,)


@app.cell
def _(mo):
    database = mo.notebook_dir() / "database.duckdb"
    return (database,)


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


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
def _(as_of, ask):
    ask(f"""
        SELECT
            p.portfolio_id,
            p.portfolio_name,
            count(t.trade_id) AS trade_count,
            sum(CASE WHEN t.trade_side = 'BUY'  THEN 1 ELSE 0 END) AS buy_count,
            sum(CASE WHEN t.trade_side = 'SELL' THEN 1 ELSE 0 END) AS sell_count,
            sum(CASE WHEN t.trade_side = 'BUY'  THEN t.quantity * t.price_per_unit + t.fee ELSE 0 END) AS total_bought,
            sum(CASE WHEN t.trade_side = 'SELL' THEN t.quantity * t.price_per_unit - t.fee ELSE 0 END) AS total_sold
        FROM portfolios AS p
        LEFT JOIN trades AS t
            ON t.portfolio_id = p.portfolio_id
            AND t.trade_date > DATE '{as_of}' - INTERVAL 30 DAY
            AND t.trade_date <= DATE '{as_of}'
        GROUP BY p.portfolio_id, p.portfolio_name
        ORDER BY trade_count DESC 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Here we see each portfolio's activity during the 30 days ending December 31, 2022. The table shows the number of trades, buys, and sells, along with the money spent on buys, including fees, and received from sells after fees. I ordered the portfolios from most active to least active. Portfolio 4 was the most active, with 7 trades.
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
def _(ask):
    ask(f"""
        SELECT
            m.member_id,
            m.last_name,
            count(DISTINCT p.portfolio_id) AS portfolio_count,
            sum(CASE WHEN t.trade_side = 'BUY' THEN t.quantity * t.price_per_unit + t.fee ELSE 0 END) AS total_bought
        FROM members AS m
        LEFT JOIN portfolios AS p
            ON p.member_id = m.member_id
        LEFT JOIN trades AS t
            ON t.portfolio_id = p.portfolio_id
        GROUP BY m.member_id, m.last_name
        ORDER BY m.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** The table shows the portfolio count for all 15 members of the club. Each has at most 2 portfolios, and 2 members have no portfolio at all. Among members with a portfolio, the total amount bought varies widely, from about $1.1 million up to about $4.1 million.
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
def _(as_of, ask):
    ask(f"""
        SELECT
            p.portfolio_id,
            p.portfolio_name,
            a.asset_id,
            a.asset_name,
            sum(CASE
                WHEN t.trade_side = 'BUY' THEN t.quantity
                WHEN t.trade_side = 'SELL' THEN -t.quantity
                ELSE 0
            END) AS units_held
        FROM portfolios AS p
        JOIN trades AS t
            ON t.portfolio_id = p.portfolio_id
            AND t.trade_date <= DATE '{as_of}'
        JOIN assets AS a
            ON a.asset_id = t.asset_id
        GROUP BY p.portfolio_id, p.portfolio_name, a.asset_id, a.asset_name
        HAVING sum(CASE
                WHEN t.trade_side = 'BUY' THEN t.quantity
                WHEN t.trade_side = 'SELL' THEN -t.quantity
                ELSE 0
            END) > 0
        ORDER BY p.portfolio_id, a.asset_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** As of December 31, 2022, the table shows 167 rows, one for each portfolio's positive holding in a given asset, with the units held for that asset. For example, Portfolio 1 held 28 units of Microsoft and 48 units of NVIDIA.
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
def _(as_of, ask):
    ask(f"""
        SELECT
            t.trade_id,
            t.trade_date,
            t.asset_id,
            t.trade_side,
            t.price_per_unit AS trade_price,
            cp.close_price,
            round((t.price_per_unit - cp.close_price) / cp.close_price * 100, 2) AS pct_diff_from_close
        FROM trades AS t
        JOIN closing_prices AS cp
            ON cp.asset_id = t.asset_id
            AND cp.price_date = t.trade_date
        WHERE t.trade_date > DATE '{as_of}' - INTERVAL 90 DAY
            AND t.trade_date <= DATE '{as_of}'
        ORDER BY t.trade_date, t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Over the 90 days ending December 31, 2022, 127 trades matched to a closing price on their trade date, and all 127 traded at exactly the closing price (0% average difference).
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
def _(ask):
    ask(f"""
        SELECT
            a.asset_id,
            a.asset_name
        FROM assets AS a
        LEFT JOIN trades AS t
            ON t.asset_id = a.asset_id
        WHERE t.trade_id IS NULL
        ORDER BY a.asset_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** The table has 0 rows, so every asset the club follows has been traded at least once; no asset has never been traded.
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
def _(ask):
    ask(f"""
        SELECT
            a.asset_id,
            a.asset_name,
            count(t.trade_id) AS trade_count,
            sum(t.quantity * t.price_per_unit) AS total_value_traded
        FROM assets AS a
        JOIN trades AS t
            ON t.asset_id = a.asset_id
        WHERE a.asset_id IN (
            SELECT asset_id
            FROM asset_tickers
            GROUP BY asset_id
            HAVING count(*) > 1
        )
            AND t.trade_date >= DATE '2022-01-01'
            AND t.trade_date <= DATE '2022-12-31'
        GROUP BY a.asset_id, a.asset_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** The asset whose ticker changed is asset_id 9, Meta Platforms. It had 46 trades in 2022, totaling $198,719.56 in value traded across both tickers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7. Did every trade have a closing price for its asset on that date?

    Every trade checked against the rule that it happens on a day its asset has a closing price, and a list of any that break it.
    """)
    return


@app.cell
def _(ask):
    ask(f"""
        SELECT
            t.trade_id,
            t.trade_date,
            t.asset_id,
            t.trade_side,
            t.price_per_unit AS trade_price
        FROM trades AS t
        LEFT JOIN closing_prices AS cp
            ON cp.asset_id = t.asset_id
            AND cp.price_date = t.trade_date
        WHERE cp.asset_id IS NULL
        ORDER BY t.trade_date, t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** The table has 0 rows, so every trade broke no rule: every trade's asset had a closing price recorded on that same trade date.
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
def _(ask):
    ask(f"""
        WITH signed_trades AS (
            SELECT
                t.trade_id,
                t.trade_date,
                t.portfolio_id,
                t.asset_id,
                t.trade_side,
                t.quantity,
                CASE WHEN t.trade_side = 'BUY' THEN t.quantity ELSE -t.quantity END AS signed_quantity
            FROM trades AS t
        ),
        running AS (
            SELECT
                *,
                sum(signed_quantity) OVER (
                    PARTITION BY portfolio_id, asset_id
                    ORDER BY trade_date, trade_id
                ) AS running_balance
            FROM signed_trades
        )
        SELECT
            r.trade_id,
            r.trade_date,
            r.portfolio_id,
            r.asset_id,
            r.trade_side,
            r.quantity,
            r.running_balance,
            p.member_id,
            m.last_name
        FROM running AS r
        JOIN portfolios AS p
            ON p.portfolio_id = r.portfolio_id
        JOIN members AS m
            ON m.member_id = p.member_id
        WHERE r.trade_side = 'SELL' AND r.running_balance < 0
        ORDER BY r.trade_date, r.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** 2 sells broke the rule: trade_id 501 (portfolio 1, asset 1, member Student1) and trade_id 502 (portfolio 2, asset 2, member Student2), both on 2022-12-30, each leaving a running balance of -1 units.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9. Your manager question:
    Who has the most profitable portfolio and what are their top three assets by total return?
    """)
    return


@app.cell
def _(ask):
    ask(f"""
        SELECT
            p.portfolio_name,
            p.member_id,
            m.last_name,
            SUM(CASE
                WHEN t.trade_side = 'BUY' THEN -(t.quantity * t.price_per_unit + t.fee)
                WHEN t.trade_side = 'SELL' THEN (t.quantity * t.price_per_unit - t.fee)
                ELSE 0
            END) AS total_profit
        FROM portfolios p
        JOIN trades t ON p.portfolio_id = t.portfolio_id
        JOIN members m ON m.member_id = p.member_id
        GROUP BY p.portfolio_name, p.member_id, m.last_name
        ORDER BY total_profit DESC
        LIMIT 1;
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            a.asset_name,
            SUM(CASE
                WHEN t.trade_side = 'BUY' THEN -(t.quantity * t.price_per_unit + t.fee)
                WHEN t.trade_side = 'SELL' THEN (t.quantity * t.price_per_unit - t.fee)
                ELSE 0
            END) AS asset_profit
        FROM trades t
        JOIN assets a ON t.asset_id = a.asset_id
        WHERE t.portfolio_id = (
            SELECT p.portfolio_id
            FROM portfolios p
            JOIN trades t2 ON p.portfolio_id = t2.portfolio_id
            GROUP BY p.portfolio_id
            ORDER BY SUM(CASE
                WHEN t2.trade_side = 'BUY' THEN -(t2.quantity * t2.price_per_unit + t2.fee)
                WHEN t2.trade_side = 'SELL' THEN (t2.quantity * t2.price_per_unit - t2.fee)
                ELSE 0
            END) DESC
            LIMIT 1
        )
        GROUP BY a.asset_name
        ORDER BY asset_profit DESC
        LIMIT 3;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** Portfolio 1, owned by member Student1, has the most profitable realized trading, with a total profit of -\$383,339.24 because it is the least negative among all portfolios.  Its top three assets by realized return are Apple (+\$837.75), Exxon Mobil (-\$203.21), and Invesco NASDAQ 100 ETF (-\$2,131.37).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 10. Your second manager question

    What were the top three assest sold by quantity and by value during the last fiscal year?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            a.asset_name,
            SUM(t.quantity) AS total_quantity_sold,
            SUM(t.quantity * t.price_per_unit) AS total_value_sold
        FROM trades AS t
        JOIN assets AS a ON a.asset_id = t.asset_id
        WHERE t.trade_side = 'SELL'
            AND t.trade_date >= DATE '2022-01-01'
            AND t.trade_date <= DATE '2022-12-31'
        GROUP BY a.asset_name
        ORDER BY total_quantity_sold DESC
        LIMIT 3
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            a.asset_name,
            SUM(t.quantity) AS total_quantity_sold,
            SUM(t.quantity * t.price_per_unit) AS total_value_sold
        FROM trades AS t
        JOIN assets AS a ON a.asset_id = t.asset_id
        WHERE t.trade_side = 'SELL'
            AND t.trade_date >= DATE '2022-01-01'
            AND t.trade_date <= DATE '2022-12-31'
        GROUP BY a.asset_name
        ORDER BY total_value_sold DESC
        LIMIT 3
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Answer:** By quantity, the top three assets sold in 2022 were Bitcoin (172 units), Apple (160 units), and Ethereum (130 units); by value, the top three were Bitcoin (\$5,458,972.17), Ethereum (\$219,544.07), and Microsoft (\$43,269.36).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right

    Reach at least two answers a second way and show that the results agree. At least one check must run as code, show both numbers, and fail if they do not agree.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Alternate Approach for Q1: How much did each portfolio buy and sell in the last 30 days?

    For each portfolio, show its number of trades, money spent on buys with fees added, and money received from sells with fees taken off.
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        WITH buys AS (
            SELECT
                portfolio_id,
                count(*) AS buy_count,
                sum(quantity * price_per_unit + fee) AS total_bought
            FROM trades
            WHERE trade_side = 'BUY'
                AND trade_date > DATE '{as_of}' - INTERVAL 30 DAY
                AND trade_date <= DATE '{as_of}'
            GROUP BY portfolio_id
        ),
        sells AS (
            SELECT
                portfolio_id,
                count(*) AS sell_count,
                sum(quantity * price_per_unit - fee) AS total_sold
            FROM trades
            WHERE trade_side = 'SELL'
                AND trade_date > DATE '{as_of}' - INTERVAL 30 DAY
                AND trade_date <= DATE '{as_of}'
            GROUP BY portfolio_id
        )
        SELECT
            p.portfolio_id,
            p.portfolio_name,
            coalesce(b.buy_count, 0) + coalesce(s.sell_count, 0) AS trade_count,
            coalesce(b.buy_count, 0) AS buy_count,
            coalesce(s.sell_count, 0) AS sell_count,
            coalesce(b.total_bought, 0) AS total_bought,
            coalesce(s.total_sold, 0) AS total_sold
        FROM portfolios AS p
        LEFT JOIN buys AS b
            ON b.portfolio_id = p.portfolio_id
        LEFT JOIN sells AS s
            ON s.portfolio_id = p.portfolio_id
        ORDER BY trade_count DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The tables generated by different code chunks produce the same tables generated. This indicates that the output is consistent regardless of the method used to generate it.This confirms that both approaches are valid and can be used interchangeably to achieve the desired result.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Alternate Approach for Q2: How many portfolios does each member have, and how much have they bought?

    Include members with no portfolio. Show each member's portfolio count and the total value they bought across their portfolios.
    """)
    return


@app.cell
def _(ask):
    ask(f"""
        WITH portfolio_counts AS (
            SELECT
                member_id,
                count(*) AS portfolio_count
            FROM portfolios
            GROUP BY member_id
        ),
        member_buys AS (
            SELECT
                p.member_id,
                sum(t.quantity * t.price_per_unit + t.fee) AS total_bought
            FROM portfolios AS p
            JOIN trades AS t
                ON t.portfolio_id = p.portfolio_id
            WHERE t.trade_side = 'BUY'
            GROUP BY p.member_id
        )
        SELECT
            m.member_id,
            m.last_name,
            coalesce(pc.portfolio_count, 0) AS portfolio_count,
            coalesce(mb.total_bought, 0) AS total_bought
        FROM members AS m
        LEFT JOIN portfolio_counts AS pc
            ON pc.member_id = m.member_id
        LEFT JOIN member_buys AS mb
            ON mb.member_id = m.member_id
        ORDER BY m.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The tables generated by different code chunks produce the same tables generated. This indicates that the output is consistent regardless of the method used to generate it.This confirms that both approaches are valid and can be used interchangeably to achieve the desired result.
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
    **My response:** In the "Going Further on Q1" section, the agent first wrote a code block  comparing portfolios with more than 3 trades to portfolios with 3 or fewer, using no date filter, so it counted every trade a portfolio ever made. The result showed trade counts ranging from 26 up into the 30s for every portfolio.

    I didn't accept this, because I remembered Question 1 had already shown each portfolio's trade count, and the most active portfolio there was Portfolio 4 with only 7 trades. A portfolio with 7 trades in Question 1 now showing 30+ trades here didn't add up, so I asked the agent directly why the numbers disagreed.

    The agent explained the cause: Question 1 only counted trades in the last 30 days (the 30 days ending December 31, 2022), while the new code counted trades across all of history, two different timeframes being compared as if they were the same thing. I asked the agent to restrict the new query to the same 30-day window so the comparison would be fair.

    After that fix, I caught a second problem: the two trade-count groups only added up to 13 portfolios, not 15. The agent traced this to an inner JOIN silently dropping any portfolio with zero trades in the 30-day window, and discovered along the way that the database actually has 18 portfolios, not 15. Switching to a LEFT JOIN with profit defaulting to $0 fixed the count to 12 + 6 = 18, matching the true total.
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


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT count(*) AS joined_row_count
        FROM portfolios AS p
        JOIN trades AS t
            ON t.portfolio_id = p.portfolio_id
            AND t.trade_date <= DATE '{as_of}'
        JOIN assets AS a
            ON a.asset_id = t.asset_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Comparison and meaning:** My prediction was correct: the joins alone (before any grouping) produce exactly 502 rows, matching the 502 trades from Part A, since each trade joins to exactly one portfolio and one asset.

    This is a different number from the 167 rows in Part 3's final answer. That drop isn't because only 167 trades had positive returns, it's because of two later steps, not the join itself. First, `GROUP BY` collapses every trade that shares the same portfolio and asset into a single summed row, so a portfolio that traded the same asset across many separate trades still ends up as only one row. Second, the `HAVING` clause then drops any portfolio/asset pair whose summed holding is zero or negative, keeping only positive holdings. So 502 individual trades collapse down to far fewer portfolio/asset pairs, and of those pairs, 167 happen to have a positive balance left over as of the as_of date.

    One row in the final result means one portfolio's positive holding in one asset as of December 31, 2022, for example, Portfolio 1 held 28 units of Microsoft as of December 31, 2022.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Going Further on Q1

    Are portfolios with more than 3 trades more profitable than portfolio's with fewer trades?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        WITH portfolio_stats AS (
            SELECT
                p.portfolio_id,
                count(t.trade_id) AS trade_count,
                coalesce(sum(CASE
                    WHEN t.trade_side = 'BUY' THEN -(t.quantity * t.price_per_unit + t.fee)
                    WHEN t.trade_side = 'SELL' THEN (t.quantity * t.price_per_unit - t.fee)
                    ELSE 0
                END), 0) AS total_profit
            FROM portfolios AS p
            LEFT JOIN trades AS t
                ON t.portfolio_id = p.portfolio_id
                AND t.trade_date > DATE '{as_of}' - INTERVAL 30 DAY
                AND t.trade_date <= DATE '{as_of}'
            GROUP BY p.portfolio_id
        ),
        grouped AS (
            SELECT
                CASE WHEN trade_count > 3 THEN 'More than 3 trades' ELSE '3 or fewer trades' END AS trade_group,
                count(*) AS portfolio_count,
                avg(total_profit) AS avg_profit
            FROM portfolio_stats
            GROUP BY trade_group
        ),
        all_groups(trade_group) AS (
            VALUES ('More than 3 trades'), ('3 or fewer trades')
        )
        SELECT
            ag.trade_group,
            coalesce(g.portfolio_count, 0) AS portfolio_count,
            round(g.avg_profit, 2) AS avg_profit,
            round(
                g.avg_profit - (
                    SELECT other.avg_profit
                    FROM grouped AS other
                    WHERE other.trade_group <> ag.trade_group
                ),
            2) AS difference_from_other_group
        FROM all_groups AS ag
        LEFT JOIN grouped AS g
            ON g.trade_group = ag.trade_group
        ORDER BY ag.trade_group
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **My response:** I checked whether portfolios with more than 3 trades were more profitable than portfolios with 3 or fewer.

    My first attempt counted trades and profit across all time, with no date filter. That gave only one group: all 15 portfolios had more than 3 trades, since the smallest all-time trade count in the data was 26. There was no "3 or fewer" group to compare against, so the question couldn't be answered that way.

    I asked the agent why my highest trade count in Question 1 was only 7, while this query showed portfolios with over 30 trades. The answer was that Question 1 only counted trades in the last 30 days, while my new query counted all-time trades, two different timeframes. To make a fair comparison, I asked the agent to restrict this query to the same 30-day window as Question 1 (the 30 days ending December 31, 2022).

    After adding that date filter, the two groups still didn't add up to all portfolios: 7 + 6 only equaled 13. The agent found the cause: the query used an inner JOIN to trades, so any portfolio with zero trades in that 30-day window vanished from the results entirely, rather than showing up with a trade count of 0. It turned out my database has 18 portfolios total, not 15, and 5 of them made no trades at all in the window. Switching to a LEFT JOIN, with profit defaulting to $0 for portfolios with no trades, fixed this: 12 + 6 now equals 18, matching the true portfolio count.

    The query groups each portfolio into "more than 3 trades" or "3 or fewer trades" based on its trade count in that 30-day window, using the same realized profit formula as Question 9 (BUY subtracts cost, SELL adds proceeds), then averages profit within each group.

    The final result has two rows: 12 portfolios made 3 or fewer trades in the last 30 days, averaging about -$126.48 in profit; 6 portfolios made more than 3 trades, averaging about $65,300.04 in profit, a difference of about $65,426.52. So within this 30-day window, portfolios with more than 3 trades were on average much more profitable than those with fewer trades.
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
    **Hours:** 5
    """)
    return


if __name__ == "__main__":
    app.run()
