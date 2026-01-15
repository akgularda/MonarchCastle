"""
MONARCH CASTLE TECHNOLOGIES
SCHEDULER - Automated Task Scheduling
=====================================
Cron-like scheduling system for running intelligence modules
at specified intervals.

Usage:
    python scheduler.py              # Run scheduler daemon
    python scheduler.py --once       # Run all due tasks once and exit
    python scheduler.py --list       # List scheduled tasks

Schedule Types:
    - every_6_hours: Inflation tracking
    - hourly_after_6pm: Pentagon monitoring (6 PM - 6 AM EST)
    - every_12_hours: Threat index updates
    - daily_8am: Report generation
"""

import os
import sys
import time
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import pytz

# Add parent to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# ============================================================================
# CONFIGURATION
# ============================================================================

# Timezone for Pentagon operations
EST = pytz.timezone('America/New_York')
TRT = pytz.timezone('Europe/Istanbul')

SCHEDULES = {
    "inflation": {
        "type": "interval",
        "interval_hours": 6,
        "description": "Inflation tracking every 6 hours"
    },
    "pentagon": {
        "type": "window",
        "start_hour": 18,  # 6 PM EST
        "end_hour": 6,     # 6 AM EST
        "interval_minutes": 60,
        "timezone": "EST",
        "description": "Pentagon monitoring hourly during night shift"
    },
    "bnti": {
        "type": "interval",
        "interval_hours": 12,
        "description": "Border threat updates every 12 hours"
    },
    "daily_briefing": {
        "type": "daily",
        "hour": 8,
        "minute": 0,
        "timezone": "TRT",
        "description": "Daily briefing at 8 AM Istanbul time"
    }
}

STATE_FILE = Path(__file__).parent / ".scheduler_state.json"

# ============================================================================
# SCHEDULER CORE
# ============================================================================

