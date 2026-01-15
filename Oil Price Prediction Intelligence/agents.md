# OIL PRICE PREDICTION - AGENT CONTEXT
> **Role**: You are the Commodities Forecasting Analyst for the Oil module.

---

## 📊 MODULE: Black Gold Oracle
**Code**: OPI | **Division**: MCFI (Financial Intelligence) | **Status**: STANDBY

---

## 🎯 OBJECTIVE

Create a time-series forecasting model for Brent Crude Oil prices using Facebook Prophet. Generate 90-day predictions with confidence intervals.

---

## 📁 FILES TO CREATE

| File | Purpose |
|------|---------|
| `oil_predictor.py` | Prophet forecasting script |
| `oil_data.csv` | Historical price data |
| `forecast.csv` | Generated predictions |
| `requirements.txt` | Dependencies |

---

## 🔧 IMPLEMENTATION REQUIREMENTS

### 1. Data Ingestion
```python
import yfinance as yf

# Brent Crude Oil Futures
oil = yf.download("BZ=F", period="5y")
```

### 2. Prophet Model
```python
from prophet import Prophet

# Prepare data for Prophet (ds, y columns)
df = oil[['Close']].reset_index()
df.columns = ['ds', 'y']

# Fit model
model = Prophet()
model.fit(df)

# Forecast 90 days
future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)
```

### 3. Visualization
- Historical prices: Black dots
- Predicted prices: Blue line
- Confidence interval: Shaded blue area
- Key metric: "Predicted Price in 30 Days: $XX.XX"

---

## 🚀 RUN COMMANDS

```bash
# Generate forecast
python oil_predictor.py

# View in dashboard
streamlit run ../dashboard.py
```

---

## 📈 OUTPUT

Display:
- Current price vs 30-day prediction
- Trend direction (↑ or ↓)
- Confidence range

---

## ⚠️ DISCLAIMER

Oil predictions are for informational purposes only. High volatility means wide confidence intervals.

---

## 🔗 INTEGRATION

Add as new tab in `dashboard.py` when implemented.

---

**Priority**: Phase 3 | **Dependencies**: yfinance, prophet, plotly