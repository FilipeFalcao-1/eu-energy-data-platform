
# European Energy Data Platform - A Data Engineering Project

An end-to-end data engineering project built on real European electricity market data — day-ahead prices, load, and generation mix. The European energy sector is one of the largest employers of data engineers on the continent: the energy transition has turned utilities into data-driven organizations. All data comes from the ENTSO-E Transparency Platform — a public, official, and continuously updated source, accessed via REST API


## Source

 - [ENTSOE DataBase](https://transparency.entsoe.eu)

  ENTSO-E (European Network of Transmission System Operators for Electricity) is an association of 40 electricity transmission system operators (TSOs) across 36 European countries. It coordinates the continent's interconnected power grid to ensure secure electricity supplies, manage cross-border energy trading, and drive the transition toward carbon neutrality.

## Project Architecture
```
eu-energy-data-platform/
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── src/
├── tests/
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```


## Tech Stack

| Camada        | Technology.   |
| ------------- |:-------------:|
| Extraction    | entsoe-py/requests|
| Processing    | Pandas→PySpark|
| Storage       | Parquet (Delta Lake)    |
| Orchestration      | Script-based→Airflow|
| Visualization    | Power BI|

## Running

```
We'll put it here later
```


## Authors

- [@filipefalcao-1](https://www.github.com/FilipeFalcao-1)
- [Linkedin_Profile](https://www.linkedin.com/in/filipe-falcao1/)
