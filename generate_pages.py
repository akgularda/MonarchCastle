"""
MONARCH CASTLE - STATIC PAGE GENERATOR
Reads JSON data and generates static HTML pages with embedded data.
No JavaScript data fetching - everything is pre-rendered.
"""

import json
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"


def load_json(filename):
    """Load JSON data file"""
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def generate_sentiment_page():
    """Generate Cloudy & Shiny sentiment page with real data"""
    data = load_json("sentiment_index.json")
    crypto = load_json("crypto_fear_greed.json")
    
    if not data:
        print("[ERROR] No sentiment data found")
        return
    
    score = data["composite_score"]
    classification = data["classification"]
    condition = data["condition"]
    
    # Generate history rows
    crypto_history = ""
    if crypto and "history" in crypto:
        for h in crypto["history"][:7]:
            crypto_history += f'<tr><td>{h["date"]}</td><td>{h["value"]}</td><td>{h["classification"]}</td></tr>'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSI-008 | Market Sentiment Index</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ --bg: #0a0a0a; --surface: #141414; --border: #262626; --text: #fafafa; --text-secondary: #737373; --accent: #f59e0b; --success: #10b981; --danger: #ef4444; }}
        body {{ font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; -webkit-font-smoothing: antialiased; }}
        .container {{ max-width: 960px; margin: 0 auto; padding: 0 24px; }}
        header {{ padding: 20px 0; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: rgba(10,10,10,0.9); backdrop-filter: blur(12px); z-index: 100; }}
        header .container {{ display: flex; justify-content: space-between; align-items: center; }}
        .breadcrumb {{ display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-secondary); }}
        .breadcrumb a {{ color: var(--text-secondary); text-decoration: none; }}
        .status-badge {{ display: flex; align-items: center; gap: 8px; padding: 6px 12px; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); border-radius: 6px; font-size: 12px; font-weight: 500; color: var(--success); }}
        .status-dot {{ width: 6px; height: 6px; background: var(--success); border-radius: 50%; animation: blink 2s ease-in-out infinite; }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
        .hero {{ padding: 80px 0 60px; border-bottom: 1px solid var(--border); }}
        .module-id {{ font-size: 12px; font-weight: 600; color: var(--accent); letter-spacing: 0.1em; margin-bottom: 16px; font-family: monospace; }}
        .hero h1 {{ font-size: 42px; font-weight: 600; letter-spacing: -0.02em; margin-bottom: 16px; }}
        .hero p {{ font-size: 18px; color: var(--text-secondary); max-width: 600px; line-height: 1.7; }}
        .gauge-container {{ display: flex; justify-content: center; margin: 60px 0; }}
        .gauge {{ width: 280px; text-align: center; }}
        .gauge-value {{ font-size: 96px; font-weight: 700; color: var(--accent); font-family: monospace; }}
        .gauge-label {{ font-size: 18px; color: var(--text); margin-top: 8px; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 600; }}
        .gauge-condition {{ font-size: 14px; color: var(--text-secondary); margin-top: 4px; }}
        .gauge-bar {{ height: 12px; background: var(--surface); border-radius: 6px; margin-top: 32px; overflow: hidden; border: 1px solid var(--border); }}
        .gauge-fill {{ height: 100%; width: {score}%; background: linear-gradient(90deg, var(--danger), var(--accent), var(--success)); border-radius: 6px; transition: width 0.5s; }}
        .gauge-scale {{ display: flex; justify-content: space-between; margin-top: 8px; font-size: 12px; color: var(--text-secondary); }}
        .content {{ padding: 60px 0; }}
        .section {{ margin-bottom: 48px; }}
        .section-title {{ font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
        .section-title::before {{ content: '//'; color: var(--accent); font-family: monospace; }}
        .data-table {{ width: 100%; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }}
        .data-table th, .data-table td {{ padding: 14px 16px; text-align: left; font-size: 13px; border-bottom: 1px solid var(--border); }}
        .data-table th {{ background: var(--surface); font-weight: 500; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; font-size: 11px; }}
        .data-table tr:last-child td {{ border-bottom: none; }}
        .data-table td {{ font-family: monospace; font-size: 13px; }}
        .sources-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 24px; }}
        .source-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 24px; text-align: center; }}
        .source-name {{ font-size: 13px; color: var(--text-secondary); margin-bottom: 8px; }}
        .source-value {{ font-size: 32px; font-weight: 600; color: var(--text); font-family: monospace; }}
        .source-weight {{ font-size: 11px; color: var(--accent); margin-top: 4px; }}
        .updated {{ font-size: 12px; color: var(--text-secondary); text-align: center; margin-top: 40px; }}
        footer {{ padding: 32px 0; border-top: 1px solid var(--border); text-align: center; }}
        footer p {{ font-size: 12px; color: var(--text-secondary); }}
        footer a {{ color: var(--accent); text-decoration: none; }}
        @media (max-width: 768px) {{ .sources-grid {{ grid-template-columns: 1fr; }} .hero h1 {{ font-size: 32px; }} .gauge-value {{ font-size: 64px; }} }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="breadcrumb"><a href="../website/index.html">Monarch Castle</a> / <span>CSI-008</span></div>
            <div class="status-badge"><span class="status-dot"></span><span>LIVE DATA</span></div>
        </div>
    </header>
    <main>
        <section class="hero">
            <div class="container">
                <div class="module-id">CSI-008 // FINANCIAL INTELLIGENCE</div>
                <h1>Cloudy & Shiny Index</h1>
                <p>Unified market sentiment score aggregating fear/greed signals from stocks, crypto, and volatility indices.</p>
            </div>
        </section>
        <div class="container">
            <div class="gauge-container">
                <div class="gauge">
                    <div class="gauge-value">{score:.0f}</div>
                    <div class="gauge-label">{classification}</div>
                    <div class="gauge-condition">Condition: {condition}</div>
                    <div class="gauge-bar"><div class="gauge-fill"></div></div>
                    <div class="gauge-scale">
                        <span>0 - Fear</span>
                        <span>100 - Greed</span>
                    </div>
                </div>
            </div>
        </div>
        <section class="content">
            <div class="container">
                <div class="section">
                    <h2 class="section-title">Component Scores</h2>
                    <div class="sources-grid">
                        <div class="source-card">
                            <div class="source-name">Stock Fear/Greed</div>
                            <div class="source-value">{data["components"]["stock_fear_greed"]:.0f}</div>
                            <div class="source-weight">Weight: 40%</div>
                        </div>
                        <div class="source-card">
                            <div class="source-name">Crypto Fear/Greed</div>
                            <div class="source-value">{data["components"]["crypto_fear_greed"]}</div>
                            <div class="source-weight">Weight: 30%</div>
                        </div>
                        <div class="source-card">
                            <div class="source-name">VIX (Inverted)</div>
                            <div class="source-value">{data["components"]["vix_inverted"]:.0f}</div>
                            <div class="source-weight">Weight: 30%</div>
                        </div>
                    </div>
                </div>
                <div class="section">
                    <h2 class="section-title">Crypto Fear & Greed History (7 Days)</h2>
                    <table class="data-table">
                        <thead><tr><th>Date</th><th>Score</th><th>Classification</th></tr></thead>
                        <tbody>{crypto_history}</tbody>
                    </table>
                </div>
                <p class="updated">Last updated: {data["fetched_at"][:16].replace("T", " ")}</p>
            </div>
        </section>
    </main>
    <footer><div class="container"><p>CSI-008 · <a href="../website/index.html">Monarch Castle Technologies</a> · Data from alternative.me</p></div></footer>
</body>
</html>'''
    
    output_path = ROOT_DIR / "Cloudy&Shiny Index (Global Fear & Greed)" / "index.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] Generated {output_path}")


def build_nato_chart(countries):
    """Generate SVG bar chart for NATO spending % GDP"""
    width = 800
    height = 400
    padding_left = 120
    padding_bottom = 40
    padding_top = 40
    padding_right = 40
    
    # Sort by % GDP desc
    sorted_data = sorted(countries, key=lambda x: x['pct_gdp'], reverse=True)
    max_val = max([x['pct_gdp'] for x in sorted_data] + [4.0])
    
    bar_height = (height - padding_top - padding_bottom) / len(sorted_data)
    bar_gap = 4
    actual_bar_height = bar_height - bar_gap
    
    target_x = padding_left + (2.0 / max_val) * (width - padding_left - padding_right)
    
    bars = ""
    labels = ""
    values = ""
    
    for i, c in enumerate(sorted_data):
        y = padding_top + i * bar_height
        bar_width = (c['pct_gdp'] / max_val) * (width - padding_left - padding_right)
        
        color = "#10b981" if c['pct_gdp'] >= 2.0 else "#ef4444"
        if c['pct_gdp'] < 2.0 and c['pct_gdp'] > 1.8: color = "#f59e0b" # Near miss
        
        bars += f'<rect x="{padding_left}" y="{y}" width="{bar_width}" height="{actual_bar_height}" fill="{color}" rx="2" />'
        labels += f'<text x="{padding_left - 10}" y="{y + actual_bar_height/1.5}" text-anchor="end" fill="#9aa4b2" font-size="11">{c["flag"]} {c["name"]}</text>'
        values += f'<text x="{padding_left + bar_width + 8}" y="{y + actual_bar_height/1.5}" fill="#f5f7fa" font-size="10" font-family="monospace">{c["pct_gdp"]:.2f}%</text>'

    svg = f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="NATO spending chart">
        <rect x="0" y="0" width="{width}" height="{height}" fill="#141a24" rx="8" />
        <line x1="{target_x}" y1="{padding_top}" x2="{target_x}" y2="{height - padding_bottom}" stroke="#3b82f6" stroke-width="2" stroke-dasharray="4 4" />
        <text x="{target_x}" y="{padding_top - 10}" text-anchor="middle" fill="#3b82f6" font-size="12" font-weight="600">2% TARGET</text>
        {bars}
        {labels}
        {values}
    </svg>
    """
    return svg


def generate_nato_page():
    """Generate NATO spending page with high-fidelity UI"""
    data = load_json("nato_spending.json")
    
    if not data:
        print("[ERROR] No NATO data found")
        return
    
    # Sort for table
    sorted_countries = sorted(data["countries"], key=lambda x: x['spending_bn'], reverse=True)
    
    # Generate country rows
    country_rows = ""
    for c in sorted_countries:
        status_class = "yes" if c["meets_target"] else "no"
        status_text = "COMPLIANT" if c["meets_target"] else "DEFICIT"
        p_capita = (c['spending_bn'] * 1e9) / (c.get('population', 1) or 1) # simple calc
        
        # Calculate deficit/surplus
        target_amount = (c['spending_bn'] / c['pct_gdp']) * 2.0
        diff = c['spending_bn'] - target_amount
        diff_str = f"+${diff:.1f}B" if diff > 0 else f"-${abs(diff):.1f}B"
        diff_class = "success" if diff > 0 else "danger"
        
        bar_width = min(100, (c['pct_gdp'] / 4.0) * 100)
        
        country_rows += f'''<tr>
            <td style="font-weight: 500; color: #fff;">{c["flag"]} {c["name"]}</td>
            <td style="font-family: monospace; color: #e3b341;">${c["spending_bn"]:.1f}B</td>
            <td>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 60px; height: 6px; background: #1f2430; border-radius: 3px; overflow: hidden;">
                        <div style="width: {bar_width}%; height: 100%; background: {'#22c55e' if c['meets_target'] else '#ef4444'};"></div>
                    </div>
                    <span style="font-family: monospace;">{c["pct_gdp"]:.2f}%</span>
                </div>
            </td>
            <td style="font-family: monospace;" class="text-{diff_class}">{diff_str}</td>
            <td><span class="status-pill {status_class}">{status_text}</span></td>
        </tr>'''

    chart_svg = build_nato_chart(data["countries"])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NATO-005 | Alliance Expenditure Tracker</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ 
            --bg: #050608;
            --surface: #10141c;
            --panel: #141a24;
            --border: #1f2430;
            --text: #f5f7fa;
            --muted: #9aa4b2;
            --accent: #3b82f6;
            --accent-glow: rgba(59, 130, 246, 0.4);
            --success: #22c55e;
            --danger: #ef4444;
            --warning: #f59e0b;
        }}
        body {{ 
            font-family: 'Inter', -apple-system, sans-serif; 
            background: linear-gradient(135deg, #050608 0%, #0b0f18 100%);
            color: var(--text); 
            min-height: 100vh; 
        }}
        .grid-overlay {{
            position: fixed; inset: 0; pointer-events: none; opacity: 0.4;
            background-size: 40px 40px;
            background-image: linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
                              linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 32px; }}
        
        /* Header */
        header {{ 
            position: sticky; top: 0; z-index: 50; 
            background: rgba(5,6,8,0.9); backdrop-filter: blur(12px); 
            border-bottom: 1px solid var(--border); 
        }}
        header .container {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 0; }}
        .brand {{ display: flex; align-items: center; gap: 12px; font-weight: 600; }}
        .brand img {{ width: 24px; height: 24px; }}
        .badge {{ 
            padding: 4px 10px; border-radius: 99px; font-size: 11px; 
            letter-spacing: 0.1em; text-transform: uppercase; border: 1px solid var(--accent); color: var(--accent);
            box-shadow: 0 0 10px var(--accent-glow);
        }}

        /* Hero */
        .hero {{ padding: 60px 0 40px; }}
        .module-id {{ color: var(--accent); font-family: monospace; font-size: 12px; margin-bottom: 12px; display: block; }}
        h1 {{ font-size: 48px; letter-spacing: -0.02em; font-weight: 700; background: linear-gradient(to right, #fff, #9aa4b2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; }}
        .subtitle {{ color: var(--muted); font-size: 18px; max-width: 600px; line-height: 1.6; }}

        /* Stats Grid */
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 40px 0; }}
        .stat-card {{ background: var(--panel); border: 1px solid var(--border); padding: 20px; border-radius: 12px; }}
        .stat-label {{ color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }}
        .stat-value {{ font-size: 32px; font-weight: 600; font-family: monospace; color: #fff; }}
        .stat-sub {{ font-size: 12px; color: var(--success); margin-top: 4px; }}

        /* Main Content */
        .layout-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 32px; margin-bottom: 60px; }}
        .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 24px; overflow: hidden; }}
        .section-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }}
        .section-title {{ font-size: 14px; font-weight: 600; text-transform: uppercase; color: var(--muted); letter-spacing: 0.1em; }}
        
        /* Table */
        .table-container {{ overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; color: var(--muted); font-size: 11px; text-transform: uppercase; padding: 12px; border-bottom: 1px solid var(--border); }}
        td {{ padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 13px; color: var(--muted); }}
        tr:last-child td {{ border-bottom: none; }}
        
        /* Components */
        .status-pill {{ padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: 600; text-transform: uppercase; }}
        .status-pill.yes {{ background: rgba(34, 197, 94, 0.1); color: var(--success); border: 1px solid rgba(34, 197, 94, 0.2); }}
        .status-pill.no {{ background: rgba(239, 68, 68, 0.1); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.2); }}
        .text-success {{ color: var(--success); }}
        .text-danger {{ color: var(--danger); }}
        
        footer {{ border-top: 1px solid var(--border); padding: 40px 0; text-align: center; color: var(--muted); font-size: 12px; margin-top: 80px; }}
        
        @media (max-width: 1024px) {{ .stats {{ grid-template-columns: repeat(2, 1fr); }} .layout-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="grid-overlay"></div>
    <header>
        <div class="container">
            <div class="brand">
                <img src="../website/logo.png" alt="Logo">
                <span>Monarch Castle</span>
            </div>
            <div class="badge">Valid: {data["year"]}</div>
        </div>
    </header>
    
    <main class="container">
        <section class="hero">
            <span class="module-id">NATO-005 // INTELLIGENCE</span>
            <h1>NATO Expenditure Tracker</h1>
            <p class="subtitle">Strategic monitoring of North Atlantic Treaty Organization defense spending against the 2% GDP treaty obligation.</p>
        </section>

        <section class="stats">
            <div class="stat-card">
                <div class="stat-label">Total Spending</div>
                <div class="stat-value" style="color: #e3b341">${data["summary"]["total_spending_bn"]:.0f}B</div>
                <div class="stat-sub">USD Equivalent</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Compliance Rate</div>
                <div class="stat-value">{data["summary"]["countries_meeting_target"]} <span style="font-size: 16px; color: var(--muted);">/ 31</span></div>
                <div class="stat-sub">Member States</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Burden</div>
                <div class="stat-value">{data["summary"]["avg_pct_gdp"]:.2f}%</div>
                <div class="stat-sub">of GDP</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">US Contribution</div>
                <div class="stat-value">66%</div>
                <div class="stat-sub">of Total</div>
            </div>
        </section>

        <div class="layout-grid">
            <!-- Left Column: Visuals -->
            <div style="display: flex; flex-direction: column; gap: 32px;">
                <div class="card">
                    <div class="section-header">
                        <div class="section-title">Compliance Landscape</div>
                    </div>
                    {chart_svg}
                </div>
                
                <div class="card">
                    <div class="section-header">
                        <div class="section-title">Strategic Assessment</div>
                    </div>
                    <div style="color: var(--muted); line-height: 1.6; font-size: 14px;">
                        <p style="margin-bottom: 12px;"><strong style="color: #fff;">EXECUTIVE SUMMARY:</strong> The Alliance shows a bifurcated spending pattern. While the Eastern Flank (Poland, Baltics) has rapidly accelerated spending exceeding 2.5% of GDP in response to regional threats, major Western European economies remain below the threshold.</p>
                        <p>Total capability gaps estimated at $80B+ annually to meet full spectrum dominance requirements. Recommend focused diplomatic pressure on Tier 2 economies to bridge the deficit gap.</p>
                    </div>
                </div>
            </div>

            <!-- Right Column: Data Table -->
            <div class="card">
                <div class="section-header">
                    <div class="section-title">Member Ledger</div>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Member</th>
                                <th>Spend</th>
                                <th>% GDP</th>
                                <th>Delta</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {country_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </main>
    
    <footer>
        NATO-005 · Monarch Castle Technologies · Source: {data["source"]}
    </footer>
</body>
</html>'''
    
    output_path = ROOT_DIR / "NATO Expenditure Tracker" / "index.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] Generated {output_path}")



