import csv
import random
from datetime import date, timedelta
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
FIRST_DAY = date(2022, 1, 1)
AS_OF = date(2022, 12, 31)
SEED = 6301
ORDINARY_TRADE_COUNT = 500


def write_csv(filename, columns, rows):
    with (DATA_DIR / filename).open("w", newline="") as _file:
        _writer = csv.DictWriter(_file, fieldnames=columns)
        _writer.writeheader()
        _writer.writerows(rows)


def main():
    randomizer = random.Random(SEED)
    DATA_DIR.mkdir(exist_ok=True)

    members = []
    for member_id in range(1, 16):
        members.append(
            {
                "member_id": member_id,
                "first_name": f"Member{member_id}",
                "last_name": f"Student{member_id}",
                "school_email": f"student{member_id}@babson.edu",
                "class_year": 2023 + (member_id - 1) % 5,
                "join_date": date(2018 + (member_id - 1) % 5, 9, 1).isoformat(),
            }
        )

    strategies = ["Value", "Income", "Momentum", "Balanced", "Dividend", "Growth"]
    portfolios = []
    for portfolio_id in range(1, 19):
        member_id = (portfolio_id - 1) % 13 + 1
        portfolios.append(
            {
                "portfolio_id": portfolio_id,
                "member_id": member_id,
                "portfolio_name": f"Portfolio {portfolio_id}",
                "created_on": (date(2021, 1, 1) + timedelta(days=portfolio_id * 12)).isoformat(),
                "strategy_label": strategies[(portfolio_id - 1) % len(strategies)],
            }
        )

    asset_details = [
        ("Apple", "stock", "Technology", 175.0),
        ("Microsoft", "stock", "Technology", 335.0),
        ("NVIDIA", "stock", "Semiconductors", 150.0),
        ("Exxon Mobil", "stock", "Energy", 65.0),
        ("Vanguard Total Stock Market ETF", "etf", "Broad Market", 220.0),
        ("Invesco NASDAQ 100 ETF", "etf", "Technology", 390.0),
        ("Bitcoin", "crypto", None, 47000.0),
        ("Ethereum", "crypto", None, 3700.0),
        ("Meta Platforms", "stock", "Communication Services", 340.0),
        ("JPMorgan Chase", "stock", "Financials", 160.0),
        ("Johnson & Johnson", "stock", "Healthcare", 170.0),
        ("SPDR S&P 500 ETF", "etf", "Broad Market", 475.0),
    ]
    assets = []
    for asset_id, detail in enumerate(asset_details, start=1):
        asset_name, asset_type, sector, _starting_price = detail
        assets.append(
            {
                "asset_id": asset_id,
                "asset_name": asset_name,
                "asset_type": asset_type,
                "sector": sector,
            }
        )

    asset_tickers = []
    for asset_id, ticker in [
        (1, "AAPL"),
        (2, "MSFT"),
        (3, "NVDA"),
        (4, "XOM"),
        (5, "VTI"),
        (6, "QQQ"),
        (7, "BTC"),
        (8, "ETH"),
        (9, "FB"),
        (10, "JPM"),
        (11, "JNJ"),
        (12, "SPY"),
    ]:
        asset_tickers.append(
            {
                "asset_id": asset_id,
                "ticker": ticker,
                "valid_from": FIRST_DAY.isoformat(),
                "valid_to": "",
            }
        )

    asset_tickers[8]["valid_to"] = date(2022, 6, 8).isoformat()
    asset_tickers.append(
        {
            "asset_id": 9,
            "ticker": "META",
            "valid_from": date(2022, 6, 9).isoformat(),
            "valid_to": "",
        }
    )

    calendar_days = []
    current_day = FIRST_DAY
    while current_day <= AS_OF:
        calendar_days.append(current_day)
        current_day += timedelta(days=1)

    weekday_dates = []
    for calendar_day in calendar_days:
        if calendar_day.weekday() < 5:
            weekday_dates.append(calendar_day)

    closing_prices = []
    price_by_asset_and_day = {}
    for asset_id, detail in enumerate(asset_details, start=1):
        _asset_name, asset_type, _sector, starting_price = detail
        if asset_type == "crypto":
            price_dates = calendar_days
            daily_volatility = 0.035
        else:
            price_dates = weekday_dates
            daily_volatility = 0.012

        current_price = starting_price
        for price_day in price_dates:
            daily_return = randomizer.gauss(0.0002, daily_volatility)
            current_price = max(0.5, current_price * (1 + daily_return))
            close_price = round(current_price, 2)
            closing_prices.append(
                {
                    "asset_id": asset_id,
                    "price_date": price_day.isoformat(),
                    "close_price": f"{close_price:.2f}",
                }
            )
            price_by_asset_and_day[(asset_id, price_day)] = close_price

    trades = []
    holdings = {}
    used_portfolio_asset_days = set()
    reserved_pairs = {(1, 1), (2, 2)}

    for trade_id, portfolio_id, asset_id, day_index in [
        (1, 1, 1, 0),
        (2, 2, 2, 1),
    ]:
        trade_day = weekday_dates[day_index]
        quantity = 20
        trades.append(
            {
                "trade_id": trade_id,
                "portfolio_id": portfolio_id,
                "asset_id": asset_id,
                "trade_date": trade_day.isoformat(),
                "trade_side": "BUY",
                "quantity": quantity,
                "price_per_unit": f"{price_by_asset_and_day[(asset_id, trade_day)]:.2f}",
                "fee": "0.00",
            }
        )
        holdings[(portfolio_id, asset_id)] = quantity
        used_portfolio_asset_days.add((portfolio_id, asset_id, trade_day))

    for trade_id in range(3, ORDINARY_TRADE_COUNT + 1):
        trade_day_index = (trade_id - 1) * len(weekday_dates) // ORDINARY_TRADE_COUNT
        trade_day = weekday_dates[trade_day_index]

        while True:
            portfolio_id = randomizer.randint(1, 15)
            asset_id = randomizer.randint(1, len(assets))
            trade_key = (portfolio_id, asset_id, trade_day)
            if (portfolio_id, asset_id) not in reserved_pairs and trade_key not in used_portfolio_asset_days:
                break

        held_quantity = holdings.get((portfolio_id, asset_id), 0)
        if held_quantity > 1 and randomizer.random() < 0.30:
            trade_side = "SELL"
            quantity = randomizer.randint(1, held_quantity - 1)
            holdings[(portfolio_id, asset_id)] = held_quantity - quantity
        else:
            trade_side = "BUY"
            quantity = randomizer.randint(5, 25)
            holdings[(portfolio_id, asset_id)] = held_quantity + quantity

        fee = randomizer.choice([0, round(randomizer.uniform(0.25, 7.50), 2)])
        trades.append(
            {
                "trade_id": trade_id,
                "portfolio_id": portfolio_id,
                "asset_id": asset_id,
                "trade_date": trade_day.isoformat(),
                "trade_side": trade_side,
                "quantity": quantity,
                "price_per_unit": f"{price_by_asset_and_day[(asset_id, trade_day)]:.2f}",
                "fee": f"{fee:.2f}",
            }
        )
        used_portfolio_asset_days.add(trade_key)

    intentional_violations = []
    for trade_id, portfolio_id, asset_id in [(501, 1, 1), (502, 2, 2)]:
        trade_day = weekday_dates[-1]
        held_quantity = holdings[(portfolio_id, asset_id)]
        quantity = held_quantity + 1
        trades.append(
            {
                "trade_id": trade_id,
                "portfolio_id": portfolio_id,
                "asset_id": asset_id,
                "trade_date": trade_day.isoformat(),
                "trade_side": "SELL",
                "quantity": quantity,
                "price_per_unit": f"{price_by_asset_and_day[(asset_id, trade_day)]:.2f}",
                "fee": "1.00",
            }
        )
        intentional_violations.append(
            f"trade_id={trade_id}: portfolio {portfolio_id}, asset {asset_id}, "
            f"sold {quantity} with only {held_quantity} shares held"
        )

    actual_violations = []
    seen_trade_days = set()
    checked_holdings = {}
    for trade in sorted(trades, key=lambda row: (row["trade_date"], row["trade_id"])):
        trade_date = date.fromisoformat(trade["trade_date"])
        trade_key = (trade["portfolio_id"], trade["asset_id"], trade_date)
        if trade_key in seen_trade_days:
            raise ValueError(f"More than one trade for portfolio/asset/day: {trade_key}")
        seen_trade_days.add(trade_key)

        if (trade["asset_id"], trade_date) not in price_by_asset_and_day:
            raise ValueError(f"Trade has no closing price: trade_id={trade['trade_id']}")

        holding_key = (trade["portfolio_id"], trade["asset_id"])
        held_quantity = checked_holdings.get(holding_key, 0)
        if trade["trade_side"] == "BUY":
            checked_holdings[holding_key] = held_quantity + trade["quantity"]
        elif trade["quantity"] > held_quantity:
            actual_violations.append(trade["trade_id"])
        else:
            checked_holdings[holding_key] = held_quantity - trade["quantity"]

    if actual_violations != [501, 502]:
        raise ValueError(f"Expected only trades 501 and 502 to oversell; found {actual_violations}")

    write_csv(
        "members.csv",
        ["member_id", "first_name", "last_name", "school_email", "class_year", "join_date"],
        members,
    )
    write_csv(
        "portfolios.csv",
        ["portfolio_id", "member_id", "portfolio_name", "created_on", "strategy_label"],
        portfolios,
    )
    write_csv(
        "assets.csv",
        ["asset_id", "asset_name", "asset_type", "sector"],
        assets,
    )
    write_csv(
        "asset_tickers.csv",
        ["asset_id", "ticker", "valid_from", "valid_to"],
        asset_tickers,
    )
    write_csv(
        "closing_prices.csv",
        ["asset_id", "price_date", "close_price"],
        closing_prices,
    )
    write_csv(
        "trades.csv",
        [
            "trade_id",
            "portfolio_id",
            "asset_id",
            "trade_date",
            "trade_side",
            "quantity",
            "price_per_unit",
            "fee",
        ],
        trades,
    )

    print(f"As of: {AS_OF} (12 months: {FIRST_DAY} through {AS_OF})")
    print(
        f"Members: {len(members)}; portfolios: {len(portfolios)}; "
        f"assets: {len(assets)}; ticker records: {len(asset_tickers)}"
    )
    print(f"Trades: {len(trades)}; closing prices: {len(closing_prices)}")
    print("Intentional sell-more-than-held rows:")
    for violation in intentional_violations:
        print(f"  {violation}")
    print("Unattached rows: members 14 and 15 have no portfolios; portfolios 16, 17, and 18 have no trades.")


if __name__ == "__main__":
    main()