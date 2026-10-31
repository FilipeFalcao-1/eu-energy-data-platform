import pandas as pd
import pytest


def test_resample_15min_to_1h():
    """15-min prices should resample to 1h with correct mean."""
    timestamps = pd.date_range("2026-10-01", periods=4, freq="15min", tz="UTC")
    df = pd.DataFrame({"price_mwh": [100.0, 110.0, 120.0, 130.0]}, index=timestamps)

    df_hourly = df.resample("1h").mean()

    assert len(df_hourly) == 1
    assert df_hourly["price_mwh"].iloc[0] == 115.0


def test_resample_incomplete_hour():
    """If only 2 of 4 quarters arrive, resample still produces 1 row."""
    timestamps = pd.date_range("2026-10-01", periods=2, freq="15min", tz="UTC")
    df = pd.DataFrame({"price_mwh": [100.0, 120.0]}, index=timestamps)

    df_hourly = df.resample("1h").mean()

    assert len(df_hourly) == 1
    assert df_hourly["price_mwh"].iloc[0] == 110.0


def test_spread_calculation():
    """Price spread PT - ES should be correct."""
    index = pd.date_range("2026-10-01", periods=3, freq="1h", tz="UTC")
    pt = pd.Series([100.0, 150.0, 200.0], index=index, name="price_mwh")
    es = pd.Series([100.0, 120.0, 200.0], index=index, name="price_mwh")

    spread = pt - es

    assert spread.iloc[0] == 0.0    # same price, no divergence
    assert spread.iloc[1] == 30.0   # PT more expensive
    assert spread.iloc[2] == 0.0    # same price again
