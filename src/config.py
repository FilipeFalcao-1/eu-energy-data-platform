import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API
ENTSOE_API_KEY = os.getenv("ENTSOE_API_KEY")

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_BRONZE = PROJECT_ROOT / "data" / "bronze"
DATA_SILVER = PROJECT_ROOT / "data" / "silver"
DATA_GOLD = PROJECT_ROOT / "data" / "gold"

# Countries for generation and load (ISO codes)
COUNTRIES = ["PT", "ES", "FR", "DE", "NL"]

# Bidding zones for prices (some differ from ISO)
PRICE_ZONES = {
    "PT": "PT",
    "ES": "ES",
    "FR": "FR",
    "DE": "DE_LU",
    "NL": "NL",
}
# Period (3 years of data)
DEFAULT_START = "2024-01-01"
DEFAULT_END = "2026-10-31"
