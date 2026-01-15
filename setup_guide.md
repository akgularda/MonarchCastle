# 🛠️ MONARCH CASTLE - SETUP GUIDE

## Prerequisites

### 1. Python Installation
Download Python 3.9+ from [python.org](https://www.python.org/downloads/)

**Windows:**
- Check "Add Python to PATH" during installation
- Verify: `python --version`

**Mac/Linux:**
```bash
# Mac (Homebrew)
brew install python@3.11

# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip
```

---

## Quick Setup

### Step 1: Navigate to Project
```bash
cd C:\Users\akgul\Downloads\MonarchCastle
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Chrome WebDriver
The `webdriver-manager` package handles this automatically, but ensure Chrome is installed.

---

## Running the Scripts

### Inflation Tracker
```bash
cd "MVP 1 - Inflation Intelligence Agency (IIA)"
python inflation_tracker.py
```
**Output:** `inflation_data.csv`

### Pentagon Pizza Tracker
```bash
cd "Pizza Stores Around Pentagon Tracker"
python pentagon_pizza.py
```
**Output:** `defense_signals.csv`

### Intelligence Dashboard
```bash
# From root MonarchCastle folder
streamlit run dashboard.py
```
**Opens:** http://localhost:8501

---

## Troubleshooting

### "selenium not found"
```bash
pip install selenium webdriver-manager
```

### "streamlit not found"
```bash
pip install streamlit
# Or run with: python -m streamlit run dashboard.py
```

### Chrome WebDriver issues
```bash
pip install --upgrade webdriver-manager
```

### Playwright setup
```bash
pip install playwright
playwright install chromium
```

---

## Gemini-CLI Usage

From MonarchCastle folder, use these patterns:

```bash
# Read project context
gemini "Read GEMINI.md and summarize the project structure"

# Extend a scraper
gemini "@context Read agents.md. Add bread tracking to inflation_tracker.py"

# Fix an error
gemini "Fix this error: [paste error message]"
```

---

## Data Locations

| Script | Output File | Location |
|--------|-------------|----------|
| inflation_tracker.py | inflation_data.csv | IIA folder |
| pentagon_pizza.py | defense_signals.csv | Pentagon folder |

---

<p align="center"><b>Monarch Castle Technologies</b> | System Status: ONLINE</p>
