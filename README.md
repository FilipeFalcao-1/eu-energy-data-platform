# European Energy Data Platform

## Live Dashboard

📊 **[Open Dashboard](https://eu-energy-data-platform-qlezaqdxwpme5ygdxdmitv.streamlit.app)**

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
```
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
```

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


## Key Findings (January 2024 — October 2026)

### Portugal is becoming more dependent on energy imports
Over the three-year period, Portugal's net import position has deepened. The country starts each year as a net exporter (Q1), but transitions to net importer earlier each year — by April 2026, Portugal was already importing consistently, whereas in 2024 this shift happened later in the year.

### Seasonal pattern: hydro drives the first half, imports cover the second
Portugal exports energy in Q1 when rainfall fills reservoirs (strong hydro generation) and wind output is high. From Q2 onward, reservoirs drop, wind decreases, and even with strong solar generation, domestic supply falls short. Air conditioning demand in summer worsens the gap.

### Portugal's import dependency is comparable to Germany's
Both countries show a structural importer pattern across the period. The Netherlands, while also an importer, has a stronger export participation. France stands out as a consistent exporter, powered by its nuclear fleet.

### Prices are stabilizing, but imports keep growing
Energy prices across all five countries show a downward trend from the 2022 crisis peaks. However, Portugal's import volumes have not decreased proportionally — suggesting that price stabilization has not translated into energy independence.

### MIBEL convergence remains high (~93%)
Portugal and Spain share the same price ~93% of the time, confirming the integrated Iberian market. Price divergences concentrate during evening peak hours (18:00–21:00) when Portuguese renewable generation drops and interconnection capacity becomes the bottleneck.

### 1.5M+ records processed
The pipeline processes over 1.5 million records across 5 countries (PT, ES, FR, DE, NL), 3 datasets (prices, generation, load), and 34 months — from a live REST API with authentication, rate limits, and timezone normalization.

## Author

**Filipe Falcão** — Senior Data Analyst transitioning into Data Engineering.

[LinkedIn](https://linkedin.com/in/filipe-falcao1) · [GitHub](https://github.com/FilipeFalcao-1)
