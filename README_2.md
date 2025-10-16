# 🏠 Evolve - Dynamic Minimum Stay Recommender

<p align="center">
  <img src="evolve-banner.png" alt="Evolve" width="600"/>
</p>

<p align="center">
  <strong>A data-driven Streamlit application for optimizing vacation rental minimum stay requirements</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#demo">Demo</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#deployment">Deployment</a> •
  <a href="#methodology">Methodology</a> •
  <a href="#contributing">Contributing</a>
</p>

---

## 📋 Overview

The **Evolve Minimum Stay Recommender** is an intelligent system designed to help vacation rental property managers optimize their minimum stay requirements based on real-time market conditions, historical booking patterns, and property-specific factors. By analyzing multiple data points, the system provides actionable recommendations that balance occupancy rates with revenue optimization.

### 🎯 Key Benefits

- **Maximize Revenue**: Set optimal minimum stays during peak demand periods
- **Improve Occupancy**: Reduce restrictions during low-demand periods
- **Data-Driven Decisions**: Base strategies on actual booking patterns
- **Dynamic Flexibility**: Adapt to changing market conditions
- **Time Savings**: Automated recommendations reduce manual analysis

---

## ✨ Features

### 🎯 **Intelligent Recommendations**
- Real-time minimum stay suggestions (1-7 nights)
- Property-specific analysis and personalization
- Confidence scoring for each recommendation
- Detailed reasoning and market context

### 📊 **Comprehensive Analytics Dashboard**
- Overall booking trends visualization
- Property-level performance comparison
- Temporal pattern analysis (daily, weekly, monthly)
- Event impact assessment
- Interactive charts with Evolve brand colors

### 🎨 **Professional UI/UX**
- Clean, modern interface with Evolve branding
- Olive green, sky blue, and grey color scheme
- Manrope font family for readability
- Mobile-responsive design
- Intuitive navigation

### 🧠 **Advanced Analysis**
- Multi-factor demand scoring (0-100 scale)
- Historical pattern recognition
- Seasonality detection
- Lead time optimization
- Price sensitivity analysis

---

## 🚀 Demo

### Live Application
Visit the live demo: `https://[your-app-name].streamlit.app` (after deployment)

### Screenshots

**Get Recommendation Page:**
- Select property, date, and parameters
- Receive instant minimum stay recommendation
- View confidence scores and detailed reasoning

**Analytics Dashboard:**
- Explore booking trends over time
- Compare property performance
- Analyze temporal patterns

**About Page:**
- Learn about the methodology
- Understand the algorithm
- Review technical details

---

## 📁 Repository Structure

```
minstay-recommender/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── DEPLOYMENT.md                   # Detailed deployment guide
├── QUICKSTART.md                   # Quick start guide
├── .gitignore                      # Git ignore rules
├── evolve-banner.png              # Evolve branding banner
│
├── .streamlit/
│   └── config.toml                # Streamlit configuration (brand colors)
│
├── src/
│   ├── __init__.py                # Package initializer
│   ├── recommendation_engine.py   # Core recommendation logic
│   └── data_processor.py          # Data processing utilities
│
├── data/
│   └── minstay_experiment.csv     # Training dataset
│
├── notebooks/
│   ├── eda.ipynb                  # Exploratory data analysis
│   └── analysis.ipynb             # Additional analysis
│
└── tests/
    ├── __init__.py                # Test package initializer
    └── test_recommender.py        # Unit tests
```

---

