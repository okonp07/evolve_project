from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_processor import DataProcessor
from src.recommendation_engine import MinStayRecommender


DATA_PATH = Path("data/minstay_experiment.csv")
AUTHOR_IMAGE_PATH = Path("assets/okon_prince.png")
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

        [data-testid="stAppViewContainer"] {{
            background:
                radial-gradient(circle at top left, rgba(135, 206, 235, 0.20), transparent 28%),
                radial-gradient(circle at top right, rgba(107, 127, 63, 0.18), transparent 24%),
                linear-gradient(180deg, #fcfdfb 0%, #f4f7f2 48%, #eef4f8 100%);
        }}

        [data-testid="stAppViewContainer"] .main .block-container {{
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }}

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(180deg, rgba(107, 127, 63, 0.12) 0%, rgba(255, 255, 255, 0.96) 30%),
                #ffffff;
            border-right: 1px solid rgba(107, 127, 63, 0.14);
        }}

        [data-testid="stSidebar"] .stRadio > div {{
            gap: 0.45rem;
        }}

        [data-testid="stSidebar"] label p {{
            font-weight: 700;
            color: {BRAND["dark"]};
        }}

        [data-testid="stMetric"] {{
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(107, 127, 63, 0.12);
            border-radius: 18px;
            padding: 0.85rem 1rem;
            box-shadow: 0 12px 28px rgba(52, 58, 64, 0.05);
        }}

        [data-testid="stMetricLabel"] p {{
            font-weight: 700;
            color: {BRAND["grey"]};
        }}

        .main-title {{
            font-size: 3rem;
            font-weight: 800;
            color: {BRAND["olive"]};
            margin-bottom: 0.35rem;
            letter-spacing: -0.04em;
        }}

        .sub-title {{
            color: {BRAND["grey"]};
            font-size: 1.08rem;
            margin-bottom: 1.35rem;
            max-width: 720px;
        }}

        .eyebrow {{
            display: inline-block;
            padding: 0.35rem 0.75rem;
            margin-bottom: 0.8rem;
            border-radius: 999px;
            background: rgba(107, 127, 63, 0.10);
            color: {BRAND["olive"]};
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .hero-shell {{
            position: relative;
            overflow: hidden;
            padding: 1.5rem;
            border-radius: 28px;
            background:
                radial-gradient(circle at top right, rgba(135, 206, 235, 0.26), transparent 28%),
                linear-gradient(135deg, rgba(255, 255, 255, 0.96) 0%, rgba(248, 249, 250, 0.98) 100%);
            border: 1px solid rgba(107, 127, 63, 0.16);
            box-shadow: 0 18px 40px rgba(52, 58, 64, 0.07);
            margin-bottom: 1.25rem;
        }}

        .result-card {{
            padding: 1.6rem;
            border-radius: 24px;
            background:
                radial-gradient(circle at top right, rgba(255,255,255,0.65), transparent 26%),
                linear-gradient(135deg, rgba(107, 127, 63, 0.12) 0%, rgba(135, 206, 235, 0.18) 100%);
            border: 1px solid rgba(107, 127, 63, 0.22);
            margin-top: 1rem;
            box-shadow: 0 16px 34px rgba(52, 58, 64, 0.08);
        }}

        .hero-card {{
            padding: 1.2rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(107, 127, 63, 0.12);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
        }}

        .hero-kicker {{
            color: {BRAND["grey"]};
            font-size: 0.95rem;
            margin-bottom: 0.25rem;
        }}

        .hero-value {{
            font-size: 2.1rem;
            font-weight: 800;
            color: {BRAND["dark"]};
            line-height: 1;
        }}

        .hero-caption {{
            margin-top: 0.4rem;
            color: {BRAND["grey"]};
            font-size: 0.92rem;
        }}

        .metric-chip {{
            display: inline-block;
            padding: 0.45rem 0.8rem;
            margin: 0.2rem 0.2rem 0 0;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(107, 127, 63, 0.14);
            color: {BRAND["dark"]};
            font-size: 0.9rem;
            font-weight: 700;
        }}

        .reason-list {{
            margin: 0.5rem 0 0 0;
            padding-left: 1.2rem;
        }}

        .section-card {{
            padding: 1.2rem 1.3rem;
            border-radius: 22px;
            background: rgba(255,255,255,0.82);
            border: 1px solid rgba(107, 127, 63, 0.12);
            box-shadow: 0 12px 28px rgba(52,58,64,0.05);
            margin-bottom: 1rem;
        }}

        .section-title {{
            font-size: 1.25rem;
            font-weight: 800;
            color: {BRAND["olive"]};
            margin-bottom: 0.25rem;
        }}

        .section-copy {{
            color: {BRAND["grey"]};
            margin-bottom: 0;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin: 1rem 0 1.2rem 0;
        }}

        .info-box {{
            padding: 1rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.82);
            border: 1px solid rgba(107, 127, 63, 0.10);
        }}

        .info-box strong {{
            display: block;
            color: {BRAND["dark"]};
            margin-bottom: 0.25rem;
        }}

        .info-box span {{
            color: {BRAND["grey"]};
            font-size: 0.92rem;
        }}

        .author-card {{
            padding: 1.35rem;
            border-radius: 24px;
            background: linear-gradient(180deg, rgba(255,255,255,0.94) 0%, rgba(246,249,247,0.96) 100%);
            border: 1px solid rgba(107, 127, 63, 0.14);
            box-shadow: 0 16px 34px rgba(52,58,64,0.06);
        }}

        .author-image-wrap {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100%;
        }}

        .author-heading {{
            font-size: 1.25rem;
            font-weight: 800;
            color: {BRAND["olive"]};
            margin-bottom: 0.85rem;
        }}

        .author-name {{
            font-size: 2rem;
            font-weight: 800;
            color: {BRAND["dark"]};
            margin-bottom: 0.3rem;
            letter-spacing: -0.03em;
        }}

        .author-role {{
            color: {BRAND["olive"]};
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }}

        .author-copy {{
            color: {BRAND["dark"]};
            font-size: 1rem;
            line-height: 1.7;
            margin-bottom: 0.9rem;
        }}

        .stack-chip {{
            display: inline-block;
            padding: 0.42rem 0.78rem;
            margin: 0.18rem 0.22rem 0 0;
            border-radius: 999px;
            background: rgba(107, 127, 63, 0.08);
            border: 1px solid rgba(107, 127, 63, 0.12);
            color: {BRAND["dark"]};
            font-size: 0.88rem;
            font-weight: 700;
        }}

        .footer-block {{
            margin-top: 2.6rem;
            padding: 1.35rem 1rem 0.4rem 1rem;
            border-top: 1px solid rgba(107, 127, 63, 0.16);
            text-align: center;
            color: {BRAND["grey"]};
            font-size: 0.92rem;
            line-height: 1.8;
        }}

        .footer-block strong {{
            color: {BRAND["dark"]};
        }}

        @media (max-width: 900px) {{
            .main-title {{
                font-size: 2.35rem;
            }}

            .info-grid {{
                grid-template-columns: 1fr;
            }}
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
    st.markdown("<div class='eyebrow'>Revenue Optimization</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>Dynamic Minimum Stay Recommender</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>Property-level minimum stay recommendations grounded in historical booking behavior, seasonality, events, lead time, and pricing context.</div>",
        unsafe_allow_html=True,
    )
    metric_row(processor)

    market_rate = recommender.market_booking_rate()
    st.markdown(
        f"""
        <div class='hero-shell'>
          <div class='info-grid'>
            <div class='hero-card'>
              <div class='hero-kicker'>Portfolio coverage</div>
              <div class='hero-value'>{len(recommender.available_properties())}</div>
              <div class='hero-caption'>Active, priced properties available for recommendations</div>
            </div>
            <div class='hero-card'>
              <div class='hero-kicker'>Market booking rate</div>
              <div class='hero-value'>{market_rate:.1%}</div>
              <div class='hero-caption'>Portfolio-wide baseline used in the demand score</div>
            </div>
            <div class='hero-card'>
              <div class='hero-kicker'>Decision mode</div>
              <div class='hero-value'>Hybrid</div>
              <div class='hero-caption'>Business heuristics blended with historical demand patterns</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-title'>Build A Recommendation</div><p class='section-copy'>Choose a property, target date, and booking context to generate a practical minimum-stay policy.</p>",
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.2, 1])
    properties = recommender.available_properties()
    default_property = properties[0]

    if "selected_property" not in st.session_state or st.session_state["selected_property"] not in properties:
        st.session_state["selected_property"] = default_property

    def sync_property_defaults() -> None:
        property_context = recommender.property_context(st.session_state["selected_property"])
        st.session_state["nightly_price"] = float(round(property_context["price_mean"], 2))

    if "nightly_price" not in st.session_state:
        sync_property_defaults()

    with left:
        property_id = st.selectbox(
            "Property",
            properties,
            index=properties.index(st.session_state["selected_property"]),
            key="selected_property",
            on_change=sync_property_defaults,
        )
        date_value = st.date_input(
            "Target stay date",
            value=recommender.default_target_date(),
            min_value=recommender.min_date().date(),
            max_value=recommender.max_date().date(),
        )
        event_flag = st.checkbox("Local event / holiday", value=False)

    with right:
        property_context = recommender.property_context(property_id)
        nightly_price = st.number_input(
            "Nightly price (USD)",
            min_value=0.0,
            key="nightly_price",
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
    st.markdown("<div class='eyebrow'>Portfolio Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>Explore how booking behavior changes across time, events, and individual properties.</div>",
        unsafe_allow_html=True,
    )
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
    st.markdown("<div class='eyebrow'>Methodology</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>About</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>This page explains the project clearly, the logic behind the solution, and the author behind the work.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='section-card'>
          <div class='section-title'>What This Project Is About</div>
          <p class='section-copy'>This project is an interactive decision-support application built to recommend dynamic minimum stays for vacation rental properties. Instead of relying on a single static rule for every property and every date, the app evaluates each booking scenario in context and recommends a minimum-stay policy that better matches expected demand.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='section-card'>
          <div class='section-title'>Project Overview</div>
          <p class='author-copy'>
            The core business problem behind the app is simple: minimum-stay requirements should not be fixed all the time.
            On strong demand dates, longer minimum stays can protect revenue and reduce operational turnover. On weaker dates,
            shorter minimum stays can improve occupancy and help fill inventory that might otherwise go unused.
          </p>
          <p class='author-copy'>
            This application turns that idea into a practical workflow. A user selects a property, chooses a target stay date,
            specifies whether a local event is happening, and adjusts the booking context with nightly price and lead time.
            The system then produces a recommendation that includes the suggested minimum stay, a demand score, a confidence
            score, and a clear explanation of the reasoning behind the result.
          </p>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='section-card'>
          <div class='section-title'>How The Solution Works</div>
          <p class='author-copy'>
            The solution uses a hybrid, interpretable framework. The pipeline begins by validating and cleaning the raw booking
            data. It then engineers time-aware features such as day of week, month, seasonality, weekend behavior, and
            lead-time buckets so that the demand context for each property-date combination can be described in a meaningful way.
          </p>
          <p class='author-copy'>
            Once the data is prepared, the recommendation engine calculates five interpretable components: property performance,
            temporal demand patterns, event uplift, lead-time behavior, and price competitiveness. These components are combined
            into a weighted demand score from 0 to 100. That score is then translated into a demand tier and, finally, into a
            recommended minimum-stay policy.
          </p>
          <p class='author-copy'>
            The design is intentionally explainable. This means the app does not just output a number. It also explains why the
            recommendation was made, what parts of the demand profile influenced it, and how a property manager can interpret
            that recommendation operationally.
          </p>
          <p class='author-copy'>
            In practice, the app works as both an analytics product and a decision-support tool. It helps users understand the
            relationship between booking behavior and demand while also giving them a simple, operationally useful recommendation
            they can apply immediately.
          </p>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='section-card'>
          <div class='section-title'>Decision Logic At A Glance</div>
          <div class='info-grid'>
            <div class='info-box'><strong>40%</strong><span>Property performance and historical booking strength</span></div>
            <div class='info-box'><strong>30%</strong><span>Temporal demand patterns across weekdays, weekends, and seasonality</span></div>
            <div class='info-box'><strong>15%</strong><span>Event and holiday uplift</span></div>
            <div class='info-box'><strong>10%</strong><span>Lead-time behavior and booking-window dynamics</span></div>
            <div class='info-box'><strong>5%</strong><span>Price competitiveness versus the property's normal level</span></div>
            <div class='info-box'><strong>Output</strong><span>Demand tier, confidence, narrative explanation, and minimum-stay policy</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Decision Rules")
    st.write(
        """
        - High demand (`>= 70`): set stricter minimum stays to capture premium demand and protect higher-value booking windows.
        - Medium demand (`40-69`): balance occupancy and revenue with moderate restrictions and flexible decision-making.
        - Low demand (`< 40`): reduce restrictions to improve occupancy, fill weaker dates, and remove unnecessary friction.
        """
    )

    st.subheader("Data Summary")
    summary = processor.get_summary_statistics()
    col1, col2 = st.columns([1.1, 0.9])
    with col1:
        st.markdown(
            f"""
            <div class='section-card'>
              <div class='section-title'>Dataset Snapshot</div>
              <div class='info-grid'>
                <div class='info-box'><strong>{summary["unique_properties"]:,}</strong><span>properties</span></div>
                <div class='info-box'><strong>{summary["total_records"]:,}</strong><span>rows</span></div>
                <div class='info-box'><strong>{summary["overall_booking_rate"]:.1%}</strong><span>booking rate</span></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
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

    col1, col2 = st.columns([0.92, 1.45], gap="large")
    with col1:
        if AUTHOR_IMAGE_PATH.exists():
            st.markdown("<div class='author-image-wrap'>", unsafe_allow_html=True)
            inner_left, inner_center, inner_right = st.columns([0.08, 0.84, 0.08])
            with inner_center:
                st.image(str(AUTHOR_IMAGE_PATH), use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            """
            <div class='author-card'>
              <div class='author-heading'>About The Author</div>
              <div class='author-name'>Okon Prince</div>
              <div class='author-role'>Senior Data Scientist at MIVA Open University | AI Engineer &amp; Data Scientist</div>
              <p class='author-copy'>I design and deploy end-to-end data systems that turn raw data into production-ready intelligence.</p>
              <p class='author-copy'>My core stack includes Python, Streamlit, BigQuery, Supabase, Hugging Face, PySpark, SQL, Machine Learning, LLMs, and Transformers.</p>
              <p class='author-copy'>My work spans risk scoring systems, A/B testing, AI-powered dashboards, RAG pipelines, predictive analytics, and LLM-based solutions and AI research.</p>
              <p class='author-copy'>Currently, I work as a Senior Data Scientist at MIVA Open University, building intelligent systems that drive analytics, decision support, and scalable AI innovation.</p>
              <p class='author-copy'><strong>I believe:</strong> models are trained, systems are engineered, impact is delivered.</p>
              <div>
                <span class='stack-chip'>Python</span>
                <span class='stack-chip'>Streamlit</span>
                <span class='stack-chip'>BigQuery</span>
                <span class='stack-chip'>Supabase</span>
                <span class='stack-chip'>Hugging Face</span>
                <span class='stack-chip'>PySpark</span>
                <span class='stack-chip'>SQL</span>
                <span class='stack-chip'>Machine Learning</span>
                <span class='stack-chip'>LLMs</span>
                <span class='stack-chip'>Transformers</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    st.markdown(
        """
        <div class='footer-block'>
          <div><strong>© Okon Prince, 2026</strong></div>
          <div>This project is based on the data.org Financial Health Prediction Zindi challenge.</div>
          <div>enquiries; okonp07@gmail.com, +234(0)9020000299</div>
        </div>
        """,
        unsafe_allow_html=True,
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
        ["Get Recommendation", "Analytics Dashboard", "About"],
    )

    if page == "Get Recommendation":
        show_home(recommender, processor)
    elif page == "Analytics Dashboard":
        show_analytics(recommender, processor)
    else:
        show_about(processor, recommender)

    render_footer()


if __name__ == "__main__":
    main()
