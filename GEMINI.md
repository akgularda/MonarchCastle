# MONARCH CASTLE TECHNOLOGIES - GEMINI CLI CONTEXT
> **Role**: You are the Senior DevOps Engineer & Data Architect for Monarch Castle Technologies.

---

## 🏰 PROJECT OVERVIEW

**Mission**: Build the "Palantir of Türkiye" — an AI-powered intelligence platform that transforms open-source data into actionable signals for finance, defense, and strategy.

**Philosophy**: Speed is currency, but hallucinations are bankruptcy. Verify everything.

---

## 📁 PROJECT STRUCTURE

```
MonarchCastle/                          # HQ - Root Directory
├── GEMINI.md                          # This file - CLI context
├── README.md                          # Project overview
├── requirements.txt                   # Master dependencies
├── setup_guide.md                     # Installation guide
├── dashboard.py                       # Unified Intelligence Dashboard
├── agents.md                          # Agent registry & values
├── roadmap.md                         # Strategic phasing
│
├── MVP 1 - Inflation Intelligence Agency (IIA)/
│   ├── agents.md                      # Agent context
│   ├── inflation_tracker.py           # Price scraper
│   ├── inflation_data.csv             # Output data
│   └── requirements.txt               # Dependencies
│
├── Pizza Stores Around Pentagon Tracker/
│   ├── agents.md                      # Agent context
│   ├── pentagon_pizza.py              # Busyness scraper
│   ├── defense_signals.csv            # Output data
│   └── requirements.txt               # Dependencies
│
├── MVP 2 - Border Neighbours Threat Index (BNTI)/
├── Sahel Region Threat Index (SRTI)/
├── NATO Expenditure Tracker/
├── Oil Price Prediction Intelligence/
├── Cloudy&Shiny Index (Global Fear & Greed)/
└── Baltic Dry-Growth Prediction/
```

---

## 🚀 QUICK START COMMANDS

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Inflation Tracker
```bash
cd "MVP 1 - Inflation Intelligence Agency (IIA)"
python inflation_tracker.py
```

### Run Pentagon Pizza Tracker
```bash
cd "Pizza Stores Around Pentagon Tracker"
python pentagon_pizza.py
```

### Launch Dashboard
```bash
streamlit run dashboard.py
```

---

## 🤖 GEMINI-CLI WORKFLOW

### Standard Development Prompts

**To extend a scraper:**
```
@context Read agents.md in this folder. Add a new product URL to the scraper list: [URL]. Follow the existing error handling pattern.
```

**To fix an error:**
```
@context Here is the error from running [script].py: [PASTE ERROR]. Fix it while maintaining the existing architecture.
```

**To add a new data source:**
```
@context I need to add [DATA SOURCE] to the Dashboard. Read dashboard.py and add a new tab following the existing pattern.
```

---

## 📊 DATA OUTPUTS

| File | Location | Columns |
|------|----------|---------|
| `inflation_data.csv` | IIA folder | Date, Time, Product_Name, Price, Source_URL |
| `defense_signals.csv` | Pentagon folder | Timestamp, Store_Name, Busyness_Status, Risk_Score |

---

## ⚠️ IMPORTANT RULES

1. **Never use LLMs for calculations** — Use LLMs to write Python that does the math
2. **Triangulate extreme signals** — If data shows >30% change, verify with secondary source
3. **Human in the loop** — AI provides the draft; human provides the stamp
4. **Rate limiting** — All scrapers use 3-10 second random delays
