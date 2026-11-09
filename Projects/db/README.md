# 1. **The Scenario.**

Option B: Babson Investment Club.

The Babson Investment Club runs paper portfolios for its members to learn with. Each member can own one or more portfolios, and each portfolio records trades in assets that the club follows. The club keeps a full history of trades, tracks closing prices by day, and wants to answer questions about holdings, portfolio performance, and rule violations.

# 2. **The ERD.**

```mermaid
erDiagram
  MEMBERS ||--o{ PORTFOLIOS : owns
  PORTFOLIOS ||--o{ TRADES : makes
  ASSETS ||--o{ TRADES : trades
  ASSETS ||--o{ CLOSING_PRICES : has

  MEMBERS {
    int member_id PK
    string first_name
    string last_name
    string school_email UK
    int class_year
    date join_date
  }

  PORTFOLIOS {
    int portfolio_id PK
    int member_id FK
    string portfolio_name
    date created_on
    string strategy_label
  }

  ASSETS {
    int asset_id PK
    string ticker
    string asset_name
    string asset_type
    string sector
  }

  TRADES {
    int trade_id PK
    int portfolio_id FK
    int asset_id FK
    date trade_date
    string trade_side
    int quantity
    decimal price_per_unit
    decimal fee
  }

  CLOSING_PRICES {
    int closing_price_id PK
    int asset_id FK
    date price_date
    decimal close_price
  }
```

# 3. **What One Row Means.**

One row of `members` is one club member with one school email, class year, and join date.

One row of `portfolios` is one paper portfolio owned by one member.

One row of `assets` is one asset the club follows, identified by its ticker and its type and sector.

One row of `trades` is one buy or sell made by one portfolio in one asset on one date.

One row of `closing_prices` is one asset's closing price on one trading day.

# 4. **Design Choices.**
I used asset_id as the main key for the assets table because the club’s real data includes a ticker change over time, so the asset itself needs one stable identity for its key. The optional relationship are mostly at the top of the chain: a member can have no portfolios, a portfolio can have no trades yet, and a strategy label can be blank, while each individual trade still belongs to exactly one member’s portfolio and exactly one asset. The rule that a portfolio cannot sell more units than it currently owns is not something the table can enforce by itself because it depends on the running total across earlier trades. My agent suggested a simpler table with only current holdings, but I did not use it because the club wants a full trade history and a clean audit trail, so I kept separate trades and closing_prices tables instead.