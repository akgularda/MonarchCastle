# MONARCH CASTLE TECHNOLOGIES - DATA HANDLING POLICY

> **Classification**: INTERNAL | Required reading for all agents

---

## Data Classification Levels

### Level 1: PUBLIC
- Published reports and analyses
- Press releases
- Social media content

### Level 2: INTERNAL
- Raw scraped data
- Unpublished analyses
- Agent configurations

### Level 3: RESTRICTED
- API keys and credentials
- Client-specific reports
- Source configurations

---

## Collection Principles

### 1. Legality
All data must be collected from:
- Public websites (respecting robots.txt)
- Official APIs with valid credentials
- Open government sources

### 2. Rate Limiting
- Minimum 3-second delay between requests
- Maximum 100 requests per source per hour
- Respect server error responses (429, 503)

### 3. User-Agent Honesty
Scrapers must identify as:
```
MonarchCastle-Bot/1.0 (+https://monarchcastle.tech/bot)
```

---

## Storage Requirements

| Data Type | Retention | Encryption |
|-----------|-----------|------------|
| Raw prices | 2 years | At rest |
| Signals | 1 year | At rest |
| Logs | 90 days | None |
| API keys | Active only | Environment variables |

---

## Deletion Requests

Upon legitimate request:
1. Acknowledge within 48 hours
2. Remove data within 14 days
3. Confirm deletion in writing

---

## Incident Response

If a data breach is suspected:
1. Isolate affected systems
2. Rotate all API keys
3. Document timeline
4. Notify affected parties within 72 hours

---

**Document Version**: 1.0  
**Last Updated**: January 2026
