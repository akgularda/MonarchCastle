"""
MONARCH CASTLE TECHNOLOGIES
AI DIRECTOR - The AI CEO
=========================
Central orchestration system that coordinates all intelligence agents,
monitors system health, and generates executive summaries.

This is the "brain" of Monarch Castle - an autonomous AI that manages
the company's intelligence operations.

Usage:
    python director.py              # Run full orchestration cycle
    python director.py --status     # Check system status
    python director.py --test       # Run in test mode

Architecture:
    Director (this file)
    ├── Scheduler (task timing)
    ├── Alerts (signal aggregation)
    ├── Briefing Generator (reports)
    └── Intelligence Modules
        ├── Inflation Tracker
        ├── Pentagon Pizza
        └── Future modules...
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Fix Windows console encoding for Unicode/emoji support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add parent directory to path for imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# ============================================================================
# CONFIGURATION
# ============================================================================

class DirectorConfig:
    """Central configuration for the AI Director."""
    
    # Project paths
    ROOT = ROOT_DIR
    AI_COMMAND = ROOT / "AI_COMMAND"
    DATA_DIR = ROOT / "data"
    REPORTS_DIR = ROOT / "HQ" / "Reports"
    
    # Module paths
    MODULES = {
        "inflation": {
            "name": "Inflation Intelligence Agency",
            "code": "MCFI",
            "path": ROOT / "MVP 1 - Inflation Intelligence Agency (IIA)",
            "script": "inflation_tracker.py",
            "output": "inflation_data.csv",
            "schedule": "every_6_hours"
        },
        "pentagon": {
            "name": "Pentagon Pizza Tracker",
            "code": "MCEI", 
            "path": ROOT / "Pizza Stores Around Pentagon Tracker",
            "script": "pentagon_pizza.py",
            "output": "defense_signals.csv",
            "schedule": "hourly_after_6pm"
        },
        "bnti": {
            "name": "Border Threat Index",
            "code": "MCDI",
            "path": ROOT / "MVP 2 - Border Neighbours Threat Index (BNTI)",
            "script": "threat_feed.py",
            "output": "threat_data.csv",
            "schedule": "every_12_hours",
            "status": "standby"
        }
    }
    
    # Alert thresholds
    THRESHOLDS = {
        "inflation_critical": 10.0,    # % change triggers critical
        "inflation_warning": 5.0,      # % change triggers warning
        "pentagon_defcon": 2,          # busy stores for DEFCON
        "stale_data_hours": 24         # hours before data is stale
    }

# ============================================================================
# DIRECTOR CORE
# ============================================================================

class AIDirector:
    """
    The AI CEO of Monarch Castle Technologies.
    
    Responsibilities:
    1. Coordinate all intelligence modules
    2. Monitor system health
    3. Aggregate signals across modules
    4. Generate executive briefings
    5. Trigger alerts on anomalies
    """
    
    def __init__(self, test_mode=False):
        self.config = DirectorConfig()
        self.test_mode = test_mode
        self.status = {
            "director": "ONLINE",
            "last_run": None,
            "modules": {},
            "alerts": []
        }
        
        # Ensure directories exist
        self.config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Director logging with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = {
            "INFO": "ℹ️ ",
            "SUCCESS": "✅",
            "WARNING": "⚠️ ",
            "ERROR": "❌",
            "ALERT": "🚨"
        }.get(level, "")
        print(f"[{timestamp}] {prefix} DIRECTOR: {message}")
    
    # -------------------------------------------------------------------------
    # Module Execution
    # -------------------------------------------------------------------------
    
    def run_module(self, module_key):
        """Execute a single intelligence module."""
        module = self.config.MODULES.get(module_key)
        if not module:
            self.log(f"Unknown module: {module_key}", "ERROR")
            return False
        
        if module.get("status") == "standby":
            self.log(f"{module['name']} is on STANDBY", "INFO")
            return True
        
        script_path = module["path"] / module["script"]
        
        if not script_path.exists():
            self.log(f"Script not found: {script_path}", "ERROR")
            self.status["modules"][module_key] = "MISSING"
            return False
        
        self.log(f"Executing {module['name']}...", "INFO")
        
        if self.test_mode:
            self.log(f"[TEST MODE] Would run: python {script_path}", "INFO")
            self.status["modules"][module_key] = "TEST_OK"
            return True
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(module["path"])
            )
            
            if result.returncode == 0:
                self.log(f"{module['name']} completed successfully", "SUCCESS")
                self.status["modules"][module_key] = "ONLINE"
                return True
            else:
                self.log(f"{module['name']} failed: {result.stderr[:200]}", "ERROR")
                self.status["modules"][module_key] = "ERROR"
                return False
                
        except subprocess.TimeoutExpired:
            self.log(f"{module['name']} timed out", "ERROR")
            self.status["modules"][module_key] = "TIMEOUT"
            return False
        except Exception as e:
            self.log(f"{module['name']} exception: {str(e)}", "ERROR")
            self.status["modules"][module_key] = "EXCEPTION"
            return False
    
    def run_all_modules(self):
        """Execute all active intelligence modules."""
        self.log("=" * 50, "INFO")
        self.log("INITIATING FULL INTELLIGENCE CYCLE", "INFO")
        self.log("=" * 50, "INFO")
        
        results = {}
        for module_key in self.config.MODULES:
            results[module_key] = self.run_module(module_key)
        
        success_count = sum(results.values())
        total_count = len(results)
        
        self.log(f"Cycle complete: {success_count}/{total_count} modules successful", "INFO")
        return results
    
    # -------------------------------------------------------------------------
    # Health Monitoring
    # -------------------------------------------------------------------------
    
    def check_data_freshness(self):
        """Check if data files are stale."""
        stale_threshold = timedelta(hours=self.config.THRESHOLDS["stale_data_hours"])
        now = datetime.now()
        freshness = {}
        
        for key, module in self.config.MODULES.items():
            output_path = module["path"] / module["output"]
            
            if output_path.exists():
                mtime = datetime.fromtimestamp(output_path.stat().st_mtime)
                age = now - mtime
                is_fresh = age < stale_threshold
                freshness[key] = {
                    "fresh": is_fresh,
                    "age_hours": age.total_seconds() / 3600,
                    "last_update": mtime.isoformat()
                }
                
                if not is_fresh:
                    self.status["alerts"].append({
                        "type": "STALE_DATA",
                        "module": key,
                        "message": f"{module['name']} data is {age.total_seconds()/3600:.1f} hours old"
                    })
            else:
                freshness[key] = {
                    "fresh": False,
                    "age_hours": None,
                    "last_update": None
                }
        
        return freshness
    
    def get_system_status(self):
        """Generate comprehensive system status."""
        freshness = self.check_data_freshness()
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "director": "ONLINE",
            "modules": {},
            "data_freshness": freshness,
            "alerts": self.status["alerts"]
        }
        
        for key, module in self.config.MODULES.items():
            script_exists = (module["path"] / module["script"]).exists()
            data_exists = (module["path"] / module["output"]).exists()
            
            status["modules"][key] = {
                "name": module["name"],
                "code": module["code"],
                "script_ready": script_exists,
                "data_available": data_exists,
                "schedule": module["schedule"],
                "status": module.get("status", "active")
            }
        
        return status
    
    def print_status(self):
        """Print formatted system status."""
        status = self.get_system_status()
        
        print("\n" + "=" * 60)
        print("🏰 MONARCH CASTLE - SYSTEM STATUS")
        print("=" * 60)
        print(f"Timestamp: {status['timestamp']}")
        print(f"Director: {status['director']}")
        print("-" * 60)
        
        print("\n📊 INTELLIGENCE MODULES:")
        for key, mod in status["modules"].items():
            icon = "🟢" if mod["script_ready"] else "⚪"
            data_icon = "📁" if mod["data_available"] else "❌"
            print(f"  {icon} [{mod['code']}] {mod['name']}")
            print(f"      Script: {'Ready' if mod['script_ready'] else 'Missing'} | Data: {data_icon}")
        
        print("\n⏰ DATA FRESHNESS:")
        for key, fresh in status["data_freshness"].items():
            if fresh["age_hours"] is not None:
                icon = "🟢" if fresh["fresh"] else "🟡"
                print(f"  {icon} {key}: {fresh['age_hours']:.1f} hours old")
            else:
                print(f"  ⚪ {key}: No data yet")
        
        if status["alerts"]:
            print("\n🚨 ACTIVE ALERTS:")
            for alert in status["alerts"]:
                print(f"  - [{alert['type']}] {alert['message']}")
        else:
            print("\n✅ No active alerts")
        
        print("\n" + "=" * 60)
    
    # -------------------------------------------------------------------------
    # Orchestration
    # -------------------------------------------------------------------------
    
    def run_orchestration_cycle(self):
        """
        Main orchestration cycle - the "heartbeat" of Monarch Castle.
        
        1. Check system status
        2. Run scheduled modules
        3. Aggregate signals
        4. Check for anomalies
        5. Generate briefing if needed
        """
        self.log("=" * 50, "INFO")
        self.log("🏰 MONARCH CASTLE AI DIRECTOR ONLINE", "INFO")
        self.log("=" * 50, "INFO")
        
        # Step 1: Status check
        self.log("Phase 1: System Status Check", "INFO")
        self.print_status()
        
        # Step 2: Run modules
        self.log("Phase 2: Execute Intelligence Modules", "INFO")
        results = self.run_all_modules()
        
        # Step 3: Aggregate signals
        self.log("Phase 3: Signal Aggregation", "INFO")
        self.aggregate_signals()
        
        # Step 4: Anomaly detection
        self.log("Phase 4: Anomaly Detection", "INFO")
        anomalies = self.detect_anomalies()
        
        # Step 5: Generate briefing
        if not self.test_mode:
            self.log("Phase 5: Generate Briefing", "INFO")
            self.generate_briefing()
        
        # Final status
        self.status["last_run"] = datetime.now().isoformat()
        self.log("Orchestration cycle complete", "SUCCESS")
        
        return self.status
    
    def aggregate_signals(self):
        """Aggregate signals from all modules into unified view."""
        signals = {
            "inflation": None,
            "pentagon": None,
            "overall_threat": "NORMAL"
        }
        
        # TODO: Implement actual data reading from CSVs
        self.log("Signal aggregation complete", "INFO")
        return signals
    
    def detect_anomalies(self):
        """Detect anomalies across all data sources."""
        anomalies = []
        
        # Placeholder for anomaly detection logic
        # Would analyze trends, sudden changes, correlations
        
        self.log(f"Anomaly check complete: {len(anomalies)} found", "INFO")
        return anomalies
    
    def generate_briefing(self):
        """Generate daily intelligence briefing."""
        try:
            # Import briefing generator if available
            from briefing_generator import BriefingGenerator
            generator = BriefingGenerator()
            generator.generate_daily_briefing()
            self.log("Daily briefing generated", "SUCCESS")
        except ImportError:
            self.log("Briefing generator not yet implemented", "WARNING")
        except Exception as e:
            self.log(f"Briefing generation failed: {str(e)}", "ERROR")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Monarch Castle AI Director - The AI CEO"
    )
    parser.add_argument(
        "--status", 
        action="store_true",
        help="Show system status only"
    )
    parser.add_argument(
        "--test",
        action="store_true", 
        help="Run in test mode (no actual execution)"
    )
    parser.add_argument(
        "--module",
        type=str,
        help="Run specific module only (inflation, pentagon, bnti)"
    )
    
    args = parser.parse_args()
    
    director = AIDirector(test_mode=args.test)
    
    if args.status:
        director.print_status()
    elif args.module:
        director.run_module(args.module)
    else:
        director.run_orchestration_cycle()

if __name__ == "__main__":
    main()
