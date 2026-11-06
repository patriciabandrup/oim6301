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
db: add the question and the plan