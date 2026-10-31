# European Energy Data Platform

End-to-end data engineering project built on real European electricity market data — day-ahead prices, load (consumption), and generation mix.

All data comes from the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu) — a public, official, and continuously updated source, accessed via REST API.

## Central Question

**Is Portugal a net exporter or importer of electricity — and what drives it?**

The pipeline answers this by comparing generation and consumption data across Portugal and Spain (the Iberian market — MIBEL), identifying price divergences and energy balance patterns.

## Pipeline

ENTSO-E API → Bronze (raw Parquet) → Silver (cleaned, hourly UTC) → Gold (indicators) → Streamlit


| Layer  | What happens                                                        |
|--------|---------------------------------------------------------------------|
| Bronze | Raw data saved as-is from the API. Immutable.                       |
| Silver | Timezone normalized to UTC, resampled to 1h, countries unified.     |
| Gold   | Daily prices, price spread PT vs ES, generation mix, energy balance.|

## Project Structure

eu-energy-data-platform/
├── data/
│ ├── bronze/
│ ├── silver/
│ └── gold/
├── src/
│ ├── config.py
│ ├── extractor.py
│ ├── transformer.py
│ └── app.py
├── tests/
│ └── test_transformer.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md


## Tech Stack

| Layer         | Technology                      |
|---------------|---------------------------------|
| Extraction    | entsoe-py, requests             |
| Processing    | Pandas                          |
| Storage       | Parquet (medallion architecture) |
| Visualization | Streamlit                       |
| Testing       | pytest                          |

## How to Run

```bash
# 1. Clone and setup
git clone https://github.com/FilipeFalcao-1/eu-energy-data-platform.git
cd eu-energy-data-platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure API token
cp .env.example .env
# Edit .env and add your ENTSO-E security token

# 3. Run the pipeline
python src/extractor.py
python src/transformer.py

# 4. Launch the dashboard
streamlit run src/app.py

# 5. Run tests
pytest tests/ -v
```

## Key Findings (October 2026)

- Portugal is a **net importer** of electricity for most of the month
- Prices between PT and ES converge ~93% of the time (MIBEL effect)
- Price divergences occur during evening peak hours when Portuguese renewable generation drops
- Spain's diversified generation mix (nuclear, gas, wind, solar) keeps its prices more stable

## Author

**Filipe Falcão** — Senior Data Analyst transitioning into Data Engineering.

[LinkedIn](https://linkedin.com/in/filipe-falcao1) · [GitHub](https://github.com/FilipeFalcao-1)
