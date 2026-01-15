# BALTIC DRY-GROWTH PREDICTION - AGENT CONTEXT
> **Role**: You are the Economic Forecasting Analyst for the Baltic Dry Index module.

---

## 📊 MODULE: Trade Wind Economic Predictor
**Code**: BDI | **Division**: MCFI (Financial Intelligence) | **Status**: STANDBY

---

## 🎯 OBJECTIVE

Correlate the Baltic Dry Index (shipping prices) with Global GDP indicators to predict economic slowdowns. The BDI is a leading indicator - shipping costs drop before recessions hit.

---

## 📁 FILES TO CREATE

| File | Purpose |
|------|---------|
| `baltic_predictor.py` | Main forecasting script |
| `correlation_analysis.py` | Statistical correlation engine |
| `bdi_data.csv` | Historical and current data |
| `requirements.txt` | Dependencies |

---

## 🔧 IMPLEMENTATION REQUIREMENTS

### 1. Data Ingestion
```python
# Use yfinance to fetch:
# - Baltic Dry Index (^BDI or BDRY ETF proxy)
# - S&P 500 (^GSPC) as economic health proxy
# Timeframe: Last 5 years
```

### 2. Time Lag Analysis
```python
# Shift BDI data forward by 3 months
# Calculate correlation coefficient between:
# "BDI 3 months ago" vs "S&P 500 Today"
```

### 3. Visualization
- Dual-axis line chart
- Left Axis: Baltic Dry Index
- Right Axis: S&P 500
- Highlight "Crossover" points (shipping drops before market)

---

## 🚀 RUN COMMANDS

```bash
# When implemented:
python baltic_predictor.py
```

---

## 🔗 INTEGRATION

Once implemented, register with AI Director in `AI_COMMAND/director.py`.

---

**Priority**: Phase 3 | **Dependencies**: yfinance, pandas, plotly