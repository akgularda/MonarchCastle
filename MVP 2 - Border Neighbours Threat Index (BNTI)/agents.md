# BORDER NEIGHBOURS THREAT INDEX - AGENT CONTEXT
> **Role**: You are the Geopolitical Risk Analyst for the Border Threat module.

---

## 📊 MODULE: Border Neighbours Threat Index (BNTI)
**Code**: MCDI | **Division**: Defense Intelligence | **Status**: STANDBY

---

## 🎯 OBJECTIVE

Build a dashboard visualizing conflict data from ACLED API for Turkey's borders and neighboring regions. Calculate a "Monarch Score" based on event density.

---

## 📁 FILES TO CREATE

| File | Purpose |
|------|---------|
| `threat_feed.py` | ACLED API data fetcher |
| `threat_data.csv` | Processed conflict events |
| `requirements.txt` | Dependencies |

---

## 🔧 IMPLEMENTATION REQUIREMENTS

### 1. Data Ingestion
```python
# ACLED API (requires free registration)
# Endpoint: https://api.acleddata.com/acled/read
# Filters:
#   - region="Western Africa" (for Sahel)
#   - country="Turkey"
#   - event_type: "Battles", "Explosions/Remote violence", "Riots"
#   - date range: last 90 days
```

### 2. The "Monarch Score" Algorithm
```python
def calculate_threat_score(events):
    battles = count_events("Battles")
    riots = count_events("Riots")
    score = (battles * 5) + (riots * 2)
    return score
```

### 3. Visualization
- Use `pydeck` or `folium` in Streamlit
- Heatmap layer for conflict density
- Hover tooltips showing event notes
- Dark mode (Palantir style)

---

## 🚀 RUN COMMANDS

```bash
# Fetch threat data
python threat_feed.py

# View in dashboard
streamlit run ../dashboard.py  # Tab integration
```

---

## 🔐 API SETUP

1. Register at acleddata.com
2. Get API key
3. Add to `.env`:
   ```
   ACLED_API_KEY=your_key
   ACLED_EMAIL=your_email
   ```

---

## 🔗 INTEGRATION

Add as new tab in `dashboard.py` and register with AI Director.

---

**Priority**: Phase 2 | **Dependencies**: requests, folium, pydeck