# MONARCH CASTLE TECHNOLOGIES
### SYSTEM ARCHITECTURE & AI COMMAND STRUCTURE

> **MISSION STATEMENT**
> The "Palantir of Türkiye" — An AI-managed intelligence platform that transforms open-source data into actionable signals for finance, defense, and strategy.

---

## I. CORE VALUES (THE CODE)

**1. Radical Transparency**
We bridge the gap between AI and trust. Every insight traces back to its source.
*   *Protocol:* "Here is the data, here is the prompt, here is the result."

**2. Agile Accuracy**
We move faster than institutions but verify deeper than newsfeeds.
*   *Protocol:* Speed is currency, but hallucinations are bankruptcy. Verify.

**3. Data Sovereignty**
We serve raw, objective reality over editorialized narratives.
*   *Protocol:* The chart doesn't lie.

**4. Synthesized Intelligence**
We believe the intersection of unlike fields—Food, Defense, Culture—reveals the true state of the world.
*   *Protocol:* Pizza prices near the Pentagon are not trivia; they are signals.

---

## II. AI COMMAND CENTER (THE BRAIN)

The autonomous orchestration layer that manages all intelligence operations.

### 🤖 AI Director (`director.py`)
**Role:** The AI CEO of Monarch Castle
- Coordinates all intelligence modules
- Monitors system health
- Generates executive summaries
- Triggers alerts on anomalies
- **Authority:** See [GOVERNANCE.md](./GOVERNANCE.md)

### ⏰ Scheduler (`scheduler.py`)
**Role:** Automated Task Execution
- Interval-based scheduling (every N hours)
- Time-window scheduling (Pentagon after 6 PM)
- Daily briefing generation

### 🚨 Alert System (`alerts.py`)
**Role:** Cross-Module Monitoring
- Threshold-based triggers
- Anomaly detection
- Data freshness monitoring

### 📋 Briefing Generator (`briefing_generator.py`)
**Role:** Executive Reports
- Daily intelligence summaries
- Trend analysis
- Recommendation engine

---

## III. INTELLIGENCE DIVISIONS (THE AGENTS)

### MCFI: Monarch Castle Financial Intelligence
**"The Economic Truth"**
*   **Module:** Inflation Intelligence Agency (IIA)
*   **Mission:** Bypass lagging official statistics to reveal real cost of living
*   **Product:** Real-time Turkish market price tracking
*   **Data:** Web scraping (Migros, Şok, CarrefourSA)
*   **Output:** `inflation_data.csv`

### MCEI: Monarch Castle Enjoy Intelligence
**"The Cultural Signal"**
*   **Module:** Pentagon Pizza Tracker
*   **Mission:** Track cultural biomarkers that precede geopolitical shifts
*   **Product:** Pentagon area activity monitoring
*   **Data:** Google Maps busyness signals
*   **Output:** `defense_signals.csv`

### MCDI: Monarch Castle Defense Intelligence
**"The Strategic Watch"**
*   **Module:** Border Threat Index (BNTI) / Sahel Watch (SRTI)
*   **Mission:** Geopolitical risk & conflict monitoring
*   **Product:** Regional threat heatmaps
*   **Data:** ACLED API, GDELT
*   **Status:** STANDBY

---

## IV. CORPORATE STRUCTURE

```
MonarchCastle/
├── AI_COMMAND/              # 🤖 The Brain
│   ├── director.py          # AI CEO
│   ├── scheduler.py         # Task automation
│   ├── alerts.py            # Alert aggregation
│   └── briefing_generator.py
│
├── HQ/                       # 🏛️ Corporate
│   ├── PR/                   # Press & media
│   ├── Legal/                # Compliance
│   ├── Branding/             # Style guide
│   └── Reports/              # Generated briefings
│
├── [Intelligence Modules]/   # 📊 Data collection
│
├── GOVERNANCE.md             # AI decision protocols
├── SECURITY.md               # OPSEC guidelines
└── dashboard.py              # Unified display
```

---

## V. OPERATIONAL PROTOCOLS

### Data Flow
```
Sources → Scrapers → CSV → AI Director → Alerts → Briefings → Human Review
```

### Decision Authority
| Level | AI Authority |
|-------|-------------|
| AUTONOMOUS | Scheduling, logging, routine alerts |
| NOTIFY | Elevated alerts, stale data |
| APPROVE | Critical alerts, publishing |
| PROHIBITED | Transactions, military analysis |

See [GOVERNANCE.md](./GOVERNANCE.md) for complete protocols.

---

## VI. THE TOOLCHAIN

### Data Acquisition
*   **Selenium + WebDriver Manager:** Headless browser scraping
*   **Playwright:** Complex JavaScript sites

### Processing
*   **Pandas/NumPy:** Data analysis
*   **Python (not LLMs):** All calculations

### Visualization
*   **Streamlit:** Interactive dashboard
*   **Plotly:** Charts and maps

### AI Integration
*   **Gemini-CLI / Codex:** Development assistance
*   **LLMs:** Narrative generation (with human review)

---

**System Status:** ONLINE  
**Last Updated:** January 2026