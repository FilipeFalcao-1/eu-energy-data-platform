import pandas as pd
from config import DATA_BRONZE, DATA_SILVER, DATA_GOLD, COUNTRIES

def clean_prices():
    """Bronze → Silver: clean and standardize prices to hourly UTC."""
    all_prices = []

    for country in COUNTRIES:
        df = pd.read_parquet(DATA_BRONZE / f"prices_{country}.parquet")
        df.index = df.index.tz_convert("UTC")
        # Resample from 15min to 1h (mean of 4 readings)
        df_hourly = df.resample("1h").mean()
        df_hourly["country"] = country
        all_prices.append(df_hourly)

    prices = pd.concat(all_prices).reset_index()
    prices.columns = ["timestamp", "price_mwh", "country"]
    prices.to_parquet(DATA_SILVER / "prices.parquet", index=False)
    print(f"Silver prices: {len(prices)} records saved")

def clean_generation():
    """Bronze → Silver: clean and standardize generation to hourly UTC."""
    all_gen = []

    for country in COUNTRIES:
        df = pd.read_parquet(DATA_BRONZE / f"generation_{country}.parquet")
        df.index = df.index.tz_convert("UTC")

        # Flatten multi-level columns: keep only "Actual Aggregated"
        if isinstance(df.columns, pd.MultiIndex):
            df = df.xs("Actual Aggregated", axis=1, level=1, drop_level=True)

        # Resample to 1h (ES comes in 15min, PT in 1h — standardize both)
        df_hourly = df.resample("1h").mean()
        df_hourly["country"] = country
        all_gen.append(df_hourly)

    gen = pd.concat(all_gen).reset_index()
    gen = gen.rename(columns={"index": "timestamp"})
    gen.to_parquet(DATA_SILVER / "generation.parquet", index=False)
    print(f"Silver generation: {len(gen)} records saved")

def build_gold():
    """Silver → Gold: build analytical indicators."""
    prices = pd.read_parquet(DATA_SILVER / "prices.parquet")
    gen = pd.read_parquet(DATA_SILVER / "generation.parquet")

    # --- Gold 1: Daily average price per country ---
    prices["date"] = pd.to_datetime(prices["timestamp"]).dt.date
    daily_prices = prices.groupby(["date", "country"])["price_mwh"].mean().reset_index()
    daily_prices.columns = ["date", "country", "avg_price_mwh"]
    daily_prices.to_parquet(DATA_GOLD / "daily_prices.parquet", index=False)

    # --- Gold 2: Price spread PT vs ES (MIBEL divergence) ---
    pt = prices[prices["country"] == "PT"].set_index("timestamp")["price_mwh"]
    es = prices[prices["country"] == "ES"].set_index("timestamp")["price_mwh"]
    spread = (pt - es).dropna().reset_index()
    spread.columns = ["timestamp", "spread_pt_es"]
    spread["date"] = pd.to_datetime(spread["timestamp"]).dt.date
    spread.to_parquet(DATA_GOLD / "price_spread.parquet", index=False)

    # --- Gold 3: Generation mix per country (daily totals by source) ---
    gen["date"] = pd.to_datetime(gen["timestamp"]).dt.date
    gen_cols = [c for c in gen.columns if c not in ["timestamp", "country", "date"]]
    daily_gen = gen.groupby(["date", "country"])[gen_cols].sum().reset_index()
    daily_gen.to_parquet(DATA_GOLD / "daily_generation.parquet", index=False)

    print(f"Gold daily_prices: {len(daily_prices)} records")
    print(f"Gold price_spread: {len(spread)} records")
    print(f"Gold daily_generation: {len(daily_gen)} records")

if __name__ == "__main__":
    clean_prices()
    clean_generation()
    build_gold()
    print("Pipeline complete: bronze → silver → gold")
