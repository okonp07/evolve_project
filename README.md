# Evolve Dynamic Minimum Stay Recommender

<p align="center">
  <img src="evolve-banner.png" alt="Evolve" width="700"/>
</p>

Streamlit application for recommending vacation-rental minimum stay rules using historical booking behavior, temporal demand patterns, event uplift, lead time, and price context.

## Live App

### [Open the deployed Streamlit app](https://evolveproject-7ji95fds7ffsc5kzq9xmsz.streamlit.app)

If the app has just been updated, give Streamlit a minute to finish rebuilding before refreshing the page.

## Current Project Status

- The Streamlit app is live and deployable from `main`
- The recommendation flow is backed by a working `src/` package
- Zero-price / inactive properties are excluded from the property selector
- The repository includes tests and a small CLI analysis script for verification

## What This App Does

- Recommends a minimum stay of `1-7` nights for a selected property and date.
- Scores demand on a `0-100` scale using a hybrid heuristic.
- Shows confidence, supporting reasons, and practical strategy tips.
- Includes an analytics dashboard for booking trends, property comparisons, and temporal patterns.
- Restricts recommendations to properties with active pricing history.

## How To Use The App

### On The Live App

1. Open the live app link above.
2. Go to `Get Recommendation`.
3. Select a property from the dropdown.
4. Choose a target stay date.
5. Optionally mark whether there is a local event or holiday.
6. Adjust nightly price and lead time if needed.
7. Click `Get Recommendation`.

The app returns:

- a recommended minimum stay
- a demand score out of `100`
- a confidence score
- a demand tier (`Low`, `Medium`, or `High`)
- reasoning and strategy tips

### In The Analytics Dashboard

Use `Analytics Dashboard` to review:

- overall booking-rate trends over time
- event vs non-event performance
- top-performing properties
- day-of-week and month-level demand patterns

### About The Inputs

- `Property`: only active, priced properties are shown
- `Target stay date`: the date you want to evaluate
- `Nightly price`: defaults to the selected property's historical average price
- `Lead time`: days between today/booking date and check-in
- `Local event / holiday`: adds event uplift to the demand score

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

Then open `http://localhost:8501` in your browser.

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
