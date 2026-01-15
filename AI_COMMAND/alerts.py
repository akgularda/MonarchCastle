"""
MONARCH CASTLE TECHNOLOGIES
ALERTS - Cross-Module Alert Aggregation
=======================================
Unified alert system that monitors all intelligence modules
and triggers notifications on significant events.

Usage:
    python alerts.py              # Check all alerts
    python alerts.py --monitor    # Continuous monitoring mode
"""

import os
import sys
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# ============================================================================
# ALERT DEFINITIONS
# ============================================================================

class AlertLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Alert:
    """Represents a system alert."""
    id: str
    level: AlertLevel
    source: str
    title: str
    message: str
    timestamp: datetime
    data: dict = None
    acknowledged: bool = False
    
    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level.name,
            "source": self.source,
            "title": self.title,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "acknowledged": self.acknowledged
        }

# ============================================================================
# THRESHOLDS
# ============================================================================

THRESHOLDS = {
    # Inflation thresholds
    "inflation_warning": 5.0,      # % change
    "inflation_critical": 10.0,
    "price_spike_single": 20.0,    # Single item spike
    
    # Pentagon thresholds
    "pentagon_elevated": 1,        # Busy stores for elevated
    "pentagon_defcon": 2,          # Busy stores for DEFCON
    
    # Data freshness
    "stale_hours_warning": 12,
    "stale_hours_critical": 24,
    
    # System health
    "consecutive_failures": 3
}

# ============================================================================
# ALERT MANAGER
# ============================================================================

