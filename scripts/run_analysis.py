from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.data_processor import DataProcessor
from src.recommendation_engine import MinStayRecommender


DATA_PATH = Path("data/minstay_experiment.csv")


def main() -> None:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    processor = DataProcessor(df)
    recommender = MinStayRecommender(processor.process())
    recommender.train()

    sample_property = recommender.available_properties()[0]
    context = recommender.property_context(sample_property)
    recommendation = recommender.recommend(
        property_id=sample_property,
        target_date=recommender.default_target_date(),
        price=context["price_mean"],
        lead_time=21,
        event=False,
    )

    print("Dataset summary:")
    print(json.dumps(processor.get_summary_statistics(), default=str, indent=2))
    print("\nSample recommendation:")
    print(json.dumps(recommendation, indent=2))


if __name__ == "__main__":
    main()
