from __future__ import annotations
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/minstay_experiment.csv")

def main():
    # Read the data
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    # Start your analysis

if __name__ == "__main__":
    main()
