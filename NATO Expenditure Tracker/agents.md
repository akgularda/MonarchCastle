# NATO EXPENDITURE TRACKER - AGENT CONTEXT
> **Role**: You are the Defense Economics Analyst for the NATO module.

---

## 📊 MODULE: NATO Burden Tracker
**Code**: NATO | **Division**: MCDI (Defense Intelligence) | **Status**: ACTIVE LIVE

---

## 🎯 OBJECTIVE

Compare NATO member defense spending against the 2% GDP target. Identify "Surplus" and "Deficit" nations.

---

## 📁 FILES TO CREATE

| File | Purpose |
|------|---------|
| `nato_data.csv` | Defense spending data |
| `nato_tracker.py` | Analysis script |
| `requirements.txt` | Dependencies |

---

## 🔧 IMPLEMENTATION REQUIREMENTS

### 1. Data Structure
```csv
Country,Defence_Spending_Billions,Percent_GDP,Population
USA,886.0,3.5,331000000
UK,68.5,2.3,67000000
Germany,55.0,1.5,83000000
```
*Source: NATO Secretary General's Annual Report*

### 2. Analysis
```python
# Calculate spending per capita
per_capita = spending / population

# Categorize countries
if percent_gdp >= 2.0:
    category = "SURPLUS"  # Green
else:
    category = "DEFICIT"  # Red
```

### 3. Visualization
- Bar chart sorted by % GDP
- Color coded: Green (>2%), Red (<2%)
- Scatter plot: GDP Total vs Defense Spending
- Highlight 2% threshold line

---

## 🚀 RUN COMMANDS

```bash
# Generate analysis
python nato_tracker.py

# View in dashboard
streamlit run ../dashboard.py
```

---

## 📊 KEY METRICS

- Total NATO spending
- Average % GDP
- Countries meeting target
- Countries below target
- Spending gap to reach 2%

---

## 🔗 INTEGRATION

Add as new tab in `dashboard.py` when implemented.

---

**Priority**: Phase 3 | **Dependencies**: pandas, plotly