# CLOUDY&SHINY INDEX - AGENT CONTEXT
> **Role**: You are the Market Sentiment Analyst for the Fear & Greed module.

---

## 📊 MODULE: Global Fear & Greed Index
**Code**: CSI | **Division**: MCFI (Financial Intelligence) | **Status**: STANDBY

---

## 🎯 OBJECTIVE

Create a unified "Monarch Global Mood" score by aggregating sentiment from stocks, crypto, and volatility indices. Normalize all inputs to 0-100 scale.

---

## 📁 FILES TO CREATE

| File | Purpose |
|------|---------|
| `sentiment_tracker.py` | Data fetching from all sources |
| `app.py` | Streamlit visualization |
| `sentiment_data.csv` | Historical mood scores |
| `requirements.txt` | Dependencies |

---

## 🔧 IMPLEMENTATION REQUIREMENTS

### 1. Data Sources
```python
# Source A: CNN Fear & Greed Index (scrape or API)
# Source B: Crypto Fear & Greed from alternative.me API
# Source C: VIX from yfinance (^VIX)
```

### 2. The Algorithm
```python
# Normalize all to 0-100
# Weighted average:
# (Stock * 0.4) + (Crypto * 0.3) + ((100 - VIX_normalized) * 0.3)
```

### 3. Result Interpretation
- 0-20: ☁️ STORMY (Extreme Fear)
- 21-80: 🌤️ CLOUDY (Neutral)
- 81-100: ☀️ SHINY (Extreme Greed)

### 4. Visualization
- Large Gauge/Speedometer chart
- 3 smaller trend lines for components
- 7-day historical view

---

## 🚀 RUN COMMANDS

```bash
# Fetch sentiment data
python sentiment_tracker.py

# Launch dashboard
streamlit run app.py
```

---

## 🔗 INTEGRATION

Register with AI Director in `AI_COMMAND/director.py` when ready.

---

**Priority**: Phase 3 | **Dependencies**: yfinance, requests, plotly