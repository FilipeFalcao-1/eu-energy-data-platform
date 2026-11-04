import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import DATA_GOLD

st.set_page_config(page_title="EU Energy Platform", layout="wide", page_icon="⚡")

# --- Load gold tables ---
@st.cache_data
def load_data():
    prices = pd.read_parquet(DATA_GOLD / "daily_prices.parquet")
    spread = pd.read_parquet(DATA_GOLD / "price_spread.parquet")
    balance = pd.read_parquet(DATA_GOLD / "energy_balance.parquet")
    generation = pd.read_parquet(DATA_GOLD / "daily_generation.parquet")

    for df in [prices, spread, balance, generation]:
        df["date"] = pd.to_datetime(df["date"])

    if "timestamp" in spread.columns:
        spread["timestamp"] = pd.to_datetime(spread["timestamp"])

    return prices, spread, balance, generation

prices, spread, balance, generation = load_data()

# --- Sidebar filters ---
st.sidebar.image("https://transparency.entsoe.eu/public/1.50.0/assets/logo.svg", width=180)
st.sidebar.title("Filters")

countries = sorted(prices["country"].unique())
selected_countries = st.sidebar.multiselect("Countries", countries, default=["PT", "ES"])

min_date = prices["date"].min().date()
max_date = prices["date"].max().date()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# --- Filter data ---
mask_prices = (
    prices["country"].isin(selected_countries)
    & (prices["date"] >= pd.Timestamp(start_date))
    & (prices["date"] <= pd.Timestamp(end_date))
)
f_prices = prices[mask_prices]

mask_balance = (
    balance["country"].isin(selected_countries)
    & (balance["date"] >= pd.Timestamp(start_date))
    & (balance["date"] <= pd.Timestamp(end_date))
)
f_balance = balance[mask_balance]

mask_gen = (
    generation["country"].isin(selected_countries)
    & (generation["date"] >= pd.Timestamp(start_date))
    & (generation["date"] <= pd.Timestamp(end_date))
)
f_gen = generation[mask_gen]

# --- Header ---
st.title("⚡ European Energy Data Platform")
st.caption(f"ENTSO-E Transparency Platform · {start_date} to {end_date} · {len(selected_countries)} countries")

# --- KPIs (Portugal focus) ---
if "PT" in selected_countries:
    pt_prices = f_prices[f_prices["country"] == "PT"]
    pt_balance = f_balance[f_balance["country"] == "PT"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("PT Avg Price", f"€{pt_prices['avg_price_mwh'].mean():.1f}/MWh")
    col2.metric("PT Max Price", f"€{pt_prices['avg_price_mwh'].max():.1f}/MWh")
    col3.metric("Days Exporter", f"{len(pt_balance[pt_balance['status'] == 'exporter'])}")
    col4.metric("Days Importer", f"{len(pt_balance[pt_balance['status'] == 'importer'])}")

st.divider()

# --- Chart 1: Daily prices by country ---
st.subheader("Daily Average Price by Country")
chart_prices = f_prices.pivot_table(index="date", columns="country", values="avg_price_mwh")
st.line_chart(chart_prices)

# --- Two columns: spread + balance ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Price Spread (PT vs others)")
    st.caption("Positive = PT more expensive")
    if "PT" in selected_countries:
        comparisons = [f"PT vs {c}" for c in selected_countries if c != "PT"]
        f_spread = spread[
            spread["comparison"].isin(comparisons)
            & (spread["date"] >= pd.Timestamp(start_date))
            & (spread["date"] <= pd.Timestamp(end_date))
        ]
        if not f_spread.empty:
            spread_chart = f_spread.pivot_table(index="timestamp", columns="comparison", values="spread")
            st.line_chart(spread_chart)
        else:
            st.info("Select at least one country besides PT to see the spread.")
    else:
        st.info("Add PT to the country filter to see spreads.")

with col_right:
    st.subheader("Energy Balance — Portugal")
    st.caption("Positive = net exporter · Negative = net importer")
    if "PT" in selected_countries:
        pt_bal = f_balance[f_balance["country"] == "PT"].set_index("date")
        st.bar_chart(pt_bal["balance_mw"])
    else:
        st.info("Add PT to the country filter.")

st.divider()

# --- Chart 3: Generation mix ---
st.subheader("Generation Mix (daily total MW)")
gen_country = st.selectbox("Select country for generation breakdown", selected_countries)
gen_filtered = f_gen[f_gen["country"] == gen_country]
if not gen_filtered.empty:
    gen_cols = [c for c in gen_filtered.columns if c not in ["date", "country"]]
    # Drop columns that are all zeros or NaN
    gen_plot = gen_filtered.set_index("date")[gen_cols]
    gen_plot = gen_plot.loc[:, (gen_plot != 0).any()]
    st.area_chart(gen_plot)

st.divider()

# --- Country comparison table ---
st.subheader("Country Comparison Summary")
summary = f_prices.groupby("country")["avg_price_mwh"].agg(["mean", "min", "max", "std"]).round(1)
summary.columns = ["Avg €/MWh", "Min €/MWh", "Max €/MWh", "Std Dev"]

bal_summary = f_balance.groupby("country")["status"].value_counts().unstack(fill_value=0)
if "exporter" in bal_summary.columns:
    summary["Days Exporter"] = bal_summary.get("exporter", 0)
if "importer" in bal_summary.columns:
    summary["Days Importer"] = bal_summary.get("importer", 0)

st.dataframe(summary, use_container_width=True)

# --- Footer ---
st.divider()
st.caption("Data source: [ENTSO-E Transparency Platform](https://transparency.entsoe.eu) · Built by Filipe Falcão")
