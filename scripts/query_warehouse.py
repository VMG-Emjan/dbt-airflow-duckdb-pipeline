"""Query the built DuckDB warehouse and print sample results.

Run after `dbt seed && dbt run` to prove the warehouse contains real,
queryable tables. Used by CI as a smoke test and to produce the sample
output shown in the README.
"""

import sys
from pathlib import Path

import duckdb

# Windows consoles may default to a legacy code page that cannot render
# DuckDB's box-drawing output.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DB_PATH = Path(__file__).resolve().parent.parent / "warehouse" / "warehouse.duckdb"

QUERIES = {
    "Monthly revenue report (rpt_monthly_revenue)": """
        select * from rpt_monthly_revenue order by revenue_month
    """,
    "Top 5 customers by lifetime value (dim_customers)": """
        select customer_id, full_name, country, order_count, lifetime_value
        from dim_customers
        order by lifetime_value desc
        limit 5
    """,
}


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"Warehouse not found at {DB_PATH}. Run `dbt seed && dbt run` first.")

    con = duckdb.connect(str(DB_PATH), read_only=True)
    for title, query in QUERIES.items():
        print(f"\n=== {title} ===")
        print(con.sql(query))
    con.close()


if __name__ == "__main__":
    main()
