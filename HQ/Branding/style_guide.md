# MONARCH CASTLE TECHNOLOGIES - BRAND STYLE GUIDE

> **Classification**: INTERNAL | For all published materials

---

## Brand Essence

**Tagline**: *"The chart doesn't lie."*

**Voice**: Authoritative, precise, confident. We speak like a senior intelligence analyst briefing an executive—no fluff, maximum signal.

**Tone**: Professional but not corporate. Technical but accessible. Serious but not alarmist.

---

## Color Palette

### Primary Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **Monarch Black** | `#0a0a0a` | Backgrounds, primary text |
| **Castle Gold** | `#d4af37` | Accents, highlights, CTAs |
| **Deep Navy** | `#16213e` | Secondary backgrounds |

### Semantic Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **Alert Red** | `#DC143C` | HIGH risk, critical alerts |
| **Warning Amber** | `#FFA500` | ELEVATED risk, caution |
| **Safe Green** | `#228B22` | LOW risk, all clear |
| **Neutral Gray** | `#808080` | Disabled, unknown states |

### Gradients

```css
/* Primary Background */
background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);

/* Card Highlight */
background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);

/* Gold Accent */
background: linear-gradient(90deg, #d4af37 0%, #f4d03f 100%);
```

---

## Typography

### Primary Font
**Inter** — Clean, modern, highly legible
- Headers: Inter Bold (700)
- Body: Inter Regular (400)
- Data: Inter Medium (500)

### Monospace (Data/Code)
**JetBrains Mono** or **Fira Code**
- Dashboards, metrics, timestamps

### Fallback Stack
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

---

## Logo Usage

### The Mark
A stylized castle tower integrated with data visualization elements.

### Clear Space
Minimum clear space = height of the "M" in MONARCH on all sides.

### Minimum Size
- Digital: 32px height
- Print: 0.5 inches

### Don'ts
- ❌ Don't stretch or distort
- ❌ Don't use on busy backgrounds
- ❌ Don't change colors outside palette
- ❌ Don't add effects (shadows, bevels)

---

## Writing Style

### Headlines
- Title Case for major headers
- Sentence case for subheadings
- ALL CAPS only for critical alerts

### Numbers
- Use numerals for all data (5%, $100, 3 stores)
- Spell out at sentence start (Five percent...)

### Terminology

| Use | Don't Use |
|-----|-----------|
| Intelligence | Information |
| Signals | Data points |
| Anomaly | Error/Bug |
| Analysis | Report |
| Module | Script |

---

## Dashboard Components

### Metric Cards
```
┌─────────────────────────┐
│ METRIC LABEL            │
│ ██████████ 74.5%        │
│ ▲ +2.3% vs yesterday    │
└─────────────────────────┘
```
- Gold border on hover
- Subtle gradient background
- Clear hierarchy

### Alert Banners

**HIGH (Red)**
```
🚨 DEFCON 3 - [Alert Title]
Detailed description...
```

**LOW (Green)**
```
✅ ALL CLEAR - Normal Operations
```

---

## Social Media

### Twitter/X Profile
- Handle: @MonarchCastle
- Bio: "🏰 The Palantir of Türkiye | AI-powered intelligence signals | 📊 Inflation • 🍕 OSINT • 🌍 Geopolitics"

### Content Pillars
1. **The Signal** — Hard data with minimal commentary
2. **The Novelty** — Unusual correlations (Pentagon Pizza)
3. **The Architect** — Building in public narrative

---

**Document Version**: 1.0  
**Last Updated**: January 2026
