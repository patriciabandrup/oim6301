import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
	import duckdb
	import marimo as mo
	import polars as pl

	return duckdb, mo, pl


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
	# Part A: The Build

	## 1. The Tables

	The six tables record members, portfolios, assets, ticker history, trades, and closing prices. Keys protect the relationships; `CHECK`, `UNIQUE`, and `NOT NULL` rules protect individual rows. A trade's value can be calculated as quantity times price per unit; its fee stays separate. Whether a portfolio sells more shares than it owns depends on earlier trades, so that rule is checked with a query.
	""")
	return


@app.cell(hide_code=True)
def _(mo):
	mo.md(r"""
	## 2. The Data

	`make_data.py` writes one CSV per table with a fixed seed. The 12-month period is January 1 through December 31, 2022 (`as_of`). It creates 15 members, 18 portfolios, 12 assets, 500 ordinary trades, and 3,330 closing prices. Stocks and ETFs have weekday prices; crypto has a price every calendar day. Members 14 and 15 have no portfolios, and portfolios 16 through 18 have no trades. Facebook's asset keeps one identity while its ticker changes from FB to META on June 9, 2022.

	The only intentionally broken business rule is selling more shares than the portfolio holds. Trade 501 (portfolio 1, asset 1) sells 21 shares while holding 20; trade 502 (portfolio 2, asset 2) does the same. The database accepts them because this rule depends on earlier rows.
	""")
	return


@app.cell
def _(database, duckdb, mo):
	database.unlink(missing_ok=True)

	with duckdb.connect(database) as _con:
		_con.execute("""
			CREATE TABLE members (
				member_id INTEGER PRIMARY KEY,
				first_name VARCHAR NOT NULL,
				last_name VARCHAR NOT NULL,
				school_email VARCHAR NOT NULL UNIQUE,
				class_year INTEGER NOT NULL,
				join_date DATE NOT NULL
			)
		""")
		_con.execute("""
			CREATE TABLE portfolios (
				portfolio_id INTEGER PRIMARY KEY,
				member_id INTEGER NOT NULL REFERENCES members(member_id),
				portfolio_name VARCHAR NOT NULL,
				created_on DATE NOT NULL,
				strategy_label VARCHAR DEFAULT 'Unspecified',
				UNIQUE (member_id, portfolio_name)
			)
		""")
		_con.execute("""
			CREATE TABLE assets (
				asset_id INTEGER PRIMARY KEY,
				asset_name VARCHAR NOT NULL,
				asset_type VARCHAR NOT NULL CHECK (asset_type IN ('stock', 'etf', 'crypto')),
				sector VARCHAR,
				CHECK (
					(asset_type = 'crypto' AND sector IS NULL)
					OR (asset_type IN ('stock', 'etf') AND sector IS NOT NULL)
				)
			)
		""")
		_con.execute("""
			CREATE TABLE asset_tickers (
				asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
				ticker VARCHAR NOT NULL UNIQUE,
				valid_from DATE NOT NULL,
				valid_to DATE,
				PRIMARY KEY (asset_id, valid_from),
				CHECK (valid_to IS NULL OR valid_to >= valid_from)
			)
		""")
		_con.execute("""
			CREATE TABLE closing_prices (
				asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
				price_date DATE NOT NULL,
				close_price DECIMAL(12, 2) NOT NULL CHECK (close_price > 0),
				PRIMARY KEY (asset_id, price_date)
			)
		""")
		_con.execute("""
			CREATE TABLE trades (
				trade_id INTEGER PRIMARY KEY,
				portfolio_id INTEGER NOT NULL REFERENCES portfolios(portfolio_id),
				asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
				trade_date DATE NOT NULL,
				trade_side VARCHAR NOT NULL CHECK (trade_side IN ('BUY', 'SELL')),
				quantity INTEGER NOT NULL CHECK (quantity > 0),
				price_per_unit DECIMAL(12, 2) NOT NULL CHECK (price_per_unit > 0),
				fee DECIMAL(8, 2) NOT NULL DEFAULT 0 CHECK (fee >= 0),
				UNIQUE (portfolio_id, asset_id, trade_date),
				FOREIGN KEY (asset_id, trade_date)
					REFERENCES closing_prices(asset_id, price_date)
			)
		""")

		_data_dir = mo.notebook_dir() / "data"
		_con.execute(f"INSERT INTO members SELECT * FROM read_csv_auto('{_data_dir / 'members.csv'}')")
		_con.execute(f"INSERT INTO portfolios SELECT * FROM read_csv_auto('{_data_dir / 'portfolios.csv'}')")
		_con.execute(f"INSERT INTO assets SELECT * FROM read_csv_auto('{_data_dir / 'assets.csv'}')")
		_con.execute(f"INSERT INTO asset_tickers SELECT * FROM read_csv_auto('{_data_dir / 'asset_tickers.csv'}')")
		_con.execute(f"INSERT INTO closing_prices SELECT * FROM read_csv_auto('{_data_dir / 'closing_prices.csv'}')")
		_con.execute(f"INSERT INTO trades SELECT * FROM read_csv_auto('{_data_dir / 'trades.csv'}')")
		_con.execute("""
			CREATE VIEW weekly_portfolio_activity AS
			SELECT
				date_trunc('week', trade_date)::DATE AS week_start,
				portfolio_id,
				count(*) AS trade_count,
				sum(CASE WHEN trade_side = 'BUY' THEN quantity ELSE 0 END) AS shares_bought,
				sum(CASE WHEN trade_side = 'SELL' THEN quantity ELSE 0 END) AS shares_sold
			FROM trades
			GROUP BY week_start, portfolio_id
		""")

	built_database = database
	built_database.name
	return (built_database,)


@app.cell(hide_code=True)
def _(mo):
	mo.md(r"""
	## 3. A Look at the Data
	""")
	return


@app.cell
def _(built_database, mo, pl):
	_ = built_database
	_prices_file = mo.notebook_dir() / "data" / "closing_prices.csv"
	_prices = (
		pl.read_csv(_prices_file, try_parse_dates=True)
		.filter(pl.col("asset_id") == 1)
		.sort("price_date")
	)

	import matplotlib.pyplot as plt

	_figure, _axis = plt.subplots(figsize=(10, 4))
	_axis.plot(_prices["price_date"], _prices["close_price"], color="#167b72")
	_axis.set(title="AAPL simulated closing prices, 2022", xlabel="Date", ylabel="Price ($)")
	_axis.grid(alpha=0.2)
	_figure.tight_layout()
	_figure
	return


@app.cell(hide_code=True)
def _(mo):
	mo.md(r"""
	The daily AAPL prices move unevenly but gradually, a plausible shape for a traded asset; these are synthetic prices, not historical market data.
	""")
	return


@app.cell(hide_code=True)
def _(mo):
	mo.md(r"""
	## 4. Row Counts
	""")
	return


@app.cell
def _(ask, built_database):
	_ = built_database
	ask("""
		SELECT 'members' AS table_name, count(*) AS rows FROM members
		UNION ALL SELECT 'portfolios', count(*) FROM portfolios
		UNION ALL SELECT 'assets', count(*) FROM assets
		UNION ALL SELECT 'asset_tickers', count(*) FROM asset_tickers
		UNION ALL SELECT 'trades', count(*) FROM trades
		UNION ALL SELECT 'closing_prices', count(*) FROM closing_prices
		ORDER BY table_name
	""")
	return


@app.cell(hide_code=True)
def _(mo):
	mo.md(r"""
	## 5. A Row It Refuses

	This insert reuses an existing member's unique school email. The write connection closes immediately, and the caught message lets the notebook continue.
	""")
	return


@app.cell
def _(built_database, database, duckdb):
	try:
		with duckdb.connect(database) as _con:
			_con.execute("""
				INSERT INTO members (member_id, first_name, last_name, school_email, class_year, join_date)
				VALUES (999, 'Duplicate', 'Member', 'student1@babson.edu', 2022, '2022-01-01')
			""")
		refusal_message = "accepted"
	except duckdb.ConstraintException as _error:
		refusal_message = str(_error).splitlines()[0]

	refusal_message
	return


@app.cell(hide_code=True)
def _(mo):
	mo.md(r"""
	## 6. Answers You Already Knew

	These totals are known because `make_data.py` creates the source rows.

	- Members: expected 15.
	- Assets: expected 12.
	- Trades, including the two intentional oversells: expected 502.
	""")
	return


@app.cell
def _(ask, built_database):
	_ = built_database
	ask("SELECT count(*) AS members FROM members")
	return


@app.cell
def _(ask, built_database):
	_ = built_database
	ask("SELECT count(*) AS assets FROM assets")
	return


@app.cell
def _(ask, built_database):
	_ = built_database
	ask("SELECT count(*) AS trades FROM trades")
	return


@app.cell(hide_code=True)
def _(mo):
	mo.md(r"""
	## 7. A View

	`weekly_portfolio_activity` answers a weekly business question: how many trades and how many shares bought or sold did each portfolio have? It is created in the build cell and always reflects the current trades.
	""")
	return


@app.cell
def _(ask, built_database):
	_ = built_database
	ask("""
		SELECT *
		FROM weekly_portfolio_activity
		ORDER BY week_start, portfolio_id
		LIMIT 10
	""")
	return


if __name__ == "__main__":
	app.run()
