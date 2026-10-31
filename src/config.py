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

# Countries
COUNTRIES = ["PT", "ES"]

# Period (fixed for project delivery; in production, use dynamic dates for incremental ingestion)
DEFAULT_START = "2026-10-01"
DEFAULT_END = "2026-10-31"
