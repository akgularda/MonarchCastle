# MONARCH CASTLE TECHNOLOGIES - AI GOVERNANCE PROTOCOLS

> **Classification**: INTERNAL | Required reading for AI operations

---

## Purpose

This document establishes the governance framework for AI-driven operations at Monarch Castle Technologies. It defines when AI acts autonomously, when human oversight is required, and how decisions are escalated.

---

## Decision Authority Levels

### Level 1: AUTONOMOUS
AI Director may act without human approval.

| Action | Criteria |
|--------|----------|
| Run scheduled data collection | Always permitted |
| Generate routine briefings | Always permitted |
| Log alerts for normal thresholds | Always permitted |
| Update internal metrics | Always permitted |

### Level 2: NOTIFY
AI acts, then notifies human within 24 hours.

| Action | Criteria |
|--------|----------|
| Trigger ELEVATED alerts | Inflation 5-10% change |
| Mark data as stale | After 12 hours |
| Skip failed modules | After 3 consecutive failures |
| Extend collection windows | Based on detected patterns |

### Level 3: APPROVE
AI proposes action, waits for human approval.

| Action | Criteria |
|--------|----------|
| Trigger CRITICAL alerts | Inflation >10% OR DEFCON 3 |
| Publish external content | Any public-facing output |
| Modify collection schedules | Permanent changes |
| Add new data sources | New URLs, APIs |

### Level 4: PROHIBITED
AI must never perform.

| Action | Reason |
|--------|--------|
| Financial transactions | Liability |
| Publishing military analysis | OPSEC |
| Disabling logging | Audit trail |
| Modifying governance rules | Human domain |

---

## Escalation Procedures

### Standard Escalation Path

```
AI Director → Alerts System → Briefing → Human Review
```

### Critical Escalation Path

```
AI Director → IMMEDIATE ALERT → Stop automated actions → Await human
```

---

## Verification Requirements

### Before Publishing Any Intelligence

1. **Source Verification**
   - Data must trace to documented source
   - Timestamp must be within 24 hours
   - No reliance on single data point

2. **Calculation Verification**
   - All math performed by Python, not LLM
   - Results compared against reasonable bounds
   - Outliers flagged for review

3. **Cross-Reference**
   - Extreme values (>30% change) require secondary source
   - Anomalies checked against historical patterns
   - Breaking signals held for 15 minutes for confirmation

---

## Human-in-the-Loop Requirements

### Always Required For:

- [ ] Publishing to social media
- [ ] Client-facing reports
- [ ] PR statements
- [ ] Any defense/military analysis
- [ ] Financial recommendations
- [ ] Legal matters

### AI Can Draft But Human Must Approve:

- [ ] Press releases
- [ ] Newsletter content
- [ ] Methodology documents
- [ ] Partner communications

---

## Audit Trail

All AI decisions must be logged with:

1. **Timestamp** - When decision was made
2. **Input Data** - What information was used
3. **Decision** - What action was taken
4. **Rationale** - Why (if applicable)
5. **Outcome** - Result of action

Logs retained for: **90 days minimum**

---

## Override Procedures

### Human Override of AI

At any time, the Architect may:
- Disable any module
- Pause all automated operations
- Modify any threshold
- Reject any AI recommendation

Command: `python director.py --stop`

### Emergency Shutdown

If critical failure detected:
```bash
# Stop all operations immediately
taskkill /F /IM python.exe
# Or on Linux/Mac:
# pkill -f "director.py"
```

---

## Version Control

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2026 | Initial governance framework |

---

**Approved by**: The Architect  
**Effective Date**: January 2026
