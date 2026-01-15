# MONARCH CASTLE TECHNOLOGIES - SECURITY & OPSEC GUIDELINES

> **Classification**: INTERNAL | Required reading for all operations

---

## Data Classification

### PUBLIC
- Published reports
- Press releases
- Social media posts
- General methodology

### INTERNAL
- Raw scraped data
- Unpublished analyses
- Agent configurations
- This document

### RESTRICTED
- API keys and credentials
- Client-specific data
- Source configurations  
- Error logs with URLs

### PROHIBITED
- No classified information
- No non-public government data
- No personally identifiable information (PII)
- No hacked or leaked data

---

## Operational Security (OPSEC)

### Never Publish

❌ Real-time predictions of military movements  
❌ Specific troop/asset locations  
❌ Names of intelligence personnel  
❌ Client identities  
❌ Exact scraping targets (use generic references)

### Safe to Publish

✅ Historical correlations  
✅ Aggregated trends  
✅ General "activity levels"  
✅ Anonymized case studies  
✅ Methodology (without exact selectors)

---

## Credential Management

### Environment Variables

All secrets MUST be stored in environment variables:

```bash
# .env file (NEVER commit to git)
GOOGLE_PLACES_API_KEY=xxx
ACLED_API_KEY=xxx
```

### .gitignore Requirements

```gitignore
# Secrets
.env
*.env
.env.*

# State files
.scheduler_state.json
.alert_history.json

# Data files (optional)
*.csv
error_log.txt

# Cache
__pycache__/
*.pyc
```

---

## Scraping Ethics

### Do

✅ Respect robots.txt  
✅ Use reasonable delays (3-10 seconds)  
✅ Identify bots honestly  
✅ Cache when possible  
✅ Stop if blocked

### Don't

❌ Scrape login-protected content  
❌ Bypass CAPTCHAs  
❌ Overload servers  
❌ Scrape PII  
❌ Sell raw scraped data

### Rate Limiting Standards

| Source Type | Minimum Delay | Max RPS |
|-------------|---------------|---------|
| E-commerce | 5 seconds | 0.2 |
| Google Maps | 10 seconds | 0.1 |
| APIs (with key) | Per TOS | Per TOS |
| Government data | 3 seconds | 0.33 |

---

## Incident Response

### If Data Breach Suspected

1. **STOP** - Halt all automated operations
2. **ISOLATE** - Disconnect from network if needed
3. **ASSESS** - Determine scope
4. **ROTATE** - Change all API keys
5. **DOCUMENT** - Record timeline
6. **NOTIFY** - Inform affected parties if applicable

### If Scraper Blocked

1. Check if block is temporary (wait 1 hour)
2. Review rate limiting settings
3. Check for changed selectors
4. Consider alternative data source
5. Document in error log

### If Incorrect Data Published

1. Delete/retract immediately
2. Issue correction if public
3. Investigate root cause
4. Add validation to prevent recurrence

---

## Defense Intelligence Specific Rules

### The "Newspaper Test"

Before publishing any defense-related analysis, ask:

> "If this appeared on the front page of a newspaper, would it endanger anyone or reveal sensitive capabilities?"

If YES → Do not publish.

### Framing Guidelines

| Instead of | Say |
|------------|-----|
| "Military activity detected" | "Unusual patterns observed" |
| "Troops are mobilizing" | "Activity levels elevated" |
| "Attack imminent" | "Risk indicators increased" |

---

## Social Media Security

### Account Security

- [ ] 2FA enabled on all accounts
- [ ] Unique passwords (use password manager)
- [ ] No account sharing
- [ ] Regular session reviews

### Content Review

All tweets/posts must be reviewed for:
- [ ] Source attribution present
- [ ] No classified indicators
- [ ] No exact locations
- [ ] Appropriate disclaimers

---

## Compliance Checklist

Before any external publication:

- [ ] Data sourced legally
- [ ] No PII included
- [ ] Disclaimers present
- [ ] Predictions framed appropriately
- [ ] Human review completed
- [ ] Archived with timestamp

---

**Document Owner**: The Architect  
**Review Cycle**: Quarterly  
**Last Updated**: January 2026
