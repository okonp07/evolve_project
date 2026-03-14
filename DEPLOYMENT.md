# Deployment Guide

## Streamlit Cloud

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Click **New app**.
4. Select this repository and branch.
5. Set **Main file path** to `app.py`.
6. Deploy.

## Expected Files

- `app.py`
- `requirements.txt`
- `.streamlit/config.toml`
- `data/minstay_experiment.csv`

## Verification Checklist

- The app opens without module import errors.
- The recommendation page loads available properties.
- A recommendation can be generated for a sample property.
- The analytics dashboard renders charts.
- The About page shows the scoring methodology.

## Notes

- In this Codex sandbox I could validate imports, unit tests, and the recommendation pipeline.
- I could not complete a live `streamlit run` bind because local port binding is blocked by the sandbox, so the final deployment step needs to happen on your machine or on Streamlit Cloud.
