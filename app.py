def show_about_page():
    # Display banner
    try:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image('evolve-banner.png', use_container_width=True)
    except:
        pass
    
    st.header("About This Application")
    
    st.markdown("""
    ### 🎯 Purpose
    This application provides **dynamic minimum stay recommendations** for vacation rental properties 
    based on historical booking data, market conditions, and property-specific factors.
    
    Built by **Evolve** to help property managers maximize rental performance.
    
    ### 🧠 How It Works
    The recommendation engine analyzes multiple factors:
    
    <div style='background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); 
         padding: 1.5rem; border-radius: 10px; border-left: 4px solid #6B7F3F; margin: 1rem 0;'>
    
    1. **Historical Booking Patterns**: Analyzes past booking rates for similar conditions
    2. **Temporal Features**: Considers day of week, month, and seasonality
    3. **Event Impact**: Accounts for local events and holidays
    4. **Price Sensitivity**: Evaluates pricing relative to booking probability
    5. **Lead Time**: Considers booking window dynamics
    
    </div>
    
    ### 📊 Methodology
    
    The system uses a **rule-based heuristic approach** combined with statistical analysis:
    
    <div style='display: flex; gap: 1rem; margin: 1rem 0;'>
        <div style='flex: 1; background: #6B7F3F; color: white; padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>High Demand</h3>
            <p style='font-size: 2rem; margin: 0.5rem 0; font-weight: 800;'>3-7 nights</p>
            <p style='margin: 0; font-size: 0.9rem;'>Event days, weekends, peak season</p>
        </div>
        <div style='flex: 1; background: #87CEEB; color: white; padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>Medium Demand</h3>
            <p style='font-size: 2rem; margin: 0.5rem 0; font-weight: 800;'>2-4 nights</p>
            import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from recommendation_engine import MinStayRecommender
from data_processor import DataProcessor

# Page configuration
st.set_page_config(
    page_title="Evolve - Minimum Stay Recommender",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Evolve branding
st.markdown("""
    <style>
    /* Import Manrope font */
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
    
    /* Evolve brand colors */
    :root {
        --evolve-olive: #6B7F3F;
        --evolve-sky-blue: #87CEEB;
        --evolve-grey: #6C757D;
        --evolve-light-grey: #F8F9FA;
        --evolve-dark-grey: #343A40;
    }
    
    /* Apply Manrope font globally */
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--evolve-olive);
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Manrope', sans-serif;
    }
    
    .sub-header {
        font-size: 1.2rem;
        font-weight: 500;
        color: var(--evolve-grey);
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Manrope', sans-serif;
    }
    
    /* Banner container */
    .banner-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(135deg, var(--evolve-light-grey) 0%, #ffffff 100%);
        border-radius: 10px;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, var(--evolve-light-grey) 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid var(--evolve-olive);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton>button {
        background-color: var(--evolve-olive);
        color: white;
        font-family: 'Manrope', sans-serif;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #5a6b35;
        box-shadow: 0 4px 8px rgba(107, 127, 63, 0.3);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--evolve-light-grey) 0%, #ffffff 100%);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        font-family: 'Manrope', sans-serif;
        font-weight: 600;
        color: var(--evolve-dark-grey);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Manrope', sans-serif;
        color: var(--evolve-olive);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Manrope', sans-serif;
        font-weight: 600;
        background-color: var(--evolve-light-grey);
        border-radius: 8px 8px 0 0;
        color: var(--evolve-grey);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--evolve-olive);
        color: white;
    }
    
    /* Info boxes */
    .stAlert {
        font-family: 'Manrope', sans-serif;
        border-left: 4px solid var(--evolve-sky-blue);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
        color: var(--evolve-olive);
    }
    
    /* Select boxes and inputs */
    .stSelectbox label, .stDateInput label, .stNumberInput label, .stSlider label, .stCheckbox label {
        font-family: 'Manrope', sans-serif;
        font-weight: 600;
        color: var(--evolve-dark-grey);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background-color: var(--evolve-olive);
    }
    
    /* Dataframe styling */
    .dataframe {
        font-family: 'Manrope', sans-serif;
    }
    
    /* Success boxes */
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid var(--evolve-olive);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-family: 'Manrope', sans-serif;
    }
    
    /* Recommendation result box */
    .recommendation-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 2px solid var(--evolve-olive);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(107, 127, 63, 0.2);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, var(--evolve-olive) 0%, var(--evolve-sky-blue) 50%, var(--evolve-grey) 100%);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the dataset"""
    try:
        df = pd.read_csv('data/minstay_experiment.csv', parse_dates=['date'])
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'data/minstay_experiment.csv' exists.")
        return None

@st.cache_resource
def initialize_recommender(df):
    """Initialize and cache the recommendation engine"""
    processor = DataProcessor(df)
    processed_data = processor.process()
    recommender = MinStayRecommender(processed_data)
    recommender.train()
    return recommender, processor

def main():
    # Display Evolve banner
    try:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image('evolve-banner.png', use_container_width=True)
    except FileNotFoundError:
        st.markdown('<div class="banner-container"><h1>🏠 EVOLVE</h1></div>', unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">Dynamic Minimum Stay Recommender</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Data-driven recommendations for optimal rental performance</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Initialize recommender
    with st.spinner("Initializing recommendation engine..."):
        recommender, processor = initialize_recommender(df)
    
    # Sidebar
    st.sidebar.image('evolve-banner.png', use_container_width=True) if Path('evolve-banner.png').exists() else None
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio("Select Page", ["🎯 Get Recommendation", "📊 Analytics Dashboard", "ℹ️ About"])
    
    # Add branding footer to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align: center; color: #6B7F3F; font-weight: 600;'>
        Powered by Evolve
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    if page == "🎯 Get Recommendation":
        show_recommendation_page(df, recommender, processor)
    elif page == "📊 Analytics Dashboard":
        show_analytics_page(df, processor)
    else:
        show_about_page()

def show_recommendation_page(df, recommender, processor):
    st.header("Get Minimum Stay Recommendation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Parameters")
        
        # Property selection
        property_ids = sorted(df['property_id'].unique())
        selected_property = st.selectbox(
            "Select Property ID",
            property_ids,
            help="Choose a property from the dataset"
        )
        
        # Date selection
        min_date = df['date'].min()
        max_date = df['date'].max()
        selected_date = st.date_input(
            "Select Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            help="Choose a date for the recommendation"
        )
        
        # Convert to datetime
        selected_date = pd.to_datetime(selected_date)
        
        # Event checkbox
        has_event = st.checkbox(
            "Local Event/Holiday",
            help="Check if there's a local event or holiday"
        )
        
        # Price input
        property_avg_price = df[df['property_id'] == selected_property]['price'].mean()
        price = st.number_input(
            "Price per Night ($)",
            min_value=0.0,
            value=float(property_avg_price),
            step=10.0,
            help="Enter the nightly rate"
        )
        
        # Lead time
        lead_time = st.slider(
            "Lead Time (days)",
            min_value=0,
            max_value=180,
            value=30,
            help="Days between booking and check-in"
        )
        
        # Get recommendation button
        if st.button("Get Recommendation", type="primary"):
            with st.spinner("Calculating optimal minimum stay..."):
                recommendation = recommender.predict(
                    property_id=selected_property,
                    date=selected_date,
                    price=price,
                    lead_time=lead_time,
                    event=1 if has_event else 0
                )
                
                st.session_state['recommendation'] = recommendation
    
    with col2:
        st.subheader("Recommendation Results")
        
        if 'recommendation' in st.session_state:
            rec = st.session_state['recommendation']
            
            # Main recommendation in styled box
            st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
            st.markdown("### 🎯 Recommended Minimum Stay")
            st.markdown(
                f"<h1 style='text-align: center; color: #6B7F3F; font-weight: 800; font-size: 4rem;'>{rec['min_stay']} nights</h1>", 
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Confidence and reasoning
            st.markdown("### 📈 Confidence Score")
            confidence = rec.get('confidence', 0.75)
            st.progress(confidence)
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                st.write(f"**{confidence:.1%}** confidence level")
            with col_conf2:
                if confidence >= 0.8:
                    st.success("High confidence")
                elif confidence >= 0.65:
                    st.info("Medium confidence")
                else:
                    st.warning("Lower confidence")
            
            st.markdown("### 💡 Reasoning")
            for reason in rec.get('reasoning', []):
                st.markdown(f"<div style='padding: 0.5rem; margin: 0.3rem 0; background-color: #f8f9fa; border-left: 3px solid #87CEEB; border-radius: 5px;'>• {reason}</div>", unsafe_allow_html=True)
            
            # Additional insights
            st.markdown("### 📊 Market Context")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Expected Booking Rate", f"{rec.get('booking_rate', 0):.1%}", 
                         delta=None, delta_color="normal")
            with col_b:
                demand_level = rec.get('demand_level', 'Medium')
                if demand_level == "High":
                    st.metric("Market Demand", demand_level, delta="Strong", delta_color="normal")
                elif demand_level in ["Medium-High", "Medium"]:
                    st.metric("Market Demand", demand_level, delta="Moderate", delta_color="off")
                else:
                    st.metric("Market Demand", demand_level, delta="Weak", delta_color="inverse")
            
            # Strategy tips in branded box
            st.markdown("### 💼 Strategy Tip")
            st.markdown(
                f"""
                <div style='background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); 
                     border-left: 4px solid #6B7F3F; padding: 1rem; border-radius: 8px; 
                     margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                {rec.get('strategy_tip', 'Adjust pricing and minimum stay based on market conditions.')}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("👈 Enter parameters and click 'Get Recommendation' to see results")
            
            # Show property stats
            property_stats = df[df['property_id'] == selected_property].agg({
                'booked': 'mean',
                'price': 'mean',
                'lead_time': 'mean'
            })
            
            st.markdown("### Property Statistics")
            st.write(f"**Historical Booking Rate:** {property_stats['booked']:.1%}")
            st.write(f"**Average Price:** ${property_stats['price']:.2f}")
            st.write(f"**Average Lead Time:** {property_stats['lead_time']:.0f} days")