class AlertManager:
    """
    Central alert management system.
    
    Monitors:
    - Inflation rate changes
    - Pentagon activity levels
    - Data freshness
    - System health
    - Cross-module correlations
    """
    
    def __init__(self):
        self.alerts: List[Alert] = []
        self.alert_history_file = ROOT_DIR / "AI_COMMAND" / ".alert_history.json"
        self.load_history()
    
    def load_history(self):
        """Load alert history from file."""
        if self.alert_history_file.exists():
            try:
                with open(self.alert_history_file, 'r') as f:
                    data = json.load(f)
                    # Note: Full deserialization would convert back to Alert objects
            except:
                pass
    
    def save_history(self):
        """Save alert history to file."""
        history = [a.to_dict() for a in self.alerts[-100:]]  # Keep last 100
        with open(self.alert_history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def create_alert(self, level: AlertLevel, source: str, title: str, 
                     message: str, data: dict = None) -> Alert:
        """Create and register a new alert."""
        alert = Alert(
            id=f"{source}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            level=level,
            source=source,
            title=title,
            message=message,
            timestamp=datetime.now(),
            data=data
        )
        self.alerts.append(alert)
        self.save_history()
        return alert
    
    def log_alert(self, alert: Alert):
        """Print alert to console."""
        level_icons = {
            AlertLevel.LOW: "ℹ️ ",
            AlertLevel.MEDIUM: "⚠️ ",
            AlertLevel.HIGH: "🔴",
            AlertLevel.CRITICAL: "🚨"
        }
        icon = level_icons.get(alert.level, "")
        print(f"\n{icon} [{alert.level.name}] {alert.title}")
        print(f"   Source: {alert.source}")
        print(f"   {alert.message}")
        if alert.data:
            print(f"   Data: {json.dumps(alert.data, indent=6)}")
    
    # -------------------------------------------------------------------------
    # Inflation Monitoring
    # -------------------------------------------------------------------------
    
    def check_inflation_alerts(self) -> List[Alert]:
        """Check for inflation-related alerts."""
        alerts = []
        csv_path = ROOT_DIR / "MVP 1 - Inflation Intelligence Agency (IIA)" / "inflation_data.csv"
        
        if not csv_path.exists():
            return alerts
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            if len(rows) < 2:
                return alerts
            
            # Calculate basket totals
            products = {}
            for row in rows:
                name = row.get('Product_Name', '')
                price = float(row.get('Price', 0))
                if name not in products:
                    products[name] = {'first': price, 'last': price}
                products[name]['last'] = price
            
            total_first = sum(p['first'] for p in products.values())
            total_last = sum(p['last'] for p in products.values())
            
            if total_first > 0:
                inflation_pct = ((total_last - total_first) / total_first) * 100
                
                if inflation_pct >= THRESHOLDS["inflation_critical"]:
                    alert = self.create_alert(
                        AlertLevel.CRITICAL,
                        "MCFI",
                        "CRITICAL INFLATION SPIKE",
                        f"Basket inflation at {inflation_pct:.1f}% - exceeds critical threshold",
                        {"inflation_rate": inflation_pct, "basket_total": total_last}
                    )
                    alerts.append(alert)
                    
                elif inflation_pct >= THRESHOLDS["inflation_warning"]:
                    alert = self.create_alert(
                        AlertLevel.HIGH,
                        "MCFI",
                        "Inflation Warning",
                        f"Basket inflation at {inflation_pct:.1f}% - exceeds warning threshold",
                        {"inflation_rate": inflation_pct}
                    )
                    alerts.append(alert)
            
            # Check for single-item spikes
            for name, prices in products.items():
                if prices['first'] > 0:
                    item_change = ((prices['last'] - prices['first']) / prices['first']) * 100
                    if item_change >= THRESHOLDS["price_spike_single"]:
                        alert = self.create_alert(
                            AlertLevel.MEDIUM,
                            "MCFI",
                            f"Price Spike: {name}",
                            f"{name} up {item_change:.1f}%",
                            {"product": name, "change": item_change}
                        )
                        alerts.append(alert)
        
        except Exception as e:
            alert = self.create_alert(
                AlertLevel.MEDIUM,
                "SYSTEM",
                "Inflation Check Failed",
                f"Could not analyze inflation data: {str(e)}"
            )
            alerts.append(alert)
        
        return alerts
    
    # -------------------------------------------------------------------------
    # Pentagon Monitoring
    # -------------------------------------------------------------------------
    
    def check_pentagon_alerts(self) -> List[Alert]:
        """Check for Pentagon activity alerts."""
        alerts = []
        csv_path = ROOT_DIR / "Pizza Stores Around Pentagon Tracker" / "defense_signals.csv"
        
        if not csv_path.exists():
            return alerts
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            if not rows:
                return alerts
            
            # Get latest timestamp's readings
            latest_ts = rows[-1].get('Timestamp', '')
            latest_readings = [r for r in rows if r.get('Timestamp') == latest_ts]
            
            # Count HIGH risk stores
            high_count = sum(1 for r in latest_readings if r.get('Risk_Score') == 'HIGH')
            
            if high_count >= THRESHOLDS["pentagon_defcon"]:
                alert = self.create_alert(
                    AlertLevel.CRITICAL,
                    "MCEI",
                    "🚨 DEFCON 3 - LATE NIGHT ACTIVITY",
                    f"{high_count} stores showing unusual late-night activity near Pentagon",
                    {"busy_stores": high_count, "timestamp": latest_ts}
                )
                alerts.append(alert)
                
            elif high_count >= THRESHOLDS["pentagon_elevated"]:
                alert = self.create_alert(
                    AlertLevel.HIGH,
                    "MCEI",
                    "Elevated Pentagon Activity",
                    f"{high_count} store(s) busier than usual",
                    {"busy_stores": high_count}
                )
                alerts.append(alert)
        
        except Exception as e:
            pass  # Silently fail for now
        
        return alerts
    
    # -------------------------------------------------------------------------
    # Data Freshness
    # -------------------------------------------------------------------------
    
    def check_data_freshness(self) -> List[Alert]:
        """Check for stale data alerts."""
        alerts = []
        now = datetime.now()
        
        data_files = [
            ("MCFI", ROOT_DIR / "MVP 1 - Inflation Intelligence Agency (IIA)" / "inflation_data.csv"),
            ("MCEI", ROOT_DIR / "Pizza Stores Around Pentagon Tracker" / "defense_signals.csv"),
        ]
        
        for source, path in data_files:
            if path.exists():
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                age_hours = (now - mtime).total_seconds() / 3600
                
                if age_hours >= THRESHOLDS["stale_hours_critical"]:
                    alert = self.create_alert(
                        AlertLevel.HIGH,
                        source,
                        f"Stale Data Warning",
                        f"Data is {age_hours:.1f} hours old - needs refresh",
                        {"age_hours": age_hours}
                    )
                    alerts.append(alert)
                    
                elif age_hours >= THRESHOLDS["stale_hours_warning"]:
                    alert = self.create_alert(
                        AlertLevel.MEDIUM,
                        source,
                        f"Data Age Notice",
                        f"Data is {age_hours:.1f} hours old",
                        {"age_hours": age_hours}
                    )
                    alerts.append(alert)
        
        return alerts
    
    # -------------------------------------------------------------------------
    # Main Check
    # -------------------------------------------------------------------------
    
    def run_all_checks(self) -> List[Alert]:
        """Run all alert checks and return triggered alerts."""
        print("\n" + "=" * 60)
        print("🚨 MONARCH CASTLE - ALERT CHECK")
        print("=" * 60)
        
        all_alerts = []
        
        # Inflation
        print("\n📊 Checking Inflation...")
        inflation_alerts = self.check_inflation_alerts()
        all_alerts.extend(inflation_alerts)
        print(f"   Found {len(inflation_alerts)} alert(s)")
        
        # Pentagon
        print("\n🍕 Checking Pentagon Activity...")
        pentagon_alerts = self.check_pentagon_alerts()
        all_alerts.extend(pentagon_alerts)
        print(f"   Found {len(pentagon_alerts)} alert(s)")
        
        # Freshness
        print("\n⏰ Checking Data Freshness...")
        freshness_alerts = self.check_data_freshness()
        all_alerts.extend(freshness_alerts)
        print(f"   Found {len(freshness_alerts)} alert(s)")
        
        # Summary
        print("\n" + "-" * 60)
        if all_alerts:
            print(f"🔔 TOTAL ALERTS: {len(all_alerts)}")
            for alert in all_alerts:
                self.log_alert(alert)
        else:
            print("✅ NO ALERTS - All systems normal")
        
        print("=" * 60 + "\n")
        
        return all_alerts
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all unacknowledged alerts."""
        return [a for a in self.alerts if not a.acknowledged]

# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Monarch Castle Alert System")
    parser.add_argument("--monitor", action="store_true", help="Continuous monitoring")
    parser.add_argument("--interval", type=int, default=300, help="Monitor interval (seconds)")
    
    args = parser.parse_args()
    
    manager = AlertManager()
    
    if args.monitor:
        import time
        print("🔔 Starting continuous alert monitoring...")
        while True:
            manager.run_all_checks()
            time.sleep(args.interval)
    else:
        manager.run_all_checks()

if __name__ == "__main__":
    main()
