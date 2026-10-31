from entsoe import EntsoePandasClient
import pandas as pd
from config import ENTSOE_API_KEY, COUNTRIES, DEFAULT_START, DEFAULT_END, DATA_BRONZE

client = EntsoePandasClient(api_key=ENTSOE_API_KEY)

start = pd.Timestamp(DEFAULT_START, tz="UTC")
end = pd.Timestamp(DEFAULT_END, tz="UTC")

for country in COUNTRIES:
    # Preços
    prices = client.query_day_ahead_prices(country, start=start, end=end)
    prices.to_frame(name="price_mwh").to_parquet(DATA_BRONZE / f"prices_{country}.parquet")

    # Geração
    gen = client.query_generation(country, start=start, end=end, psr_type=None)
    gen.to_parquet(DATA_BRONZE / f"generation_{country}.parquet")

    #Consumo
    load = client.query_load(country, start=start, end=end)
    load.to_parquet(DATA_BRONZE / f"load_{country}.parquet")
    print(f"{country}: prices, generation and load saved to bronze")
