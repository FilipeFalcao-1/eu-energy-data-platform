import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path so config imports work
sys.path.insert(0, str(Path(__file__).parent))
from config import DATA_GOLD

st.set_page_config(page_title="EU Energy Platform", layout="wide")
st.title("⚡ European Energy Data Platform")
st.caption("Portugal vs Spain — October 2026 | Source: ENTSO-E Transparency Platform")

# --- Load gold tables ---
prices = pd.read_parquet(DATA_GOLD / "daily_prices.parquet")
spread = pd.read_parquet(DATA_GOLD / "price_spread.parquet")
balance = pd.read_parquet(DATA_GOLD / "energy_balance.parquet")
generation = pd.read_parquet(DATA_GOLD / "daily_generation.parquet")

# --- KPIs ---
bal_pt = balance[balance["country"] == "PT"]
days_exporter = len(bal_pt[bal_pt["status"] == "exporter"])
days_importer = len(bal_pt[bal_pt["status"] == "importer"])
avg_price_pt = prices[prices["country"] == "PT"]["avg_price_mwh"].mean()
avg_price_es = prices[prices["country"] == "ES"]["avg_price_mwh"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("PT Avg Price", f"€{avg_price_pt:.1f}/MWh")
col2.metric("ES Avg Price", f"€{avg_price_es:.1f}/MWh")
col3.metric("PT Days Exporter", f"{days_exporter}")
col4.metric("PT Days Importer", f"{days_importer}")

st.divider()

# --- Chart 1: Daily prices ---
st.subheader("Daily Average Price — PT vs ES")
prices["date"] = pd.to_datetime(prices["date"])
chart_prices = prices.pivot(index="date", columns="country", values="avg_price_mwh")
st.line_chart(chart_prices)

# --- Chart 2: Price spread ---
st.subheader("Price Spread PT - ES (hourly)")
st.caption("Positive = PT more expensive | Negative = ES more expensive")
spread["timestamp"] = pd.to_datetime(spread["timestamp"])
spread_chart = spread.set_index("timestamp")["spread_pt_es"]
st.line_chart(spread_chart)

# --- Chart 3: Energy balance ---
st.subheader("Energy Balance — Portugal")
st.caption("Positive = net exporter | Negative = net importer")
bal_pt = bal_pt.copy()
bal_pt["date"] = pd.to_datetime(bal_pt["date"])
st.bar_chart(bal_pt.set_index("date")["balance_mw"])

# --- Chart 4: Generation mix ---
st.subheader("Generation Mix — Portugal (daily total MW)")
gen_pt = generation[generation["country"] == "PT"].copy()
gen_pt["date"] = pd.to_datetime(gen_pt["date"])
gen_cols = [c for c in gen_pt.columns if c not in ["date", "country"]]
st.area_chart(gen_pt.set_index("date")[gen_cols])
