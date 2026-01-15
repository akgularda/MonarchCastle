# PENTAGON PIZZA TRACKER - AGENT CONTEXT
> **Role**: You are the OSINT Analyst for the Pentagon Activity module.

---

## 📊 MODULE: Pentagon Pizza Meter
**Code**: MCEI | **Division**: Enjoy Intelligence | **Status**: ACTIVE ✅

---

## 🎯 OBJECTIVE

Track "busyness" of pizza places near the Pentagon to infer late-night military activity. Unusual late-night orders may correlate with crisis events.

---

## 📁 FILES IN THIS FOLDER

| File | Purpose | Status |
|------|---------|--------|
| `pentagon_pizza.py` | Selenium Google Maps scraper | ✅ Ready |
| `defense_signals.csv` | Output activity data | Auto-generated |
| `error_log.txt` | Scraping errors | Auto-generated |
| `requirements.txt` | Dependencies | ✅ Ready |
| `agents.md` | This file | ✅ Ready |

---

## 🚀 RUN COMMANDS

```bash
# Run activity check
python pentagon_pizza.py

# Or via AI Director
python ../AI_COMMAND/director.py --module pentagon
```

---

## 🔧 CONFIGURATION

### Target Stores (in pentagon_pizza.py)
Edit `TARGET_STORES` list:
```python
TARGET_STORES = [
    {"name": "Domino's Pentagon City", "url": "...", "coords": (lat, lon)},
    # Add more stores here
]
```

### Risk Scoring Logic
- Check if current hour is 10 PM - 6 AM EST
- Count stores showing "Busier than usual"
- If ≥2 stores busy after 10 PM: **DEFCON 3**

---

## 📊 OUTPUT FORMAT

`defense_signals.csv` columns:
| Timestamp | Store_Name | Busyness_Status | Risk_Score | Risk_Description | Raw_Data |

---

## 🔗 DASHBOARD INTEGRATION

Data displayed in `dashboard.py` Tab 2: "Global Threat Level"
- RED banner for DEFCON 3
- GREEN banner for ALL CLEAR
- Store-by-store status

---

## ⚠️ ALERTS

Thresholds in `AI_COMMAND/alerts.py`:
- **Elevated**: 1 busy store
- **DEFCON 3**: ≥2 busy stores after 10 PM EST

---

## 🛠️ EXTENDING

### To add new stores:
1. Find Google Maps URL for pizza place near Pentagon
2. Add to `TARGET_STORES` in `pentagon_pizza.py`

### To improve detection:
Consider Google Places API for more reliable data.

---

**Schedule**: Hourly 6 PM - 6 AM EST | **Owner**: AI Director