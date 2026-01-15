# SAHEL REGION THREAT INDEX - AGENT CONTEXT
> **Role**: You are the Africa Regional Analyst for the Sahel module.

---

## 📊 MODULE: Sahel Watch
**Code**: SRTI | **Division**: MCDI (Defense Intelligence) | **Status**: STANDBY

---

## 🎯 OBJECTIVE

Monitor conflict in the Sahel region (Mali, Niger, Burkina Faso) with focus on coup indicators and insurgent movements. Create a "Coup Risk" detection system.

## RSS-FIRST POLICY
Use RSS feeds and lightweight web scraping from Sahel-region news sites whenever possible. Do not require APIs for SRTI data collection.

---

## 📁 FILES TO CREATE

| File | Purpose |
|------|---------|
| `sahel_watch.py` | RSS-first OSINT fetcher with Sahel filters (no API) |
| `coup_detector.py` | Coup signal summary from OSINT stream |
| `sahel_data.csv` | Processed events |
| `requirements.txt` | Dependencies |

---

## 🔧 IMPLEMENTATION REQUIREMENTS

### 1. Data Pipeline
```python
# ACLED API filters:
# region = "Western Africa"
# event_type IN ("Strategic developments", "Battles", "Violence against civilians")
```

### 2. Coup Risk Heuristic
```python
def detect_coup_risk(events):
    capitals = {
        "Bamako": (12.6392, -8.0029),      # Mali
        "Niamey": (13.5137, 2.1098),        # Niger
        "Ouagadougou": (12.3714, -1.5197)   # Burkina Faso
    }
    
    for capital, coords in capitals.items():
        nearby = events_within_radius(events, coords, 50)  # 50km
        if len(nearby) > 5 and within_24_hours(nearby):
            return "RED ALERT", capital
    
    return "NORMAL", None
```

### 3. Visualization
- Dark-themed folium map centered on Sahel
- Capital city radius circles (50km)
- Event markers:
  - 🔴 Red: Battles
  - 🟡 Yellow: Riots
  - 🟣 Purple: Strategic developments
- Click for event details

---

## 🚀 RUN COMMANDS

```bash
# Fetch and analyze
python sahel_watch.py

# Run coup detection
python coup_detector.py
```

---

## 🔐 API SETUP

Same ACLED credentials as BNTI:
```
ACLED_API_KEY=your_key
ACLED_EMAIL=your_email
```

---

## 🔗 INTEGRATION

Shares infrastructure with BNTI module. Can be combined or separate tab.

---

**Priority**: Phase 2 | **Dependencies**: requests, folium, geopy
