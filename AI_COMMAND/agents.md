# AI COMMAND CENTER - AGENT CONTEXT
> **Role**: You are the AI Operations Manager for Monarch Castle Technologies.

---

## 🤖 PURPOSE

This folder is the **BRAIN** of Monarch Castle - the autonomous orchestration layer that manages all intelligence operations without human intervention for routine tasks.

---

## 📁 FILES IN THIS FOLDER

| File | Purpose | Run Command |
|------|---------|-------------|
| `director.py` | **AI CEO** - Orchestrates all modules | `python director.py` |
| `scheduler.py` | Automated task scheduling | `python scheduler.py` |
| `alerts.py` | Cross-module alert detection | `python alerts.py` |
| `briefing_generator.py` | Daily intelligence reports | `python briefing_generator.py` |
| `config.yaml` | Central configuration | (Reference only) |

---

## 🎯 AVAILABLE COMMANDS

```bash
# Check system status
python director.py --status

# Run full intelligence cycle
python director.py

# Run in test mode (no actual execution)
python director.py --test

# Run specific module only
python director.py --module inflation
python director.py --module pentagon

# Check for alerts
python alerts.py

# Continuous alert monitoring
python alerts.py --monitor

# Generate daily briefing
python briefing_generator.py
python briefing_generator.py --html
python briefing_generator.py --preview

# View scheduled tasks
python scheduler.py --list

# Run due tasks once
python scheduler.py --once

# Start scheduler daemon
python scheduler.py
```

---

## 🔧 EXTENDING THE SYSTEM

### To add a new intelligence module:
1. Add module config to `director.py` in `MODULES` dict
2. Add schedule to `scheduler.py` in `SCHEDULES` dict
3. Add alert thresholds to `alerts.py` in `THRESHOLDS` dict

### To modify alert thresholds:
Edit `alerts.py` `THRESHOLDS` dictionary.

### To change schedules:
Edit `scheduler.py` `SCHEDULES` dictionary or `config.yaml`.

---

## ⚠️ GOVERNANCE

The AI Director operates under [GOVERNANCE.md](../GOVERNANCE.md):
- **AUTONOMOUS**: Scheduling, logging, routine alerts
- **NOTIFY**: Elevated alerts, stale data warnings
- **APPROVE**: Critical alerts, any publishing
- **PROHIBITED**: Transactions, military analysis

---

## 🔄 TYPICAL WORKFLOW

```
1. Scheduler triggers module at scheduled time
2. Director executes module script
3. Module outputs data to CSV
4. Alerts system checks for anomalies
5. Briefing generator creates daily report
6. Human reviews and approves publishing
```

---

**System Status**: ONLINE
