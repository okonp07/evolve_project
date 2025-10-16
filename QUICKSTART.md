# 🚀 Quick Start Guide

Get your Minimum Stay Recommender app up and running in under 15 minutes!

## ⚡ Fast Track (5 Steps)

### 1️⃣ Setup Repository (2 minutes)

**Option A: Automated (Recommended)**
```bash
# Download and run setup script
curl -O https://[your-url]/setup.sh
chmod +x setup.sh
./setup.sh

# On Windows, use setup.bat instead
```

**Option B: Manual**
```bash
mkdir minstay-recommender && cd minstay-recommender
mkdir -p .streamlit src data notebooks tests
touch src/__init__.py tests/__init__.py
```

### 2️⃣ Copy Code Files (3 minutes)

Copy content from provided artifacts into these files:

| File | Content From |
|------|-------------|
| `app.py` | Main Streamlit Application |
| `requirements.txt` | Dependencies |
| `src/recommendation_engine.py` | Core Logic |
| `src/data_processor.py` | Data Processing |
| `.streamlit/config.toml` | Configuration |
| `README.md` | Documentation |
| `.gitignore` | Git Ignore |

**Quick copy template:**
```bash
# For each file, create and paste content
cat > app.py << 'EOF'
[paste app.py content here]
EOF
```

### 3️⃣ Add Your Data (1 minute)

```bash
# Copy your CSV file
cp /path/to/minstay_experiment.csv data/

# Verify it's there
ls -lh data/minstay_experiment.csv
```

### 4️⃣ Test Locally (3 minutes)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

Visit http://localhost:8501 - App should load!

### 5️⃣ Deploy to Streamlit Cloud (6 minutes)

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/minstay-recommender.git
git branch -M main
git push -u origin main

# Deploy on Streamlit Cloud:
# 1. Visit https://share.streamlit.io
# 2. Sign in with GitHub
# 3. Click "New app"
# 4. Select your repository
# 5. Set main file: app.py
# 6. Click "Deploy"
```

Done! 🎉 Your app is live!

---

## 🔍 Verification Checklist

After deployment, verify:

- [ ] App URL loads: `https://your-app.streamlit.app`
- [ ] No errors on page load
- [ ] Can navigate between pages
- [ ] Can select property and date
- [ ] "Get Recommendation" button works
- [ ] Analytics dashboard displays charts
- [ ] About page loads

---

## 🐛 Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Import errors | Check all files in correct folders |
| Data not found | Verify `data/minstay_experiment.csv` exists |
| Module not found | Run `pip install -r requirements.txt` |
| App won't start | Check Python version (need 3.8+) |
| Slow performance | Add `@st.cache_data` decorators |

---

## 📚 Full Documentation

For detailed instructions, see:
- **README.md** - Complete documentation
- **DEPLOYMENT.md** - Step-by-step deployment guide

---

## 🆘 Need Help?

1. Check [Streamlit Docs](https://docs.streamlit.io)
2. Review deployment logs on Streamlit Cloud
3. Check GitHub repository settings
4. Visit [Streamlit Forum](https://discuss.streamlit.io)

---

**Time to deployment: ~15 minutes**  
**Difficulty: Easy** 🟢

Good luck! 🚀
