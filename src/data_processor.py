from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class DataProcessor:
    """Validate, clean, and enrich booking data for analysis and recommendations."""

    df: pd.DataFrame

    def __post_init__(self) -> None:
        self.df = self.df.copy()
        self._validate_data()
        self.df = self._clean_data(self.df)
        self.main_df = self._add_temporal_features(self.df)
        self.property_stats = self._calculate_property_stats()
        self.temporal_stats = self._calculate_temporal_stats()
        self.event_stats = self._calculate_event_stats()
        self.lead_time_stats = self._calculate_lead_time_stats()

    def _validate_data(self) -> None:
        required_cols = ["property_id", "date", "booked", "price", "lead_time", "event"]
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        cleaned = df.copy()
        cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
        cleaned["property_id"] = pd.to_numeric(cleaned["property_id"], errors="coerce")
        cleaned["booked"] = pd.to_numeric(cleaned["booked"], errors="coerce").fillna(0).clip(0, 1).astype(int)
        cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce").fillna(0.0).clip(lower=0.0)
        cleaned["lead_time"] = pd.to_numeric(cleaned["lead_time"], errors="coerce").fillna(0.0).clip(lower=0.0)
        cleaned["event"] = pd.to_numeric(cleaned["event"], errors="coerce").fillna(0).clip(0, 1).astype(int)
        cleaned = cleaned.dropna(subset=["property_id", "date"]).copy()
        cleaned["property_id"] = cleaned["property_id"].astype(int)
        return cleaned

    def _add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        enriched = df.copy()
        enriched["day_of_week"] = enriched["date"].dt.dayofweek
        enriched["day_name"] = enriched["date"].dt.day_name()
        enriched["month"] = enriched["date"].dt.month
        enriched["month_name"] = enriched["date"].dt.month_name()
        enriched["week_of_year"] = enriched["date"].dt.isocalendar().week.astype(int)
        enriched["is_weekend"] = enriched["day_of_week"].isin([4, 5]).astype(int)
        enriched["season"] = enriched["month"].map(
            {
                12: "Winter",
                1: "Winter",
                2: "Winter",
                3: "Spring",
                4: "Spring",
                5: "Spring",
                6: "Summer",
                7: "Summer",
                8: "Summer",
                9: "Fall",
                10: "Fall",
                11: "Fall",
            }
        )
        enriched["lead_time_bucket"] = pd.cut(
            enriched["lead_time"],
            bins=[-0.1, 7, 30, 90, float("inf")],
            labels=["0-7", "8-30", "31-90", "91+"],
        )
        return enriched

    def _calculate_property_stats(self) -> pd.DataFrame:
        property_stats = self.main_df.groupby("property_id").agg(
            booked_mean=("booked", "mean"),
            booked_sum=("booked", "sum"),
            booked_count=("booked", "count"),
            booked_std=("booked", "std"),
            price_mean=("price", "mean"),
            price_median=("price", "median"),
            price_std=("price", "std"),
            lead_time_mean=("lead_time", "mean"),
            lead_time_median=("lead_time", "median"),
            event_sum=("event", "sum"),
        )
        return property_stats.fillna({"booked_std": 0.0, "price_std": 0.0})

    def _calculate_temporal_stats(self) -> dict[tuple[str, object], float]:
        temporal_stats: dict[tuple[str, object], float] = {}

        for day, rate in self.main_df.groupby("day_name")["booked"].mean().items():
            temporal_stats[("day_name", day)] = float(rate)

        for month, rate in self.main_df.groupby("month_name")["booked"].mean().items():
            temporal_stats[("month_name", month)] = float(rate)

        for season, rate in self.main_df.groupby("season")["booked"].mean().items():
            temporal_stats[("season", season)] = float(rate)

        weekend_rates = self.main_df.groupby("is_weekend")["booked"].mean()
        temporal_stats[("is_weekend", 0)] = float(weekend_rates.get(0, 0.0))
        temporal_stats[("is_weekend", 1)] = float(weekend_rates.get(1, 0.0))
        return temporal_stats

    def _calculate_event_stats(self) -> pd.DataFrame:
        event_stats = self.main_df.groupby("event").agg(
            booked_mean=("booked", "mean"),
            booked_count=("booked", "count"),
            price_mean=("price", "mean"),
            lead_time_mean=("lead_time", "mean"),
        )
        return event_stats

    def _calculate_lead_time_stats(self) -> pd.Series:
        return self.main_df.groupby("lead_time_bucket", observed=False)["booked"].mean().fillna(0.0)

    def process(self) -> dict[str, object]:
        return {
            "main_df": self.main_df,
            "property_stats": self.property_stats,
            "temporal_stats": self.temporal_stats,
            "event_stats": self.event_stats,
            "lead_time_stats": self.lead_time_stats,
        }

    def get_summary_statistics(self) -> dict[str, object]:
        return {
            "total_records": len(self.main_df),
            "unique_properties": int(self.main_df["property_id"].nunique()),
            "date_range": (self.main_df["date"].min(), self.main_df["date"].max()),
            "overall_booking_rate": float(self.main_df["booked"].mean()),
            "average_price": float(self.main_df["price"].mean()),
            "average_lead_time": float(self.main_df["lead_time"].mean()),
            "event_days_pct": float((self.main_df["event"].mean()) * 100),
        }