class Scheduler:
    """
    Intelligent task scheduler for Monarch Castle operations.
    
    Supports:
    - Interval-based scheduling (every N hours)
    - Time-window scheduling (only during certain hours)
    - Daily scheduling (at specific times)
    """
    
    def __init__(self):
        self.schedules = SCHEDULES
        self.state = self.load_state()
    
    def load_state(self):
        """Load last run times from state file."""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"last_runs": {}}
    
    def save_state(self):
        """Persist state to file."""
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def log(self, message, level="INFO"):
        """Scheduler logging."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = {"INFO": "⏰", "RUN": "▶️ ", "SKIP": "⏭️ ", "ERROR": "❌"}.get(level, "")
        print(f"[{timestamp}] {prefix} SCHEDULER: {message}")
    
    def get_now(self, tz_name="TRT"):
        """Get current time in specified timezone."""
        tz = TRT if tz_name == "TRT" else EST
        return datetime.now(tz)
    
    def is_task_due(self, task_name):
        """Check if a task is due to run."""
        schedule = self.schedules.get(task_name)
        if not schedule:
            return False
        
        last_run_str = self.state["last_runs"].get(task_name)
        last_run = datetime.fromisoformat(last_run_str) if last_run_str else None
        
        now = datetime.now()
        
        if schedule["type"] == "interval":
            if last_run is None:
                return True
            
            interval = timedelta(hours=schedule["interval_hours"])
            return (now - last_run) >= interval
        
        elif schedule["type"] == "window":
            tz = EST if schedule.get("timezone") == "EST" else TRT
            now_tz = datetime.now(tz)
            current_hour = now_tz.hour
            
            start = schedule["start_hour"]
            end = schedule["end_hour"]
            
            # Check if current hour is in window
            if start > end:  # Crosses midnight (e.g., 6PM to 6AM)
                in_window = current_hour >= start or current_hour < end
            else:
                in_window = start <= current_hour < end
            
            if not in_window:
                return False
            
            # Check interval within window
            if last_run is None:
                return True
            
            interval = timedelta(minutes=schedule.get("interval_minutes", 60))
            return (now - last_run) >= interval
        
        elif schedule["type"] == "daily":
            tz = TRT if schedule.get("timezone") == "TRT" else EST
            now_tz = datetime.now(tz)
            
            target_hour = schedule["hour"]
            target_minute = schedule.get("minute", 0)
            
            # Check if we're past the target time today
            target_today = now_tz.replace(
                hour=target_hour, 
                minute=target_minute, 
                second=0, 
                microsecond=0
            )
            
            if now_tz < target_today:
                return False
            
            # Check if we've run today
            if last_run is None:
                return True
            
            last_run_date = last_run.date()
            today = now.date()
            
            return last_run_date < today
        
        return False
    
    def mark_run(self, task_name):
        """Mark a task as having run."""
        self.state["last_runs"][task_name] = datetime.now().isoformat()
        self.save_state()
    
    def get_due_tasks(self):
        """Get list of all tasks that are due."""
        return [name for name in self.schedules if self.is_task_due(name)]
    
    def run_task(self, task_name):
        """Execute a scheduled task."""
        self.log(f"Executing task: {task_name}", "RUN")
        
        try:
            if task_name in ["inflation", "pentagon", "bnti"]:
                # Run through director
                from director import AIDirector
                director = AIDirector()
                director.run_module(task_name)
            
            elif task_name == "daily_briefing":
                from briefing_generator import BriefingGenerator
                generator = BriefingGenerator()
                generator.generate_daily_briefing()
            
            self.mark_run(task_name)
            self.log(f"Task {task_name} completed", "INFO")
            return True
            
        except Exception as e:
            self.log(f"Task {task_name} failed: {str(e)}", "ERROR")
            return False
    
    def run_due_tasks(self):
        """Run all tasks that are currently due."""
        due_tasks = self.get_due_tasks()
        
        if not due_tasks:
            self.log("No tasks due at this time", "SKIP")
            return []
        
        self.log(f"Running {len(due_tasks)} due task(s): {', '.join(due_tasks)}", "INFO")
        
        results = []
        for task in due_tasks:
            results.append({
                "task": task,
                "success": self.run_task(task)
            })
        
        return results
    
    def run_daemon(self, check_interval=60):
        """
        Run as a daemon, checking for due tasks every N seconds.
        
        Args:
            check_interval: Seconds between checks (default: 60)
        """
        self.log("=" * 50, "INFO")
        self.log("🏰 MONARCH CASTLE SCHEDULER DAEMON STARTED", "INFO")
        self.log(f"Check interval: {check_interval} seconds", "INFO")
        self.log("=" * 50, "INFO")
        
        try:
            while True:
                self.run_due_tasks()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            self.log("Scheduler daemon stopped by user", "INFO")
    
    def list_schedules(self):
        """Print all scheduled tasks and their status."""
        print("\n" + "=" * 60)
        print("⏰ MONARCH CASTLE - SCHEDULED TASKS")
        print("=" * 60)
        
        now = datetime.now()
        
        for name, schedule in self.schedules.items():
            is_due = self.is_task_due(name)
            last_run_str = self.state["last_runs"].get(name, "Never")
            
            status = "🟢 DUE NOW" if is_due else "⏳ Waiting"
            
            print(f"\n📋 {name}")
            print(f"   Description: {schedule['description']}")
            print(f"   Type: {schedule['type']}")
            print(f"   Last Run: {last_run_str}")
            print(f"   Status: {status}")
        
        print("\n" + "=" * 60)

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Monarch Castle Scheduler"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run due tasks once and exit"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all scheduled tasks"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Check interval in seconds for daemon mode"
    )
    
    args = parser.parse_args()
    
    scheduler = Scheduler()
    
    if args.list:
        scheduler.list_schedules()
    elif args.once:
        scheduler.run_due_tasks()
    else:
        scheduler.run_daemon(args.interval)

if __name__ == "__main__":
    main()
