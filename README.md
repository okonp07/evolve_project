# Property DS Case Study

<h1 align="center">Property DS Case Study</h1>

<p align="center">
  <img src="evolve-banner.png" alt="Evolve" width="600"/>
</p>

## Welcome

Thank you for investing your time and considering a role with **Evolve**.  
This case study is designed to simulate a real-world scenario we do at Evolve around **Dynamic Minimum Stays**.

We want to see how you approach ambiguous problems, structure analysis, and communicate insights.

---

## Process

1. We'll align with you on the role and expectations before sending this repo.  
2. You’ll work asynchronously for up to **1 week** (usually 4–6 hours of focused work is sufficient).  
3. You’ll then walk us through your code & findings in a **60‑minute session**:  
   - **10 minutes**: Candidate-led walkthrough of your analysis and solution.  
   - **50 minutes**: Discussion with our data science team about assumptions, design decisions, and extensions.  

This is the only technical/coding round.

---

## Case Study Overview

Evolve helps homeowners maximize rental performance.  
One lever is **minimum stay requirements** (e.g., 2 nights vs. 5 nights). Setting this dynamically based on demand can improve both occupancy and revenue.

**Your task:** Explore the provided dataset and propose a simple framework for **dynamic minimum stays**.

---

## Data

A synthetic dataset is provided here:

```
data/minstay_experiment.csv
```

Columns include:
- `property_id`: Unique property identifier  
- `date`: Calendar date  
- `booked`: 1 if booked, 0 otherwise  
- `price`: Daily rate (USD)  
- `lead_time`: Days between booking date and stay date  
- `event`: Whether there is a local event/holiday (1/0)  

---
## Repository Structure

```
.
├── requirements.txt
├── README.md
├── evolve-banner.png
├── data
│   └── minstay_experiment.csv
├── notebooks
│   ├── eda.ipynb
│   └── analysis.ipynb
├── scripts
│   └── run_analysis.py


```
## Deliverables

- A notebook (`notebooks/analysis.ipynb`) or Python script exploring the dataset.  
- Some **EDA** (exploratory data analysis) around demand patterns.  
- A simple prototype or heuristic for recommending **minimum stays**.  
- A short write‑up of assumptions, limitations, and possible extensions.  

---

## Evaluation

We will evaluate on:  
- **Analytical reasoning** (how you approach the problem)  
- **Clarity** (how results are presented)  
- **Simplicity vs. depth** (balance of rigor and pragmatism)  
- **Communication** (how you explain trade‑offs)  

---

Good luck, and thank you again for your time!  
We’re excited to see your work.
