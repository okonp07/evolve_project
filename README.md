# Evolve Dynamic Minimum Stay Recommender

<p align="center">
  <img src="evolve-banner.png" alt="Evolve" width="700"/>
</p>

Streamlit application for recommending vacation-rental minimum stay rules using historical booking behavior, temporal demand patterns, event uplift, lead time, and price context.

## What This App Does

- Recommends a minimum stay of `1-7` nights for a selected property and date.
- Scores demand on a `0-100` scale using a hybrid heuristic.
- Shows confidence, supporting reasons, and practical strategy tips.
- Includes an analytics dashboard for booking trends, property comparisons, and temporal patterns.

## Methodology

The recommendation score follows the weighting described in the product spec:

- Property performance: `40%`
- Temporal patterns: `30%`
- Event impact: `15%`
- Lead time: `10%`
- Price competitiveness: `5%`

Demand scores map to policy tiers:

- `High (>= 70)`: stricter minimum stays
- `Medium (40-69)`: balanced restrictions
- `Low (< 40)`: lower minimums to improve occupancy

## Repository Structure

```text
.
├── app.py
├── requirements.txt
├── .streamlit/config.toml
├── src/
│   ├── data_processor.py
│   └── recommendation_engine.py
├── tests/
│   └── test_recommender.py
├── scripts/
│   └── run_analysis.py
├── data/
│   └── minstay_experiment.csv
├── notebooks/
│   ├── eda.ipynb
│   └── analysis.ipynb
└── README_2.md
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app expects the dataset at `data/minstay_experiment.csv`.

## Testing

```bash
pytest tests/ -v
python scripts/run_analysis.py
```

## Deployment

This repo is ready for Streamlit Cloud deployment with `app.py` as the entry point.

1. Push the repository to GitHub.
2. Open Streamlit Cloud.
3. Create a new app from the repo.
4. Set the main file path to `app.py`.
5. Deploy.

See [DEPLOYMENT.md](DEPLOYMENT.md) for a short deployment checklist.
