from entsoe import EntsoePandasClient
import pandas as pd

load_dotenv()
token = os.getenv("ENTSOE_API_KEY")
client = EntsoePandasClient(api_key=token)

start = pd.Timestamp("2026-10-01", tz="UTC")
end = pd.Timestamp("2026-10-31", tz="UTC")

prices_pt = client.query_day_ahead_prices("PT", start=start, end=end)
prices_es = client.query_day_ahead_prices("ES", start=start, end=end)

diff = prices_es - prices_pt
divergent = diff[diff != 0]

print(f"Total de registros: {len(prices_pt)}")
print(f"Registros com preço diferente: {len(divergent)}")
print(f"\nMomentos onde divergiram:")
print(divergent)

gen_es = client.query_generation("ES", start=pd.Timestamp("2026-10-05", tz="UTC"), end=pd.Timestamp("2026-10-06", tz="UTC"), psr_type=None)
print(gen_es)

gen_pt = client.query_generation("PT", start=pd.Timestamp("2026-10-05", tz="UTC"), end=pd.Timestamp("2026-10-06", tz="UTC"), psr_type=None)
print(gen_pt)