def show_analytics_page(df, processor):
    st.header("Analytics Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📈 Overall Trends", "🏘️ Property Analysis", "📅 Temporal Patterns"])
    
    # Evolve brand colors for charts
    evolve_colors = ['#6B7F3F', '#87CEEB', '#6C757D', '#8BA85C', '#A4D4F4']
    
    with tab1:
        st.subheader("Overall Booking Trends")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Booking Rate", f"{df['booked'].mean():.1%}")
        with col2:
            st.metric("Average Price", f"${df['price'].mean():.2f}")
        with col3:
            st.metric("Total Properties", f"{df['property_id'].nunique():,}")
        
        # Booking rate over time
        daily_stats = df.groupby('date').agg({
            'booked': 'mean',
            'price': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_stats['date'],
            y=daily_stats['booked'],
            mode='lines',
            name='Booking Rate',
            line=dict(color='#6B7F3F', width=2)
        ))
        fig.update_layout(
            title="Daily Booking Rate Over Time",
            xaxis_title="Date",
            yaxis_title="Booking Rate",
            height=400,
            font=dict(family="Manrope, sans-serif"),
            plot_bgcolor='#F8F9FA'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Event impact
        st.subheader("Event Impact Analysis")
        event_comparison = df.groupby('event')['booked'].mean()
        
        fig = px.bar(
            x=['No Event', 'Event'],
            y=event_comparison.values,
            labels={'x': 'Event Status', 'y': 'Booking Rate'},
            title="Booking Rate: Event vs Non-Event Days",
            color=event_comparison.values,
            color_continuous_scale=[[0, '#6C757D'], [1, '#6B7F3F']]
        )
        fig.update_layout(
            font=dict(family="Manrope, sans-serif"),
            plot_bgcolor='#F8F9FA'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Property-Level Analysis")
        
        # Property performance
        property_stats = df.groupby('property_id').agg({
            'booked': 'mean',
            'price': 'mean'
        }).reset_index()
        
        fig = px.scatter(
            property_stats,
            x='price',
            y='booked',
            title="Property Performance: Price vs Booking Rate",
            labels={'price': 'Average Price ($)', 'booked': 'Booking Rate'},
            color='booked',
            color_continuous_scale=[[0, '#6C757D'], [0.5, '#87CEEB'], [1, '#6B7F3F']]
        )
        fig.update_layout(
            font=dict(family="Manrope, sans-serif"),
            plot_bgcolor='#F8F9FA'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top performers
        top_properties = property_stats.nlargest(10, 'booked')
        st.subheader("Top 10 Properties by Booking Rate")
        st.dataframe(
            top_properties.style.format({
                'booked': '{:.1%}',
                'price': '${:.2f}'
            }).background_gradient(cmap='Greens', subset=['booked']),
            use_container_width=True
        )
    
    with tab3:
        st.subheader("Temporal Patterns")
        
        # Day of week analysis
        df['day_of_week'] = df['date'].dt.day_name()
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_stats = df.groupby('day_of_week')['booked'].mean().reindex(dow_order)
        
        fig = px.bar(
            x=dow_stats.index,
            y=dow_stats.values,
            title="Booking Rate by Day of Week",
            labels={'x': 'Day of Week', 'y': 'Booking Rate'},
            color=dow_stats.values,
            color_continuous_scale=[[0, '#6C757D'], [0.5, '#87CEEB'], [1, '#6B7F3F']]
        )
        fig.update_layout(
            font=dict(family="Manrope, sans-serif"),
            plot_bgcolor='#F8F9FA'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly patterns
        df['month'] = df['date'].dt.month_name()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        month_stats = df.groupby('month')['booked'].mean().reindex(month_order)
        
        fig = px.line(
            x=month_stats.index,
            y=month_stats.values,
            title="Booking Rate by Month",
            labels={'x': 'Month', 'y': 'Booking Rate'},
            markers=True
        )
        fig.update_traces(line_color='#6B7F3F', marker=dict(color='#87CEEB', size=10))
        fig.update_layout(
            font=dict(family="Manrope, sans-serif"),
            plot_bgcolor='#F8F9FA'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_about_page():
    st.header("About This Application")
    
    st.markdown("""
    ### 🎯 Purpose
    This application provides **dynamic minimum stay recommendations** for vacation rental properties 
    based on historical booking data, market conditions, and property-specific factors.
    
    ### 🧠 How It Works
    The recommendation engine analyzes multiple factors:
    
    1. **Historical Booking Patterns**: Analyzes past booking rates for similar conditions
    2. **Temporal Features**: Considers day of week, month, and seasonality
    3. **Event Impact**: Accounts for local events and holidays
    4. **Price Sensitivity**: Evaluates pricing relative to booking probability
    5. **Lead Time**: Considers booking window dynamics
    
    ### 📊 Methodology
    
    The system uses a **rule-based heuristic approach** combined with statistical analysis:
    
    - **High Demand (3-7 nights)**: Event days, weekends, peak season
    - **Medium Demand (2-4 nights)**: Shoulder season, mid-week with good lead time
    - **Low Demand (1-2 nights)**: Off-season, last-minute bookings, low historical rates
    
    ### 🔧 Key Features
    
    - ✅ Real-time minimum stay recommendations
    - ✅ Property-specific analysis
    - ✅ Market demand insights
    - ✅ Interactive analytics dashboard
    - ✅ Historical performance tracking
    
    ### 📈 Benefits
    
    - **Maximize Revenue**: Optimize minimum stays for peak demand periods
    - **Improve Occupancy**: Reduce minimum stays during low demand
    - **Data-Driven Decisions**: Base strategies on actual booking patterns
    - **Flexible Strategy**: Adapt to market conditions dynamically
    
    ### 👥 Target Users
    
    - Property managers
    - Vacation rental hosts
    - Revenue management teams
    - Real estate investors
    
    ### 📝 Limitations & Assumptions
    
    - Based on historical data patterns
    - Assumes past trends indicate future behavior
    - Does not account for external market disruptions
    - Recommendations should be validated with local market knowledge
    
    ### 🚀 Future Enhancements
    
    - Machine learning models for improved accuracy
    - Competitor pricing integration
    - Multi-property portfolio optimization
    - API integration with property management systems
    - A/B testing framework
    
    ---
    
    ### 📧 Contact & Support
    
    For questions or feedback about this application, please reach out to your data science team.
    
    **Version**: 1.0.0  
    **Last Updated**: October 2025
    """)
    
    with st.expander("📚 Technical Details"):
        st.markdown("""
        **Technologies Used:**
        - **Frontend**: Streamlit
        - **Data Processing**: Pandas, NumPy
        - **Visualization**: Plotly
        - **Deployment**: Streamlit Cloud
        
        **Data Requirements:**
        - Property ID
        - Date
        - Booking status
        - Price
        - Lead time
        - Event indicator
        
        **Algorithm Overview:**
        1. Feature engineering from raw data
        2. Statistical aggregation by property and temporal features
        3. Rule-based classification of demand levels
        4. Minimum stay assignment based on demand tier
        5. Confidence scoring based on historical variance
        """)

if __name__ == "__main__":
    main()
