from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class MinStayRecommender:
    """Hybrid heuristic recommender for dynamic minimum stays."""

    processed_data: dict[str, object]
    weights: dict[str, float] = field(
        default_factory=lambda: {
            "property_performance": 0.40,
            "temporal_patterns": 0.30,
            "event_impact": 0.15,
            "lead_time": 0.10,
            "price_competitiveness": 0.05,
        }
    )

    def train(self) -> None:
        self.main_df = self.processed_data["main_df"]
        self.property_stats = self.processed_data["property_stats"]
        self.temporal_stats = self.processed_data["temporal_stats"]
        self.event_stats = self.processed_data["event_stats"]
        self.lead_time_stats = self.processed_data["lead_time_stats"]
        self._market_booking_rate = float(self.main_df["booked"].mean())

        self._property_percentiles = self.property_stats["booked_mean"].rank(pct=True)
        self._price_percentiles = self.property_stats["price_mean"].rank(pct=True)

    def available_properties(self) -> list[int]:
        return sorted(self.property_stats.index.tolist())

    def min_date(self) -> pd.Timestamp:
        return pd.Timestamp(self.main_df["date"].min())

    def max_date(self) -> pd.Timestamp:
        return pd.Timestamp(self.main_df["date"].max())

    def default_target_date(self) -> pd.Timestamp:
        return self.min_date()

    def market_booking_rate(self) -> float:
        return self._market_booking_rate

    def property_context(self, property_id: int) -> dict[str, float]:
        row = self.property_stats.loc[property_id]
        return {
            "booking_rate": float(row["booked_mean"]),
            "price_mean": float(row["price_mean"]),
            "price_std": float(row["price_std"]),
            "sample_size": int(row["booked_count"]),
        }

    def recommend(
        self,
        property_id: int,
        target_date: pd.Timestamp,
        price: float,
        lead_time: int,
        event: bool,
    ) -> dict[str, object]:
        target_date = pd.Timestamp(target_date)
        property_row = self.property_stats.loc[property_id]
        month_name = target_date.month_name()
        day_name = target_date.day_name()
        is_weekend = int(target_date.dayofweek in (4, 5))

        factor_scores = {
            "property_performance": self._property_score(property_id),
            "temporal_patterns": self._temporal_score(day_name, month_name, is_weekend),
            "event_impact": self._event_score(bool(event)),
            "lead_time": self._lead_time_score(lead_time),
            "price_competitiveness": self._price_score(float(price), float(property_row["price_mean"])),
        }

        demand_score = round(sum(factor_scores[key] * self.weights[key] for key in self.weights))
        demand_level = self._demand_level(demand_score)
        recommended_min_stay = self._minimum_stay(demand_score, bool(event), is_weekend, lead_time)
        confidence_pct = self._confidence(property_row, target_date, bool(event))

        reasons = self._build_reasons(
            property_row=property_row,
            target_date=target_date,
            factor_scores=factor_scores,
            event=bool(event),
            lead_time=lead_time,
            price=float(price),
        )

        summary = (
            f"For property {property_id}, the target date lands in a {demand_level.lower()}-demand scenario. "
            f"The score is driven by the property's historical performance, {day_name.lower()} / {month_name.lower()} seasonality, "
            f"{'event-driven uplift' if event else 'normal market conditions'}, and a lead time of {lead_time} days."
        )

        strategy_tips = self._strategy_tips(demand_level, recommended_min_stay, bool(event), lead_time)

        return {
            "property_id": property_id,
            "target_date": target_date.date().isoformat(),
            "demand_score": int(np.clip(demand_score, 0, 100)),
            "demand_level": demand_level,
            "recommended_min_stay": recommended_min_stay,
            "confidence_pct": confidence_pct,
            "reasons": reasons,
            "summary": summary,
            "strategy_tips": strategy_tips,
            "factor_scores": factor_scores,
        }

    def _property_score(self, property_id: int) -> float:
        percentile = float(self._property_percentiles.loc[property_id])
        return float(np.clip(percentile * 100, 5, 100))

    def _temporal_score(self, day_name: str, month_name: str, is_weekend: int) -> float:
        day_rate = self.temporal_stats.get(("day_name", day_name), self._market_booking_rate)
        month_rate = self.temporal_stats.get(("month_name", month_name), self._market_booking_rate)
        weekend_rate = self.temporal_stats.get(("is_weekend", is_weekend), self._market_booking_rate)
        normalized = np.mean(
            [
                day_rate / self._market_booking_rate,
                month_rate / self._market_booking_rate,
                weekend_rate / self._market_booking_rate,
            ]
        )
        return float(np.clip(normalized * 50, 0, 100))

    def _event_score(self, event: bool) -> float:
        event_rate = float(self.event_stats["booked_mean"].get(1, self._market_booking_rate))
        non_event_rate = float(self.event_stats["booked_mean"].get(0, self._market_booking_rate))
        if not event:
            baseline = non_event_rate / self._market_booking_rate
            return float(np.clip(baseline * 50, 0, 100))
        uplift = event_rate / max(non_event_rate, 1e-6)
        return float(np.clip(55 + (uplift - 1.0) * 45, 0, 100))

    def _lead_time_score(self, lead_time: int) -> float:
        if lead_time <= 7:
            bucket = "0-7"
        elif lead_time <= 30:
            bucket = "8-30"
        elif lead_time <= 90:
            bucket = "31-90"
        else:
            bucket = "91+"
        rate = float(self.lead_time_stats.get(bucket, self._market_booking_rate))
        return float(np.clip((rate / self._market_booking_rate) * 50, 0, 100))

    def _price_score(self, price: float, property_mean_price: float) -> float:
        if property_mean_price <= 0:
            return 50.0
        ratio = price / property_mean_price
        score = 65 - abs(ratio - 1.0) * 60
        return float(np.clip(score, 10, 95))

    def _demand_level(self, demand_score: int) -> str:
        if demand_score >= 70:
            return "High"
        if demand_score >= 40:
            return "Medium"
        return "Low"

    def _minimum_stay(self, demand_score: int, event: bool, is_weekend: int, lead_time: int) -> int:
        if demand_score >= 90:
            return 7 if event and is_weekend else 6
        if demand_score >= 82:
            return 5
        if demand_score >= 70:
            return 4
        if demand_score >= 55:
            return 3
        if demand_score >= 40:
            return 2
        if lead_time <= 3 and not event:
            return 1
        return 2

    def _confidence(self, property_row: pd.Series, target_date: pd.Timestamp, event: bool) -> int:
        sample_component = min(25, int(property_row["booked_count"] / 20))
        variability_penalty = min(10, int(float(property_row["booked_std"]) * 20))
        temporal_matches = self.main_df[
            (self.main_df["property_id"] == property_row.name)
            & (self.main_df["month"] == target_date.month)
            & (self.main_df["is_weekend"] == int(target_date.dayofweek in (4, 5)))
            & (self.main_df["event"] == int(event))
        ]
        context_component = min(15, len(temporal_matches))
        confidence = 55 + sample_component + context_component - variability_penalty
        return int(np.clip(confidence, 60, 85))

    def _build_reasons(
        self,
        property_row: pd.Series,
        target_date: pd.Timestamp,
        factor_scores: dict[str, float],
        event: bool,
        lead_time: int,
        price: float,
    ) -> list[str]:
        reasons = []
        reasons.append(
            f"Property history is {'above' if property_row['booked_mean'] >= self._market_booking_rate else 'below'} market average at {property_row['booked_mean']:.1%} booked."
        )
        reasons.append(
            f"{target_date.day_name()} and {target_date.month_name()} patterns contribute a temporal score of {round(factor_scores['temporal_patterns'])}/100."
        )
        if event:
            reasons.append("Event demand is active, so the score receives an uplift to protect higher-value booking windows.")
        else:
            reasons.append("No event uplift is applied, so the recommendation leans more on base demand and property history.")
        reasons.append(
            f"A lead time of {lead_time} days produces a lead-time score of {round(factor_scores['lead_time'])}/100 based on similar historical windows."
        )
        reasons.append(
            f"The entered price of ${price:,.0f} is compared with the property's average price of ${property_row['price_mean']:,.0f}."
        )
        return reasons

    def _strategy_tips(self, demand_level: str, min_stay: int, event: bool, lead_time: int) -> list[str]:
        tips = []
        if demand_level == "High":
            tips.append("Keep a firmer minimum stay to protect revenue and reduce operational turnover.")
        elif demand_level == "Medium":
            tips.append("Use a balanced restriction and monitor pickup as the stay date approaches.")
        else:
            tips.append("Loosen restrictions to capture shorter bookings and fill occupancy gaps.")

        if event:
            tips.append("Review nearby event calendars to confirm there is still enough premium demand to justify the restriction.")
        if lead_time <= 7:
            tips.append("Because check-in is close, be ready to relax the rule if pickup remains soft.")
        else:
            tips.append("Reassess the recommendation weekly as more bookings materialize and lead time compresses.")
        tips.append(f"A {min_stay}-night minimum is a starting policy, not a hard-coded rule for all future dates.")
        return tips
