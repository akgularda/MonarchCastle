
import re
from pathlib import Path

def update_nato_in_generator():
    file_path = Path(r"c:\Users\akgul\Downloads\MonarchCastle\generate_pages.py")
    content = file_path.read_text(encoding='utf-8')

    # The new NATO chart builder and generator function
    new_code = """def build_nato_chart(countries):
    \"\"\"Generate SVG bar chart for NATO spending % GDP\"\"\"
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

    svg = f\"\"\"
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="NATO spending chart">
        <rect x="0" y="0" width="{width}" height="{height}" fill="#141a24" rx="8" />
        <line x1="{target_x}" y1="{padding_top}" x2="{target_x}" y2="{height - padding_bottom}" stroke="#3b82f6" stroke-width="2" stroke-dasharray="4 4" />
        <text x="{target_x}" y="{padding_top - 10}" text-anchor="middle" fill="#3b82f6" font-size="12" font-weight="600">2% TARGET</text>
        {bars}
        {labels}
        {values}
    </svg>
    \"\"\"
    return svg


def generate_nato_page():
    \"\"\"Generate NATO spending page with high-fidelity UI\"\"\"
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
"""
    
    # Regex to replace the old function. We match from the function definition up to the print statement of the old function.
    # Note: We need to be careful with the dotall flag to match across lines.
    
    # Pattern to find the old function
    pattern = r'def generate_nato_page\(\):.*?print\(f"\[OK\] Generated {output_path}"\)'
    
    # Check if we can find it
    match = re.search(pattern, content, re.DOTALL)
    if match:
        print("Found old function, replacing...")
        new_content = content[:match.start()] + new_code + content[match.end():]
        file_path.write_text(new_content, encoding='utf-8')
        print("Successfully updated generate_pages.py")
    else:
        print("Could not find old generate_nato_page function pattern.")
        # Fallback: We might just append/write if it's not found? No, that would duplicate.
        # Let's verify the content by printing a snippet
        print("Snippet of file around expected location:")
        start_idx = content.find("def generate_nato_page():")
        if start_idx != -1:
            print(content[start_idx:start_idx+500])
        else:
            print("Function definition not found via string search either.")

if __name__ == "__main__":
    update_nato_in_generator()
