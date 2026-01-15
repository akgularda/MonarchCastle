"""
MONARCH CASTLE TECHNOLOGIES
BRIEFING GENERATOR - Daily Intelligence Reports
================================================
Generates Palantir-style executive briefings summarizing
all intelligence feeds.

Usage:
    python briefing_generator.py              # Generate today's briefing
    python briefing_generator.py --html       # Generate HTML version
    python briefing_generator.py --preview    # Preview without saving
"""

import os
import sys
import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

REPORTS_DIR = ROOT_DIR / "HQ" / "Reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# BRIEFING GENERATOR
# ============================================================================

class BriefingGenerator:
    """
    Generates executive intelligence briefings.
    
    Briefing Sections:
    1. Executive Summary
    2. Key Metrics
    3. Inflation Intelligence
    4. Defense Intelligence
    5. Anomalies & Alerts
    6. Recommendations
    """
    
    def __init__(self):
        self.today = datetime.now()
        self.data = {}
    
    def load_inflation_data(self):
        """Load and analyze inflation data."""
        csv_path = ROOT_DIR / "MVP 1 - Inflation Intelligence Agency (IIA)" / "inflation_data.csv"
        
        if not csv_path.exists():
            return {"available": False}
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            if not rows:
                return {"available": False}
            
            # Calculate metrics
            products = {}
            for row in rows:
                name = row.get('Product_Name', '')
                price = float(row.get('Price', 0))
                if name not in products:
                    products[name] = {'first': price, 'last': price, 'history': []}
                products[name]['last'] = price
                products[name]['history'].append(price)
            
            total_first = sum(p['first'] for p in products.values())
            total_last = sum(p['last'] for p in products.values())
            inflation_rate = ((total_last - total_first) / total_first * 100) if total_first > 0 else 0
            
            return {
                "available": True,
                "records": len(rows),
                "products_tracked": len(products),
                "basket_total": total_last,
                "inflation_rate": inflation_rate,
                "products": {k: v['last'] for k, v in products.items()}
            }
        except Exception as e:
            return {"available": False, "error": str(e)}
    
    def load_pentagon_data(self):
        """Load and analyze Pentagon data."""
        csv_path = ROOT_DIR / "Pizza Stores Around Pentagon Tracker" / "defense_signals.csv"
        
        if not csv_path.exists():
            return {"available": False}
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            if not rows:
                return {"available": False}
            
            # Get latest readings
            latest_ts = rows[-1].get('Timestamp', '')
            latest = [r for r in rows if r.get('Timestamp') == latest_ts]
            
            high_count = sum(1 for r in latest if r.get('Risk_Score') == 'HIGH')
            total_high = sum(1 for r in rows if r.get('Risk_Score') == 'HIGH')
            
            return {
                "available": True,
                "records": len(rows),
                "latest_timestamp": latest_ts,
                "current_high_count": high_count,
                "historical_high_count": total_high,
                "status": "DEFCON 3" if high_count >= 2 else "NORMAL"
            }
        except Exception as e:
            return {"available": False, "error": str(e)}
    
    def generate_markdown_briefing(self):
        """Generate the briefing in Markdown format."""
        inflation = self.load_inflation_data()
        pentagon = self.load_pentagon_data()
        
        briefing = f"""# 🏰 MONARCH CASTLE DAILY INTELLIGENCE BRIEFING

**Classification**: INTERNAL  
**Date**: {self.today.strftime('%B %d, %Y')}  
**Generated**: {self.today.strftime('%Y-%m-%d %H:%M:%S')}

---

## 📋 EXECUTIVE SUMMARY

"""
        # Determine overall status
        if pentagon.get('status') == 'DEFCON 3':
            briefing += "> 🚨 **ELEVATED ALERT**: Pentagon area showing unusual activity\n\n"
        elif inflation.get('inflation_rate', 0) > 5:
            briefing += f"> ⚠️ **CAUTION**: Inflation index at {inflation['inflation_rate']:.1f}%\n\n"
        else:
            briefing += "> ✅ **NORMAL**: All systems operating within expected parameters\n\n"
        
        # Key Metrics
        briefing += """---

## 📊 KEY METRICS AT A GLANCE

| Module | Status | Key Metric |
|--------|--------|------------|
"""
        if inflation.get('available'):
            briefing += f"| MCFI (Inflation) | 🟢 ONLINE | {inflation['inflation_rate']:+.1f}% |\n"
        else:
            briefing += "| MCFI (Inflation) | ⚪ NO DATA | - |\n"
        
        if pentagon.get('available'):
            status_icon = "🔴" if pentagon['status'] == 'DEFCON 3' else "🟢"
            briefing += f"| MCEI (Pentagon) | {status_icon} {pentagon['status']} | {pentagon['current_high_count']} high |\n"
        else:
            briefing += "| MCEI (Pentagon) | ⚪ NO DATA | - |\n"
        
        briefing += "| MCDI (Borders) | ⚪ STANDBY | - |\n"
        
        # Inflation Section
        briefing += """
---

## 🇹🇷 INFLATION INTELLIGENCE (MCFI)

"""
        if inflation.get('available'):
            briefing += f"""**Monarch Inflation Index**: {inflation['inflation_rate']:+.1f}%  
**Current Basket Total**: ₺{inflation['basket_total']:.2f}  
**Products Tracked**: {inflation['products_tracked']}  
**Total Records**: {inflation['records']}

### Price Breakdown

| Product | Current Price |
|---------|---------------|
"""
            for product, price in inflation.get('products', {}).items():
                briefing += f"| {product} | ₺{price:.2f} |\n"
        else:
            briefing += "*No inflation data available. Run inflation_tracker.py to collect data.*\n"
        
        # Pentagon Section
        briefing += """
---

## 🍕 PENTAGON ACTIVITY (MCEI)

"""
        if pentagon.get('available'):
            briefing += f"""**Current Status**: {pentagon['status']}  
**Stores at HIGH**: {pentagon['current_high_count']}  
**Historical HIGH triggers**: {pentagon['historical_high_count']}  
**Last Check**: {pentagon['latest_timestamp']}

"""
            if pentagon['status'] == 'DEFCON 3':
                briefing += """### ⚠️ ALERT ACTIVE

Multiple pizza stores near Pentagon showing unusual late-night activity.
This may correlate with increased operational tempo.
"""
        else:
            briefing += "*No Pentagon data available. Run pentagon_pizza.py to collect data.*\n"
        
        # Recommendations
        briefing += """
---

## 💡 RECOMMENDATIONS

"""
        recommendations = []
        
        if not inflation.get('available'):
            recommendations.append("1. **Initialize Inflation Tracking**: Run `inflation_tracker.py` to begin price monitoring")
        elif inflation.get('inflation_rate', 0) > 5:
            recommendations.append("1. **Inflation Alert**: Consider hedging strategies for TRY exposure")
        
        if not pentagon.get('available'):
            recommendations.append("2. **Initialize Pentagon Monitoring**: Run `pentagon_pizza.py` to begin activity tracking")
        elif pentagon.get('status') == 'DEFCON 3':
            recommendations.append("2. **Monitor News**: Check for developing geopolitical situations")
        
        if not recommendations:
            recommendations.append("1. **Continue Operations**: All systems nominal, maintain standard monitoring schedule")
        
        briefing += "\n".join(recommendations)
        
        # Footer
        briefing += f"""

---

## 🔧 SYSTEM STATUS

- **Director**: ONLINE
- **Scheduler**: ACTIVE
- **Alert System**: MONITORING
- **Next Briefing**: Tomorrow at 08:00

---

*This briefing was automatically generated by the Monarch Castle AI Director.*  
*For questions, consult the Architect.*

**MONARCH CASTLE TECHNOLOGIES** | *"The chart doesn't lie."*
"""
        
        return briefing
    
    def generate_html_briefing(self):
        """Generate HTML version of the briefing."""
        markdown = self.generate_markdown_briefing()
        
        # Simple HTML wrapper with styling
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Monarch Castle Daily Briefing - {self.today.strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #ffffff;
            padding: 40px;
            line-height: 1.6;
        }}
        h1, h2, h3 {{
            color: #d4af37;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #333;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #16213e;
            color: #d4af37;
        }}
        blockquote {{
            border-left: 4px solid #d4af37;
            padding-left: 20px;
            margin: 20px 0;
            background: rgba(212, 175, 55, 0.1);
            padding: 15px 20px;
        }}
        hr {{
            border: none;
            border-top: 1px solid #333;
            margin: 30px 0;
        }}
        code {{
            background: #16213e;
            padding: 2px 6px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
<pre style="white-space: pre-wrap; font-family: inherit;">
{markdown}
</pre>
</body>
</html>
"""
        return html
    
    def generate_daily_briefing(self, format="md"):
        """Generate and save the daily briefing."""
        date_str = self.today.strftime('%Y-%m-%d')
        
        if format == "html":
            content = self.generate_html_briefing()
            filename = f"briefing_{date_str}.html"
        else:
            content = self.generate_markdown_briefing()
            filename = f"briefing_{date_str}.md"
        
        output_path = REPORTS_DIR / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📋 Briefing saved to: {output_path}")
        return output_path
    
    def preview_briefing(self):
        """Print briefing to console without saving."""
        print(self.generate_markdown_briefing())

# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Monarch Castle Briefing Generator")
    parser.add_argument("--html", action="store_true", help="Generate HTML format")
    parser.add_argument("--preview", action="store_true", help="Preview without saving")
    
    args = parser.parse_args()
    
    generator = BriefingGenerator()
    
    if args.preview:
        generator.preview_briefing()
    else:
        format = "html" if args.html else "md"
        generator.generate_daily_briefing(format)

if __name__ == "__main__":
    main()
