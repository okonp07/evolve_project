from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_processor import DataProcessor
from src.recommendation_engine import MinStayRecommender


DATA_PATH = Path("data/minstay_experiment.csv")
BRAND = {
    "olive": "#6B7F3F",
    "sky": "#87CEEB",
    "grey": "#6C757D",
    "light": "#F8F9FA",
    "dark": "#343A40",
}


st.set_page_config(
    page_title="Evolve - Minimum Stay Recommender",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Manrope', sans-serif;
        }}

        .main-title {{
            font-size: 2.7rem;
            font-weight: 800;
            color: {BRAND["olive"]};
            margin-bottom: 0.3rem;
        }}

        .sub-title {{
            color: {BRAND["grey"]};
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }}

        .hero-card {{
            padding: 1.5rem;
            border-radius: 16px;
            background: linear-gradient(135deg, {BRAND["light"]} 0%, #ffffff 100%);
            border: 1px solid rgba(107, 127, 63, 0.18);
            box-shadow: 0 10px 30px rgba(52, 58, 64, 0.06);
        }}

        .result-card {{
            padding: 1.5rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(107, 127, 63, 0.10) 0%, rgba(135, 206, 235, 0.12) 100%);
            border: 2px solid rgba(107, 127, 63, 0.28);
            margin-top: 1rem;
        }}

        .metric-chip {{
            display: inline-block;
            padding: 0.35rem 0.7rem;
            margin: 0.2rem 0.2rem 0 0;
            border-radius: 999px;
            background: {BRAND["light"]};
            border: 1px solid rgba(107, 127, 63, 0.18);
            color: {BRAND["dark"]};
            font-size: 0.9rem;
            font-weight: 600;
        }}

        .reason-list {{
            margin: 0.5rem 0 0 0;
            padding-left: 1.2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing dataset at {DATA_PATH}")
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


@st.cache_resource
def initialize_engine() -> tuple[MinStayRecommender, DataProcessor]:
    processor = DataProcessor(load_data())
    processed = processor.process()
    recommender = MinStayRecommender(processed)
    recommender.train()
    return recommender, processor


def show_banner() -> None:
    banner_path = Path("evolve-banner.png")
    if banner_path.exists():
        st.image(str(banner_path), use_column_width=True)


def metric_row(processor: DataProcessor) -> None:
    summary = processor.get_summary_statistics()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Properties", f"{summary['unique_properties']:,}")
    col2.metric("Rows", f"{summary['total_records']:,}")
    col3.metric("Booking Rate", f"{summary['overall_booking_rate']:.1%}")
    col4.metric("Event Share", f"{summary['event_days_pct']:.1f}%")


def show_home(recommender: MinStayRecommender, processor: DataProcessor) -> None:
    st.markdown("<div class='main-title'>Dynamic Minimum Stay Recommender</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>Property-level minimum stay recommendations grounded in historical booking behavior, seasonality, events, lead time, and pricing context.</div>",
        unsafe_allow_html=True,
    )
    metric_row(processor)

    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    left, right = st.columns([1.2, 1])

    with left:
        properties = recommender.available_properties()
        default_property = properties[0]
        property_id = st.selectbox("Property", properties, index=0)
        date_value = st.date_input(
            "Target stay date",
            value=recommender.default_target_date(),
            min_value=recommender.min_date().date(),
            max_value=recommender.max_date().date(),
        )
        event_flag = st.checkbox("Local event / holiday", value=False)

    with right:
        property_context = recommender.property_context(default_property if property_id is None else property_id)
        nightly_price = st.number_input(
            "Nightly price (USD)",
            min_value=0.0,
            value=float(round(property_context["price_mean"], 2)),
            step=5.0,
        )
        lead_time = st.slider("Lead time (days until check-in)", min_value=0, max_value=180, value=21)

        st.markdown(
            "".join(
                [
                    f"<span class='metric-chip'>Market avg booking rate: {recommender.market_booking_rate():.1%}</span>",
                    f"<span class='metric-chip'>Property avg booking rate: {property_context['booking_rate']:.1%}</span>",
                    f"<span class='metric-chip'>Typical nightly price: ${property_context['price_mean']:.0f}</span>",
                ]
            ),
            unsafe_allow_html=True,
        )

    if st.button("Get Recommendation", use_container_width=True):
        result = recommender.recommend(
            property_id=property_id,
            target_date=pd.Timestamp(date_value),
            price=nightly_price,
            lead_time=lead_time,
            event=event_flag,
        )
        demand_color = {
            "Low": BRAND["grey"],
            "Medium": BRAND["sky"],
            "High": BRAND["olive"],
        }[result["demand_level"]]
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <h2 style="margin-bottom:0.3rem;">Recommended Minimum Stay: {result['recommended_min_stay']} night(s)</h2>
            <div style="font-size:1rem;color:{BRAND['dark']};">
                Demand level: <strong style="color:{demand_color};">{result['demand_level']}</strong> |
                Confidence: <strong>{result['confidence_pct']}%</strong> |
                Demand score: <strong>{result['demand_score']}</strong>/100
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(result["demand_score"] / 100)
        st.write(result["summary"])
        st.markdown("**Why this recommendation**")
        st.markdown(
            "<ul class='reason-list'>" + "".join(f"<li>{reason}</li>" for reason in result["reasons"]) + "</ul>",
            unsafe_allow_html=True,
        )
        st.markdown("**Strategy tips**")
        for tip in result["strategy_tips"]:
            st.write(f"- {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def show_analytics(recommender: MinStayRecommender, processor: DataProcessor) -> None:
    st.header("Analytics Dashboard")
    tabs = st.tabs(["Overall Trends", "Property Analysis", "Temporal Patterns"])
    data = processor.main_df

    with tabs[0]:
        booking_trend = (
            data.groupby("date", as_index=False)
            .agg(booking_rate=("booked", "mean"), avg_price=("price", "mean"), event_rate=("event", "mean"))
        )
        fig = px.line(
            booking_trend,
            x="date",
            y="booking_rate",
            title="Booking Rate Over Time",
            color_discrete_sequence=[BRAND["olive"]],
        )
        fig.update_layout(yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

        event_compare = data.groupby("event", as_index=False)["booked"].mean()
        event_compare["event_label"] = event_compare["event"].map({0: "Non-event", 1: "Event"})
        fig = px.bar(
            event_compare,
            x="event_label",
            y="booked",
            title="Event Impact on Booking Rate",
            color="event_label",
            color_discrete_sequence=[BRAND["grey"], BRAND["sky"]],
        )
        fig.update_layout(showlegend=False, yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        property_stats = processor.property_stats.reset_index()
        top_n = st.slider("Properties to compare", 5, 25, 10)
        ranked = property_stats.nlargest(top_n, "booked_mean")
        fig = px.bar(
            ranked.sort_values("booked_mean"),
            x="booked_mean",
            y="property_id",
            orientation="h",
            title="Top Properties by Historical Booking Rate",
            color="price_mean",
            color_continuous_scale=["#d5dde5", BRAND["olive"]],
        )
        fig.update_layout(xaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

        selected_property = st.selectbox(
            "Inspect property history",
            recommender.available_properties(),
            key="analytics_property",
        )
        property_history = data.loc[data["property_id"] == selected_property].sort_values("date")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=property_history["date"],
                y=property_history["booked"].rolling(14, min_periods=1).mean(),
                name="14-day booking rate",
                line=dict(color=BRAND["olive"], width=3),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=property_history["date"],
                y=property_history["price"],
                name="Nightly price",
                yaxis="y2",
                line=dict(color=BRAND["sky"], width=2),
            )
        )
        fig.update_layout(
            title=f"Property {selected_property}: Booking Rate and Price",
            yaxis=dict(title="Booking rate", tickformat=".0%"),
            yaxis2=dict(title="Price", overlaying="y", side="right"),
            legend=dict(orientation="h"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        day_rates = data.groupby("day_name", as_index=False)["booked"].mean()
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_rates["day_name"] = pd.Categorical(day_rates["day_name"], categories=day_order, ordered=True)
        day_rates = day_rates.sort_values("day_name")
        fig = px.bar(
            day_rates,
            x="day_name",
            y="booked",
            title="Booking Rate by Day of Week",
            color_discrete_sequence=[BRAND["olive"]],
        )
        fig.update_layout(showlegend=False, yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

        month_rates = data.groupby("month_name", as_index=False)["booked"].mean()
        month_order = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        month_rates["month_name"] = pd.Categorical(month_rates["month_name"], categories=month_order, ordered=True)
        month_rates = month_rates.sort_values("month_name")
        fig = px.line(
            month_rates,
            x="month_name",
            y="booked",
            title="Booking Rate by Month",
            markers=True,
            color_discrete_sequence=[BRAND["sky"]],
        )
        fig.update_layout(yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

        heatmap_df = (
            data.groupby(["day_name", "event"], as_index=False)["booked"]
            .mean()
            .pivot(index="day_name", columns="event", values="booked")
            .reindex(day_order)
        )
        fig = px.imshow(
            heatmap_df,
            labels=dict(x="Event", y="Day of week", color="Booking rate"),
            title="Booking Rate by Day and Event Presence",
            color_continuous_scale=["#eef2f5", BRAND["olive"]],
            aspect="auto",
        )
        fig.update_xaxes(
            tickvals=[0, 1],
            ticktext=["No event", "Event"],
        )
        st.plotly_chart(fig, use_container_width=True)


def show_about(processor: DataProcessor, recommender: MinStayRecommender) -> None:
    st.header("About This Application")
    st.write(
        "This Streamlit app turns historical booking data into practical minimum-stay guidance for property managers."
    )
    st.markdown(
        """
        ### Methodology
        The recommender uses a hybrid scoring system that mirrors the product README:

        - Property performance contributes **40%** of the score.
        - Temporal patterns contribute **30%**.
        - Event impact contributes **15%**.
        - Lead time contributes **10%**.
        - Price competitiveness contributes **5%**.

        The final demand score is translated into low, medium, or high demand, then mapped to a minimum-stay policy.
        """
    )

    st.subheader("Decision Rules")
    st.write(
        """
        - High demand (`>= 70`): set stricter minimum stays to capture premium demand.
        - Medium demand (`40-69`): balance occupancy with revenue using moderate minimum stays.
        - Low demand (`< 40`): reduce restrictions to fill nights and improve occupancy.
        """
    )

    st.subheader("Data Summary")
    summary = processor.get_summary_statistics()
    st.json(
        {
            "date_range": [summary["date_range"][0].date().isoformat(), summary["date_range"][1].date().isoformat()],
            "properties": summary["unique_properties"],
            "records": summary["total_records"],
            "overall_booking_rate": round(summary["overall_booking_rate"], 4),
            "average_price": round(summary["average_price"], 2),
        }
    )

    st.subheader("Scoring Weights")
    weights = recommender.weights
    st.dataframe(
        pd.DataFrame(
            [{"factor": key.replace("_", " ").title(), "weight_pct": int(value * 100)} for key, value in weights.items()]
        ),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    inject_styles()
    show_banner()
    try:
        recommender, processor = initialize_engine()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    page = st.sidebar.radio(
        "Navigate",
        ["🎯 Get Recommendation", "📊 Analytics Dashboard", "ℹ️ About"],
    )

    if page == "🎯 Get Recommendation":
        show_home(recommender, processor)
    elif page == "📊 Analytics Dashboard":
        show_analytics(recommender, processor)
    else:
        show_about(processor, recommender)


if __name__ == "__main__":
    main()
