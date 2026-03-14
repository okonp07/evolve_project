from __future__ import annotations

import pandas as pd

from src.data_processor import DataProcessor
from src.recommendation_engine import MinStayRecommender


def make_sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "property_id": [1001, 1001, 1001, 1002, 1002, 1002, 1002, 1003, 1003],
            "date": pd.to_datetime(
                [
                    "2024-01-05",
                    "2024-01-12",
                    "2024-07-06",
                    "2024-02-01",
                    "2024-02-09",
                    "2024-07-13",
                    "2024-12-21",
                    "2024-03-03",
                    "2024-11-29",
                ]
            ),
            "booked": [1, 1, 1, 0, 0, 1, 1, 0, 1],
            "price": [210, 220, 250, 140, 145, 155, 180, 120, 150],
            "lead_time": [30, 45, 60, 5, 10, 20, 50, 2, 25],
            "event": [0, 1, 1, 0, 0, 0, 1, 0, 1],
        }
    )


def test_processor_adds_temporal_features() -> None:
    processor = DataProcessor(make_sample_df())
    enriched = processor.main_df
    assert {"day_name", "month_name", "is_weekend", "season", "lead_time_bucket"}.issubset(enriched.columns)
    assert processor.get_summary_statistics()["unique_properties"] == 3


def test_recommender_returns_expected_shape() -> None:
    processor = DataProcessor(make_sample_df())
    recommender = MinStayRecommender(processor.process())
    recommender.train()

    result = recommender.recommend(
        property_id=1001,
        target_date=pd.Timestamp("2024-07-12"),
        price=240,
        lead_time=35,
        event=True,
    )

    assert result["demand_level"] in {"Low", "Medium", "High"}
    assert 1 <= result["recommended_min_stay"] <= 7
    assert 60 <= result["confidence_pct"] <= 85
    assert len(result["reasons"]) >= 4


def test_high_demand_case_recommends_longer_stay() -> None:
    processor = DataProcessor(make_sample_df())
    recommender = MinStayRecommender(processor.process())
    recommender.train()

    high = recommender.recommend(
        property_id=1001,
        target_date=pd.Timestamp("2024-07-13"),
        price=230,
        lead_time=45,
        event=True,
    )
    low = recommender.recommend(
        property_id=1002,
        target_date=pd.Timestamp("2024-02-05"),
        price=150,
        lead_time=2,
        event=False,
    )

    assert high["recommended_min_stay"] >= low["recommended_min_stay"]
    assert high["demand_score"] >= low["demand_score"]
