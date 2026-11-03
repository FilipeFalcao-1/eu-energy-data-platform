from entsoe import EntsoePandasClient
import pandas as pd
import time
from config import ENTSOE_API_KEY, COUNTRIES, PRICE_ZONES, DEFAULT_START, DEFAULT_END, DATA_BRONZE

client = EntsoePandasClient(api_key=ENTSOE_API_KEY)

start = pd.Timestamp(DEFAULT_START, tz="UTC")
end = pd.Timestamp(DEFAULT_END, tz="UTC")

for country in COUNTRIES:
    print(f"\n--- Extracting {country} ---")

    # Prices
      # Prices (using bidding zone, not ISO code)
    try:
        zone = PRICE_ZONES[country]
        prices = client.query_day_ahead_prices(zone, start=start, end=end)
        prices.to_frame(name="price_mwh").to_parquet(DATA_BRONZE / f"prices_{country}.parquet")
        print(f"  prices: {len(prices)} records")
    except Exception as e:
        print(f"  prices FAILED: {e}")

    time.sleep(5)

    # Generation
    try:
        gen = client.query_generation(country, start=start, end=end, psr_type=None)
        gen.to_parquet(DATA_BRONZE / f"generation_{country}.parquet")
        print(f"  generation: {len(gen)} records")
    except Exception as e:
        print(f"  generation FAILED: {e}")

    time.sleep(5)

    # Load
    try:
        load = client.query_load(country, start=start, end=end)
        load.to_parquet(DATA_BRONZE / f"load_{country}.parquet")
        print(f"  load: {len(load)} records")
    except Exception as e:
        print(f"  load FAILED: {e}")

    time.sleep(5)

    print(f"  {country} complete")