## 🔧 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** package manager
- **Git** (for version control)
- 4GB RAM minimum (8GB recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/minstay-recommender.git
cd minstay-recommender
```

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Add Your Data

Place your `minstay_experiment.csv` file in the `data/` directory:

```bash
cp /path/to/your/minstay_experiment.csv data/
```

**Required CSV columns:**
- `property_id`: Unique property identifier (integer)
- `date`: Calendar date (YYYY-MM-DD format)
- `booked`: Booking status (0 or 1)
- `price`: Daily rate in USD (float)
- `lead_time`: Days between booking and stay (float)
- `event`: Local event/holiday indicator (0 or 1)

### Step 5: Verify Installation

```bash
# Run tests
pytest tests/ -v

# Start the application
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

---

## 💻 Usage

### Running Locally

```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start the application
streamlit run app.py
```

The app will automatically open in your default browser.

### Getting a Recommendation

1. **Navigate** to "🎯 Get Recommendation" page
2. **Select** a property from the dropdown
3. **Choose** a target date
4. **Configure** parameters:
   - Check "Local Event/Holiday" if applicable
   - Adjust price per night
   - Set lead time (days until check-in)
5. **Click** "Get Recommendation"
6. **Review** the results:
   - Recommended minimum stay (1-7 nights)
   - Confidence score (60-85%)
   - Demand level (Low/Medium/High)
   - Detailed reasoning
   - Strategy tips

### Exploring Analytics

1. **Navigate** to "📊 Analytics Dashboard"
2. **Choose** a tab:
   - **Overall Trends**: Booking rates over time, event impact
   - **Property Analysis**: Performance comparison, top performers
   - **Temporal Patterns**: Day of week, monthly trends
3. **Interact** with charts (hover, zoom, pan)
4. **Export** data or screenshots as needed

### Understanding Results

**Minimum Stay Values:**
- `1 night`: Low demand, maximize occupancy
- `2-3 nights`: Medium demand, balanced approach
- `4-7 nights`: High demand, maximize revenue

**Confidence Levels:**
- `80-85%`: High confidence, strong historical data
- `65-80%`: Medium confidence, moderate data
- `60-65%`: Lower confidence, limited data

**Demand Levels:**
- `High`: Strong market conditions, set higher minimums
- `Medium`: Balanced conditions, moderate minimums
- `Low`: Weak conditions, reduce minimums

---

## ☁️ Deployment

### Streamlit Cloud (Recommended)

**Benefits:**
- ✅ Free hosting
- ✅ Automatic HTTPS
- ✅ Auto-redeploy on git push
- ✅ Easy setup (5 minutes)

**Steps:**

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/minstay-recommender.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Wait 2-5 minutes** for deployment to complete

4. **Access your app** at `https://[your-app-name].streamlit.app`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Alternative Deployment Options

- **Heroku**: See [Heroku deployment guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- **Docker**: Create Dockerfile and deploy to any container platform
- **AWS/GCP/Azure**: Deploy on cloud VMs or container services
- **Local Network**: Run on internal server for team access

---

## 🧠 Methodology

### Algorithm Overview

The recommendation system uses a **hybrid approach** combining:

1. **Rule-Based Heuristics**: Proven business logic for minimum stay decisions
2. **Statistical Analysis**: Historical data patterns and trends
3. **Multi-Factor Scoring**: Weighted evaluation of multiple variables

### Demand Scoring (0-100)

The system calculates a composite demand score based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Property Performance | 40% | Historical booking rate vs. market average |
| Temporal Patterns | 30% | Day of week (15%) + Month/Season (15%) |
| Event Impact | 15% | Presence of local events/holidays |
| Lead Time | 10% | Booking window optimization |
| Price Competitiveness | 5% | Price positioning relative to property average |

### Decision Rules

**High Demand (Score ≥70):**
- Minimum stay: 3-7 nights
- Conditions: Events, weekends, peak season
- Strategy: Maximize revenue per booking

**Medium Demand (Score 40-69):**
- Minimum stay: 2-3 nights
- Conditions: Shoulder season, mid-week
- Strategy: Balance occupancy and revenue

**Low Demand (Score <40):**
- Minimum stay: 1-2 nights
- Conditions: Off-season, last-minute, low historical rates
- Strategy: Maximize occupancy

### Key Factors Analyzed

1. **Historical Booking Patterns**
   - Property-specific booking rates
   - Market-wide trends
   - Seasonal variations

2. **Temporal Features**
   - Day of week effects
   - Monthly seasonality
   - Weekend vs. weekday patterns

3. **Event Impact**
   - Local events and holidays
   - Historical event performance
   - Event booking premiums

4. **Lead Time Dynamics**
   - Optimal booking windows
   - Last-minute vs. advance bookings
   - Lead time correlations

5. **Price Sensitivity**
   - Price-demand relationships
   - Competitive positioning
   - Price elasticity

### Confidence Scoring

Confidence levels are determined by:
- Historical data volume and quality
- Variance in past booking patterns
- Presence of similar historical scenarios
- Data recency and relevance

---

## 📊 Data Requirements

### Input Data Format

**CSV File:** `minstay_experiment.csv`

**Required Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `property_id` | Integer | Unique property identifier | 1001 |
| `date` | Date | Calendar date | 2024-07-15 |
| `booked` | Binary | Booking status (0=No, 1=Yes) | 1 |
| `price` | Float | Nightly rate in USD | 250.00 |
| `lead_time` | Float | Days between booking and stay | 30.0 |
| `event` | Binary | Event/holiday indicator (0=No, 1=Yes) | 1 |

**Data Quality Guidelines:**
- Minimum 30 days of historical data per property
- Complete records (no missing values in key columns)
- Consistent date formatting (YYYY-MM-DD)
- Prices in USD (or consistent currency)
- Lead time in days (can be 0 for same-day bookings)

### Sample Data

```csv
property_id,date,booked,price,lead_time,event
1001,2024-01-01,1,250.00,30.0,1
1001,2024-01-02,0,225.00,15.0,0
1002,2024-01-01,1,180.00,45.0,1
```

---

## 🧪 Testing

### Run Unit Tests

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_recommender.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

The test suite covers:
- ✅ Data processing and validation
- ✅ Feature engineering
- ✅ Recommendation logic
- ✅ Edge cases and error handling
- ✅ Integration tests

### Manual Testing Checklist

- [ ] App loads without errors
- [ ] Data loads successfully
- [ ] All pages navigate correctly
- [ ] Property selection works
- [ ] Date picker functions properly
- [ ] Recommendations generate correctly
- [ ] Charts display properly
- [ ] Mobile responsive design works

---

## 🎨 Customization

### Brand Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#6B7F3F"      # Evolve olive green
backgroundColor="#FFFFFF"    # White
secondaryBackgroundColor="#F8F9FA"  # Light grey
textColor="#343A40"         # Dark grey
```

### Fonts

The app uses **Manrope** font family. To change:

1. Update the `@import` statement in `app.py`
2. Modify the `font-family` CSS properties

### Banner

Replace `evolve-banner.png` with your own logo:
- Recommended size: 1200x300 pixels
- Format: PNG with transparent background
- Location: Root directory

### Recommendation Logic

Modify `src/recommendation_engine.py`:
- Adjust demand thresholds
- Change weighting factors
- Add custom rules
- Modify minimum stay ranges

---

## 🔒 Security & Privacy

### Data Privacy

- All data processing happens **locally** or on your chosen platform
- No data is sent to external services without your consent
- CSV data remains in your control

### Best Practices

1. **Sensitive Data**: Use `.gitignore` for sensitive files
2. **Secrets Management**: Use Streamlit secrets for API keys
3. **Access Control**: Deploy privately on Streamlit Teams if needed
4. **Data Encryption**: Use HTTPS (automatic on Streamlit Cloud)

### Environment Variables

For sensitive configuration, use Streamlit secrets:

**`.streamlit/secrets.toml` (local only, not committed):**
```toml
[data]
csv_url = "https://secure-url/data.csv"
api_key = "your-api-key-here"
```

Access in app:
```python
import streamlit as st
csv_url = st.secrets["data"]["csv_url"]
```

---

## 📈 Performance Optimization

### Caching

The app uses Streamlit caching for optimal performance:

```python
@st.cache_data  # Cache data loading
def load_data():
    return pd.read_csv('data.csv')

@st.cache_resource  # Cache models
def initialize_recommender():
    return MinStayRecommender()
```

### Large Datasets

For datasets >100MB:
- Use data sampling for initial load
- Implement pagination
- Host data externally (S3, GCS)
- Use database instead of CSV

### Memory Management

- Limit concurrent users on free tier
- Optimize data types (use int8, float32 where possible)
- Clear cache periodically
- Monitor resource usage

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Module not found errors**
```bash
Solution: pip install -r requirements.txt
```

**Issue: Data file not found**
```bash
Solution: Verify data/minstay_experiment.csv exists
```

**Issue: Streamlit Cloud deployment fails**
```bash
Solution: Check requirements.txt for correct versions
```

**Issue: App runs slowly**
```bash
Solution: Add @st.cache_data decorators, reduce data size
```

**Issue: Charts not displaying**
```bash
Solution: Check Plotly installation, verify data format
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

1. Check [Streamlit Documentation](https://docs.streamlit.io)
2. Visit [Streamlit Forum](https://discuss.streamlit.io)
3. Review [GitHub Issues](https://github.com/YOUR_USERNAME/minstay-recommender/issues)
4. Contact Evolve support team

---

## 🛣️ Roadmap

### Version 1.1 (Q1 2025)
- [ ] Machine learning model integration
- [ ] A/B testing framework
- [ ] Multi-property bulk recommendations
- [ ] Export to CSV/PDF reports

### Version 1.2 (Q2 2025)
- [ ] API integration with PMS systems
- [ ] Competitor pricing data
- [ ] Advanced forecasting models
- [ ] Mobile app version

### Version 2.0 (Q3 2025)
- [ ] Real-time market data integration
- [ ] Portfolio optimization
- [ ] Automated rule execution
- [ ] Advanced analytics suite

---

## 👥 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Write tests for new features
5. Run tests: `pytest tests/ -v`
6. Commit changes: `git commit -m "Add feature"`
7. Push to branch: `git push origin feature-name`
8. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Include unit tests
- Update documentation
- Keep commits atomic and well-described

### Code Review Process

1. Automated tests must pass
2. Code review by maintainer
3. Documentation review
4. Merge approval

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Evolve

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

### Built With

- [Streamlit](https://streamlit.io/) - Web application framework
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [NumPy](https://numpy.org/) - Numerical computing
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pytest](https://pytest.org/) - Testing framework

### Fonts & Design

- **Manrope** font by Mikhail Sharanda
- Evolve brand guidelines
- Streamlit design system

### Inspiration

- Vacation rental industry best practices
- Revenue management strategies
- Data science community

---

## 📞 Contact & Support

### Evolve Team

- **Website**: [www.evolve.com](https://www.evolve.com)
- **Email**: support@evolve.com
- **GitHub**: [@evolve](https://github.com/evolve)

### Project Maintainers

- **Lead Developer**: Your Name
- **Data Science**: DS Team
- **Product**: Product Team

### Community

- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/minstay-recommender/discussions)
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/minstay-recommender/issues)
- **Slack**: #minstay-recommender (internal)

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/minstay-recommender)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/minstay-recommender)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/minstay-recommender)
![License](https://img.shields.io/github/license/YOUR_USERNAME/minstay-recommender)
![Python version](https://img.shields.io/badge/python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

---

<p align="center">
  Made with ❤️ by <strong>Evolve</strong>
</p>

<p align="center">
  <sub>Helping property managers optimize performance through data-driven insights</sub>
</p>

---

**Version**: 1.0.0  
**Last Updated**: October 2025  
**Status**: Production Ready ✅
