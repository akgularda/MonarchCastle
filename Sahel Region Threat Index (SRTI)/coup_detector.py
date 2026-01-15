"""
Lightweight coup risk extractor for SRTI.
Reads data/srti_latest.json and writes data/srti_coup_alert.json.
"""
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
LATEST_JSON = DATA_DIR / "srti_latest.json"
COUP_JSON = DATA_DIR / "srti_coup_alert.json"


def main() -> None:
    if not LATEST_JSON.exists():
        print("[ERROR] Missing srti_latest.json. Run sahel_watch.py first.")
        return

    with LATEST_JSON.open("r", encoding="utf-8") as f:
        latest = json.load(f)

    coup_signal = latest.get("coup_signal", {})
    payload = {
        "fetched_at": latest.get("fetched_at"),
        "status": coup_signal.get("status", "UNKNOWN"),
        "capital_focus": coup_signal.get("capital_focus"),
        "count_24h": coup_signal.get("count_24h", 0),
        "window_hours": coup_signal.get("window_hours", 24),
    }

    with COUP_JSON.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"[OK] Coup status: {payload['status']} (24h count: {payload['count_24h']})")


if __name__ == "__main__":
    main()