def generate_oil_page():
    """Generate Oil Price page with real data"""
    data = load_json("oil_prices.json")
    
    if not data:
        print("[ERROR] No oil data found")
        return
    
    price = data["current"]["price"]
    change = data["current"]["change_1m_pct"]
    trend = "↑" if change > 0 else "↓"
    trend_color = "#10b981" if change > 0 else "#ef4444"
    
    # Generate history rows
    history_rows = ""
    for h in data["history"]:
        history_rows += f'<tr><td>{h["date"]}</td><td>${h["close"]:.2f}</td></tr>'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OPI-006 | Oil Price Oracle</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ --bg: #0a0a0a; --surface: #141414; --border: #262626; --text: #fafafa; --text-secondary: #737373; --accent: #8b5cf6; }}
        body {{ font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; -webkit-font-smoothing: antialiased; }}
        .container {{ max-width: 960px; margin: 0 auto; padding: 0 24px; }}
        header {{ padding: 20px 0; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: rgba(10,10,10,0.9); backdrop-filter: blur(12px); z-index: 100; }}
        header .container {{ display: flex; justify-content: space-between; align-items: center; }}
        .breadcrumb {{ display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-secondary); }}
        .breadcrumb a {{ color: var(--text-secondary); text-decoration: none; }}
        .status-badge {{ display: flex; align-items: center; gap: 8px; padding: 6px 12px; background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.2); border-radius: 6px; font-size: 12px; font-weight: 500; color: var(--accent); }}
        .status-dot {{ width: 6px; height: 6px; background: var(--accent); border-radius: 50%; animation: blink 2s ease-in-out infinite; }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
        .hero {{ padding: 80px 0 60px; border-bottom: 1px solid var(--border); }}
        .module-id {{ font-size: 12px; font-weight: 600; color: var(--accent); letter-spacing: 0.1em; margin-bottom: 16px; font-family: monospace; }}
        .hero h1 {{ font-size: 42px; font-weight: 600; letter-spacing: -0.02em; margin-bottom: 16px; }}
        .hero p {{ font-size: 18px; color: var(--text-secondary); max-width: 600px; line-height: 1.7; }}
        .price-display {{ text-align: center; padding: 60px 0; }}
        .price-value {{ font-size: 72px; font-weight: 700; font-family: monospace; }}
        .price-change {{ font-size: 24px; margin-top: 8px; }}
        .price-label {{ font-size: 14px; color: var(--text-secondary); margin-top: 8px; }}
        .content {{ padding: 60px 0; }}
        .section {{ margin-bottom: 48px; }}
        .section-title {{ font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
        .section-title::before {{ content: '//'; color: var(--accent); font-family: monospace; }}
        .data-table {{ width: 100%; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }}
        .data-table th, .data-table td {{ padding: 14px 16px; text-align: left; font-size: 13px; border-bottom: 1px solid var(--border); }}
        .data-table th {{ background: var(--surface); font-weight: 500; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; font-size: 11px; }}
        .data-table tr:last-child td {{ border-bottom: none; }}
        .data-table td {{ font-family: monospace; font-size: 13px; }}
        footer {{ padding: 32px 0; border-top: 1px solid var(--border); text-align: center; }}
        footer p {{ font-size: 12px; color: var(--text-secondary); }}
        footer a {{ color: var(--accent); text-decoration: none; }}
        @media (max-width: 768px) {{ .hero h1 {{ font-size: 32px; }} .price-value {{ font-size: 48px; }} }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="breadcrumb"><a href="../website/index.html">Monarch Castle</a> / <span>OPI-006</span></div>
            <div class="status-badge"><span class="status-dot"></span><span>TRACKING</span></div>
        </div>
    </header>
    <main>
        <section class="hero">
            <div class="container">
                <div class="module-id">OPI-006 // FINANCIAL INTELLIGENCE</div>
                <h1>Oil Price Oracle</h1>
                <p>Brent Crude oil price tracking and trend analysis.</p>
            </div>
        </section>
        <div class="container">
            <div class="price-display">
                <div class="price-value">${price:.2f}</div>
                <div class="price-change" style="color: {trend_color}">{trend} {abs(change):.1f}% (30d)</div>
                <div class="price-label">Brent Crude Futures (BZ=F)</div>
            </div>
        </div>
        <section class="content">
            <div class="container">
                <div class="section">
                    <h2 class="section-title">Price History</h2>
                    <table class="data-table">
                        <thead><tr><th>Date</th><th>Close</th></tr></thead>
                        <tbody>{history_rows}</tbody>
                    </table>
                </div>
            </div>
        </section>
    </main>
    <footer><div class="container"><p>OPI-006 · <a href="../website/index.html">Monarch Castle Technologies</a> · {data["source"]}</p></div></footer>
</body>
</html>'''
    
    output_path = ROOT_DIR / "Oil Price Prediction Intelligence" / "index.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] Generated {output_path}")


def generate_baltic_page():
    """Generate Baltic Dry Index page with real data"""
    data = load_json("baltic_dry.json")
    
    if not data:
        print("[ERROR] No Baltic Dry data found")
        return
    
    price = data["current"]["price"]
    change = data["current"]["change_3m_pct"]
    signal = data["current"]["signal"]
    trend_color = "#10b981" if change > 0 else "#ef4444"
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDI-007 | Baltic Dry Predictor</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ --bg: #0a0a0a; --surface: #141414; --border: #262626; --text: #fafafa; --text-secondary: #737373; --accent: #06b6d4; --danger: #ef4444; }}
        body {{ font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; -webkit-font-smoothing: antialiased; }}
        .container {{ max-width: 960px; margin: 0 auto; padding: 0 24px; }}
        header {{ padding: 20px 0; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: rgba(10,10,10,0.9); backdrop-filter: blur(12px); z-index: 100; }}
        header .container {{ display: flex; justify-content: space-between; align-items: center; }}
        .breadcrumb {{ display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-secondary); }}
        .breadcrumb a {{ color: var(--text-secondary); text-decoration: none; }}
        .status-badge {{ display: flex; align-items: center; gap: 8px; padding: 6px 12px; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 6px; font-size: 12px; font-weight: 500; color: var(--danger); }}
        .status-dot {{ width: 6px; height: 6px; background: var(--danger); border-radius: 50%; animation: blink 2s ease-in-out infinite; }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
        .hero {{ padding: 80px 0 60px; border-bottom: 1px solid var(--border); }}
        .module-id {{ font-size: 12px; font-weight: 600; color: var(--accent); letter-spacing: 0.1em; margin-bottom: 16px; font-family: monospace; }}
        .hero h1 {{ font-size: 42px; font-weight: 600; letter-spacing: -0.02em; margin-bottom: 16px; }}
        .hero p {{ font-size: 18px; color: var(--text-secondary); max-width: 600px; line-height: 1.7; }}
        .signal-box {{ background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); border-radius: 8px; padding: 24px; text-align: center; margin: 40px 0; }}
        .signal-title {{ font-size: 12px; color: var(--danger); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }}
        .signal-value {{ font-size: 24px; font-weight: 600; }}
        .price-display {{ text-align: center; padding: 40px 0; }}
        .price-value {{ font-size: 56px; font-weight: 700; font-family: monospace; }}
        .price-change {{ font-size: 20px; margin-top: 8px; }}
        .content {{ padding: 60px 0; }}
        .section {{ margin-bottom: 48px; }}
        .section-title {{ font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
        .section-title::before {{ content: '//'; color: var(--accent); font-family: monospace; }}
        .section p {{ font-size: 15px; color: var(--text-secondary); line-height: 1.8; }}
        .theory-box {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 24px; margin-top: 16px; }}
        .theory-box h4 {{ font-size: 14px; font-weight: 600; margin-bottom: 12px; color: var(--accent); }}
        .theory-box p {{ font-size: 14px; color: var(--text-secondary); line-height: 1.7; }}
        footer {{ padding: 32px 0; border-top: 1px solid var(--border); text-align: center; }}
        footer p {{ font-size: 12px; color: var(--text-secondary); }}
        footer a {{ color: var(--accent); text-decoration: none; }}
        @media (max-width: 768px) {{ .hero h1 {{ font-size: 32px; }} .price-value {{ font-size: 40px; }} }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="breadcrumb"><a href="../website/index.html">Monarch Castle</a> / <span>BDI-007</span></div>
            <div class="status-badge"><span class="status-dot"></span><span>WARNING</span></div>
        </div>
    </header>
    <main>
        <section class="hero">
            <div class="container">
                <div class="module-id">BDI-007 // FINANCIAL INTELLIGENCE</div>
                <h1>Baltic Dry-Growth Prediction</h1>
                <p>Correlate the Baltic Dry Index with global economic indicators. A leading predictor of economic health.</p>
            </div>
        </section>
        <div class="container">
            <div class="signal-box">
                <div class="signal-title">Economic Signal</div>
                <div class="signal-value">{signal}</div>
            </div>
            <div class="price-display">
                <div class="price-value">${price:.2f}</div>
                <div class="price-change" style="color: {trend_color}">{change:+.1f}% (3 months)</div>
            </div>
        </div>
        <section class="content">
            <div class="container">
                <div class="section">
                    <h2 class="section-title">Analysis</h2>
                    <div class="theory-box">
                        <h4>Leading Indicator Interpretation</h4>
                        <p>{data["analysis"]["interpretation"]}</p>
                    </div>
                </div>
            </div>
        </section>
    </main>
    <footer><div class="container"><p>BDI-007 · <a href="../website/index.html">Monarch Castle Technologies</a> · {data["source"]}</p></div></footer>
</body>
</html>'''
    
    output_path = ROOT_DIR / "Baltic Dry-Growth Prediction" / "index.html"      
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] Generated {output_path}")


def build_srti_chart(history_points, forecast_points):
    width = 860
    height = 220
    padding = 24

    total_points = max(1, len(history_points) + len(forecast_points))
    denom = max(1, total_points - 1)

    def scale_x(index):
        return padding + (index * (width - 2 * padding) / denom)

    def scale_y(value):
        return padding + (1 - (value / 100.0)) * (height - 2 * padding)

    history_coords = []
    for i, value in enumerate(history_points):
        history_coords.append((scale_x(i), scale_y(value)))

    forecast_coords = []
    if forecast_points:
        start_index = len(history_points) - 1
        forecast_coords.append((scale_x(start_index), scale_y(history_points[-1])))
        for j, value in enumerate(forecast_points, start=1):
            forecast_coords.append((scale_x(start_index + j), scale_y(value)))

    history_poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in history_coords) if history_coords else ""
    forecast_poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in forecast_coords) if forecast_coords else ""

    svg = f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="SRTI history chart">
        <defs>
            <linearGradient id="srti-line" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#e3b341" />
                <stop offset="100%" stop-color="#36c2ce" />
            </linearGradient>
        </defs>
        <rect x="0" y="0" width="{width}" height="{height}" fill="none" />
        <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height - padding}" stroke="#1f2430" />
        <line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" stroke="#1f2430" />
        <polyline points="{history_poly}" fill="none" stroke="url(#srti-line)" stroke-width="2.5" />
        <polyline points="{forecast_poly}" fill="none" stroke="#8aa3b1" stroke-width="2" stroke-dasharray="6 6" />
    </svg>
    """
    return svg


def render_srti_html(latest, history, logo_path):
    """Render SRTI HTML."""
    risk = latest.get("risk_level", "UNKNOWN")
    risk_palette = {
        "LOW": "#22c55e",
        "GUARDED": "#e3b341",
        "ELEVATED": "#f59e0b",
        "HIGH": "#ef4444",
        "CRITICAL": "#b91c1c",
    }
    risk_color = risk_palette.get(risk, "#e3b341")

    score_value = float(latest.get("score", 0.0))
    history_tail = history[-48:]
    history_scores = [float(item["score"]) for item in history_tail]
    if not history_scores:
        history_scores = [float(latest.get("score", 0.0))]
    forecast_scores = [float(item["score"]) for item in latest.get("forecast", [])]
    chart_svg = build_srti_chart(history_scores, forecast_scores)

    sources_ok = sum(1 for s in latest.get("sources", []) if s.get("status") == "ok")
    sources_total = len(latest.get("sources", []))

    headline_rows = ""
    for item in latest.get("top_headlines", [])[:6]:
        tags = ", ".join(item.get("tags") or [])
        headline_rows += f"""
        <div class="headline">
            <div>
                <div class="headline-title"><a href="{item.get('link')}" target="_blank" rel="noopener">{item.get('title')}</a></div>
                <div class="headline-meta">{item.get('source')} | {item.get('published_at')[:16].replace('T', ' ')}</div>
            </div>
            <div class="headline-score">{item.get('score'):.1f}</div>
            <div class="headline-tags">{tags}</div>
        </div>
        """

    weight_rows = ""
    for key, weight in latest.get("weights", {}).items():
        score = latest.get("components", {}).get(key, 0)
        label = key.replace("_", " ").title()
        weight_rows += f"""
        <div class="weight-card">
            <div class="weight-label">{label}</div>
            <div class="weight-score">{score:.1f}</div>
            <div class="weight-bar">
                <div class="weight-fill" style="width: {score:.1f}%;"></div>
            </div>
            <div class="weight-meta">Weight {weight:.2f}</div>
        </div>
        """

    forecast_rows = ""
    for item in latest.get("forecast", []):
        forecast_rows += f"""
        <tr>
            <td>{item.get('timestamp')[:16].replace('T', ' ')}</td>
            <td>{item.get('score'):.1f}</td>
        </tr>
        """

    source_rows = ""
    for source in latest.get("sources", []):
        source_rows += f"""
        <div class="source-row">
            <div>{source.get('name')}</div>
            <div class="source-status {source.get('status')}">{source.get('status')}</div>
            <div>{source.get('items')}</div>
        </div>
        """

    coup_signal = latest.get("coup_signal", {})

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SRTI-004 | Sahel Region Threat Index</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        :root {{
            --bg: #050608;
            --surface: #10141c;
            --panel: #141a24;
            --border: #1f2430;
            --text: #f5f7fa;
            --muted: #9aa4b2;
            --accent: #e3b341;
            --accent-2: #36c2ce;
            --danger: #ef4444;
            --success: #22c55e;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at 20% 20%, #0b0f18 0%, #050608 45%, #050608 100%);
            color: var(--text);
            min-height: 100vh;
        }}
        .grid-overlay {{
            position: fixed;
            inset: 0;
            background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 80px 80px;
            pointer-events: none;
            opacity: 0.35;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 32px;
        }}
        header {{
            position: sticky;
            top: 0;
            z-index: 10;
            backdrop-filter: blur(14px);
            background: rgba(5, 6, 8, 0.85);
            border-bottom: 1px solid var(--border);
        }}
        header .container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px 0;
        }}
        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
        }}
        .brand img {{
            width: 28px;
            height: 28px;
        }}
        .badge {{
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 12px;
            letter-spacing: 0.1em;
            border: 1px solid {risk_color};
            color: {risk_color};
            text-transform: uppercase;
        }}
        .hero {{
            padding: 80px 0 40px;
        }}
        .hero h1 {{
            font-size: 46px;
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 16px;
        }}
        .hero p {{
            color: var(--muted);
            max-width: 640px;
            line-height: 1.7;
        }}
        .hero-grid {{
            display: grid;
            grid-template-columns: 1.3fr 1fr;
            gap: 32px;
            margin-top: 36px;
        }}
        .score-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 28px;
        }}
        .score-value {{
            font-size: 72px;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: var(--accent);
        }}
        .score-meta {{
            display: flex;
            gap: 24px;
            margin-top: 18px;
            color: var(--muted);
            font-size: 13px;
        }}
        .pill {{
            padding: 6px 12px;
            border-radius: 8px;
            border: 1px solid var(--border);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .map-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
        }}
        .map-card svg {{
            width: 100%;
            height: auto;
        }}
        .section {{
            padding: 60px 0 0;
        }}
        .section-title {{
            font-size: 13px;
            color: var(--muted);
            letter-spacing: 0.2em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }}
        .chart-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
        }}
        .weights-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }}
        .weight-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
        }}
        .weight-label {{
            font-size: 12px;
            text-transform: uppercase;
            color: var(--muted);
            letter-spacing: 0.12em;
        }}
        .weight-score {{
            font-size: 32px;
            font-weight: 600;
            margin: 12px 0;
        }}
        .weight-bar {{
            height: 8px;
            border-radius: 6px;
            background: #0b0f16;
            border: 1px solid var(--border);
        }}
        .weight-fill {{
            height: 100%;
            border-radius: 6px;
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
        }}
        .weight-meta {{
            font-size: 12px;
            color: var(--muted);
            margin-top: 10px;
        }}
        .headline {{
            display: grid;
            grid-template-columns: 1fr 80px 160px;
            gap: 20px;
            padding: 16px 0;
            border-bottom: 1px solid var(--border);
        }}
        .headline:last-child {{
            border-bottom: none;
        }}
        .headline-title a {{
            color: var(--text);
            text-decoration: none;
        }}
        .headline-meta {{
            color: var(--muted);
            font-size: 12px;
            margin-top: 6px;
        }}
        .headline-score {{
            font-weight: 600;
            color: var(--accent);
            text-align: right;
        }}
        .headline-tags {{
            font-size: 12px;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .table th, .table td {{
            text-align: left;
            padding: 12px 8px;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
        }}
        .source-row {{
            display: grid;
            grid-template-columns: 1fr 120px 60px;
            gap: 12px;
            padding: 10px 0;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
        }}
        .source-status {{
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.08em;
        }}
        .source-status.ok {{
            color: var(--success);
        }}
        .source-status.empty {{
            color: var(--muted);
        }}
        .source-status.unreachable {{
            color: var(--danger);
        }}
        .pricing-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }}
        .price-card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
        }}
        .price-card h3 {{
            font-size: 18px;
            margin-bottom: 12px;
        }}
        .price {{
            font-size: 32px;
            font-weight: 600;
            margin-bottom: 16px;
        }}
        .price-list {{
            color: var(--muted);
            font-size: 13px;
            line-height: 1.8;
        }}
        footer {{
            padding: 40px 0;
            margin-top: 60px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 12px;
            text-align: center;
        }}
        @media (max-width: 960px) {{
            .hero-grid {{
                grid-template-columns: 1fr;
            }}
            .weights-grid {{
                grid-template-columns: 1fr;
            }}
            .headline {{
                grid-template-columns: 1fr;
            }}
            .pricing-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="grid-overlay"></div>
    <header>
        <div class="container">
            <div class="brand">
                <img src="{logo_path}" alt="Monarch Castle logo">
                <span>Monarch Castle Technologies</span>
            </div>
            <div class="badge">{risk}</div>
        </div>
    </header>
    <main class="container">
        <section class="hero">
            <div class="pill">SRTI-004 // Defense Intelligence</div>
            <h1>Sahel Region Threat Index</h1>
            <p>Automated OSINT scoring for Mali, Niger, and Burkina Faso. RSS-first aggregation of conflict, coup, and civilian risk signals with hourly refresh and transparency on sources.</p>
            <div class="hero-grid">
                <div class="score-card">
                    <div class="score-value">{score_value:.1f}</div>
                    <div class="score-meta">
                        <div>Risk Level: <span style="color: {risk_color}; font-weight: 600;">{risk}</span></div>
                        <div>Items: {latest.get("items_count")}</div>
                        <div>Sources Live: {sources_ok}/{sources_total}</div>
                    </div>
                    <div class="score-meta" style="margin-top: 12px;">
                        <div>Last Updated: {latest.get("fetched_at")[:16].replace("T", " ")}</div>
                        <div>Coup Signal: {coup_signal.get("status")}</div>
                    </div>
                </div>
                <div class="map-card">
                    <div class="section-title">Sahel Focus Map</div>
                    <svg viewBox="0 0 600 360" role="img" aria-label="Sahel map">
                        <defs>
                            <linearGradient id="sahelGlow" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#2b3a4c" />
                                <stop offset="50%" stop-color="#253142" />
                                <stop offset="100%" stop-color="#1d2a38" />
                            </linearGradient>
                        </defs>
                        <rect x="12" y="12" width="576" height="336" rx="16" fill="#0b0f16" stroke="#1f2430" />
                        <path d="M120 70 L190 60 L250 75 L300 92 L360 86 L420 92 L465 125 L490 170 L485 220 L455 260 L410 292 L350 315 L285 322 L230 310 L185 285 L150 250 L130 205 L120 160 Z" fill="#0f1722" stroke="#1f2430" stroke-width="1.2"/>
                        <path d="M120 138 C210 118 320 118 480 138 L480 205 C320 230 210 228 120 205 Z" fill="url(#sahelGlow)" opacity="0.6"/>
                        <path d="M150 95 L220 80 L265 95 L260 135 L242 170 L248 208 L208 212 L170 202 L142 170 L148 130 Z" fill="#1f3b4d" stroke="#36c2ce" stroke-width="1.5"/>
                        <path d="M262 122 L350 98 L430 120 L448 162 L438 195 L410 214 L392 248 L340 244 L310 218 L288 175 L270 145 Z" fill="#1f2f3f" stroke="#e3b341" stroke-width="1.5"/>
                        <path d="M170 210 L230 220 L258 255 L238 287 L185 295 L145 270 L152 232 Z" fill="#263444" stroke="#e3b341" stroke-width="1.5"/>
                        <circle cx="178" cy="165" r="4" fill="#e3b341"/>
                        <circle cx="350" cy="175" r="4" fill="#e3b341"/>
                        <circle cx="210" cy="255" r="4" fill="#e3b341"/>
                        <text x="170" y="135" fill="#9aa4b2" font-size="12">Mali</text>
                        <text x="340" y="140" fill="#9aa4b2" font-size="12">Niger</text>
                        <text x="175" y="290" fill="#9aa4b2" font-size="12">Burkina Faso</text>
                        <text x="186" y="178" fill="#8aa3b1" font-size="10">Bamako</text>
                        <text x="362" y="188" fill="#8aa3b1" font-size="10">Niamey</text>
                        <text x="222" y="268" fill="#8aa3b1" font-size="10">Ouagadougou</text>
                        <text x="400" y="130" fill="#7b8794" font-size="10" text-anchor="end">Sahel belt</text>
                    </svg>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="section-title">Historical Signal ({latest.get("window_hours")}h window)</div>
            <div class="chart-card">
                {chart_svg}
            </div>
        </section>

        <section class="section">
            <div class="section-title">Signal Weights</div>
            <div class="weights-grid">
                {weight_rows}
            </div>
        </section>

        <section class="section">
            <div class="section-title">Top Headlines</div>
            <div class="chart-card">
                {headline_rows}
            </div>
        </section>

        <section class="section">
            <div class="section-title">Forecast (Next {len(latest.get("forecast", []))} Hours)</div>
            <div class="chart-card">
                <table class="table">
                    <thead>
                        <tr><th>Timestamp (UTC)</th><th>Projected Score</th></tr>
                    </thead>
                    <tbody>
                        {forecast_rows}
                    </tbody>
                </table>
            </div>
        </section>

        <section class="section">
            <div class="section-title">Source Coverage</div>
            <div class="chart-card">
                {source_rows}
            </div>
        </section>

        <section class="section">
            <div class="section-title">Commercial Access</div>
            <div class="pricing-grid">
                <div class="price-card">
                    <h3>Observer</h3>
                    <div class="price">$299 / month</div>
                    <div class="price-list">
                        - Hourly SRTI feed<br>
                        - RSS source transparency<br>
                        - 48h history window
                    </div>
                </div>
                <div class="price-card">
                    <h3>Analyst</h3>
                    <div class="price">$1,200 / month</div>
                    <div class="price-list">
                        - Forecast exports<br>
                        - Full headline archive<br>
                        - Custom alert thresholds
                    </div>
                </div>
                <div class="price-card">
                    <h3>Enterprise</h3>
                    <div class="price">Contact Sales</div>
                    <div class="price-list">
                        - Dedicated briefing channel<br>
                        - On-prem deployment<br>
                        - Analyst support SLA
                    </div>
                </div>
            </div>
        </section>
    </main>
    <footer>
        SRTI-004 - Monarch Castle Technologies - Data sources are listed above for verification.
    </footer>
</body>
</html>"""
    return html


def generate_srti_page():
    """Generate SRTI page with OSINT RSS data."""
    latest = load_json("srti_latest.json")
    history = load_json("srti_history.json")

    if not latest or not history:
        print("[ERROR] No SRTI data found")
        return

    module_html = render_srti_html(latest, history, "../website/logo.png")
    output_path = ROOT_DIR / "Sahel Region Threat Index (SRTI)" / "index.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(module_html)
    print(f"[OK] Generated {output_path}")

    root_html = render_srti_html(latest, history, "website/logo.png")
    root_path = ROOT_DIR / "index.html"
    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(root_html)
    print(f"[OK] Generated {root_path}")


def main():
    print("=" * 50)
    print("MONARCH CASTLE - STATIC PAGE GENERATOR")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 50)

    print("\n[1/5] Generating Sentiment Index page...")
    generate_sentiment_page()

    print("\n[2/5] Generating NATO page...")
    generate_nato_page()

    print("\n[3/5] Generating Oil Price page...")
    generate_oil_page()
    
    print("\n[4/5] Generating Baltic Dry page...")
    generate_baltic_page()

    print("\n[5/5] Generating SRTI page...")
    generate_srti_page()

    print("\n" + "=" * 50)
    print("STATIC PAGE GENERATION COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()
