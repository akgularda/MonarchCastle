# INFLATION INTELLIGENCE AGENCY - AGENT CONTEXT
> **Role**: You are the Economic Data Analyst for the Turkey Inflation module.

---

## 📊 MODULE: Inflation Intelligence Agency (IIA)
**Code**: MCFI | **Division**: Financial Intelligence | **Status**: ACTIVE ✅

---

## 🎯 OBJECTIVE

Track real-time prices from Turkish supermarkets to build a "Shadow CPI" that bypasses lagging official statistics and reveals the actual cost of living.

---

## 📁 FILES IN THIS FOLDER

| File | Purpose | Status |
|------|---------|--------|
| `inflation_tracker.py` | Selenium price scraper | ✅ Ready |
| `inflation_data.csv` | Output price data | Auto-generated |
| `error_log.txt` | Scraping errors | Auto-generated |
| `requirements.txt` | Dependencies | ✅ Ready |
| `agents.md` | This file | ✅ Ready |

---

## 🚀 RUN COMMANDS

```bash
# Run price collection
python inflation_tracker.py

# Or via AI Director
python ../AI_COMMAND/director.py --module inflation
```

---

## 🔧 CONFIGURATION

### Target Products (in inflation_tracker.py)
Edit `PRODUCT_URLS` list to add/modify products:
```python
PRODUCT_URLS = [
    {"name": "1L Süt", "url": "...", "price_selector": "span.price"},
    # Add more products here
]
```

### Rate Limiting
- MIN_DELAY: 3 seconds
- MAX_DELAY: 10 seconds

---

## 📈 OUTPUT FORMAT

`inflation_data.csv` columns:
| Date | Time | Product_Name | Price | Source_URL |

---

## 🔗 DASHBOARD INTEGRATION

Data displayed in `dashboard.py` Tab 1: "Turkey Inflation Monitor"
- Line chart of prices over time
- % change calculation (first vs last)
- Basket total metric

---

## ⚠️ ALERTS

Thresholds configured in `AI_COMMAND/alerts.py`:
- **Warning**: Inflation > 5%
- **Critical**: Inflation > 10%
- **Single Item Spike**: Any product > 20% change

---

## 🛠️ EXTENDING

### To add new products:
1. Find product URL on Migros/Şok/CarrefourSA
2. Inspect page to find price CSS selector
3. Add to `PRODUCT_URLS` in `inflation_tracker.py`

### To change schedule:
Edit `AI_COMMAND/scheduler.py` - currently runs every 6 hours

---

**Schedule**: Every 6 hours | **Owner**: AI Director