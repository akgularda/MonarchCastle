"""
MONARCH CASTLE TECHNOLOGIES
Pentagon Pizza Tracker (MCEI - Enjoy Intelligence)
===================================================
OSINT tool monitoring late-night activity near the Pentagon
by tracking "busyness" at nearby food outlets.

Theory: Unusual late-night activity at pizza places near intelligence
hubs may correlate with crisis events.

Usage:
    python pentagon_pizza.py

Output:
    defense_signals.csv - Activity data with risk scoring
    error_log.txt - Any scraping errors
"""

import csv
import os
import random
import time
import logging
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ============================================================================
# CONFIGURATION
# ============================================================================

# Pizza places near the Pentagon (Arlington, VA)
# These are Google Maps URLs for specific locations
TARGET_STORES = [
    {
        "name": "Domino's Pizza - Pentagon City",
        "url": "https://www.google.com/maps/place/Domino's+Pizza/@38.8629,-77.0599,17z",
        "coords": (38.8629, -77.0599)
    },
    {
        "name": "Pizza Hut - Crystal City",
        "url": "https://www.google.com/maps/place/Pizza+Hut/@38.8565,-77.0494,17z",
        "coords": (38.8565, -77.0494)
    },
    {
        "name": "Papa John's - Arlington",
        "url": "https://www.google.com/maps/place/Papa+John's+Pizza/@38.8679,-77.0685,17z",
        "coords": (38.8679, -77.0685)
    }
]

# Output files
CSV_FILE = os.path.join(os.path.dirname(__file__), "defense_signals.csv")
ERROR_LOG = os.path.join(os.path.dirname(__file__), "error_log.txt")

# Timezone for risk calculation (Pentagon is in EST/EDT)
PENTAGON_TZ = pytz.timezone('America/New_York')

# Rate limiting
MIN_DELAY = 5
MAX_DELAY = 12

# Risk thresholds
LATE_NIGHT_START = 22  # 10 PM
LATE_NIGHT_END = 5     # 5 AM

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    filename=ERROR_LOG,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================================================
# BROWSER SETUP
# ============================================================================

def create_driver():
    """Create a headless Chrome browser with anti-detection measures."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # User-Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Set language to English for consistent parsing
    options.add_argument("--lang=en-US")
    prefs = {"intl.accept_languages": "en-US,en"}
    options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    
    return driver

# ============================================================================
# BUSYNESS EXTRACTION
# ============================================================================

def extract_busyness(driver, store):
    """
    Attempt to extract "Popular Times" data from Google Maps.
    
    Returns:
        tuple: (busyness_status, raw_text)
    """
    try:
        driver.get(store["url"])
        time.sleep(random.uniform(3, 5))  # Wait for dynamic content
        
        # Google Maps uses various selectors for popular times
        # These may change - update as needed
        busyness_selectors = [
            "div[aria-label*='busy']",
            "div[aria-label*='Popular times']",
            "span[aria-label*='usually']",
            ".section-popular-times",
            "[data-attrid*='popular_times']"
        ]
        
        page_text = driver.page_source.lower()
        
        # Check for busyness indicators in page text
        if "busier than usual" in page_text or "as busy as it gets" in page_text:
            return "BUSIER_THAN_USUAL", "Detected: Busier than usual"
        elif "not too busy" in page_text or "not busy" in page_text:
            return "NOT_BUSY", "Detected: Not too busy"
        elif "usually not busy" in page_text:
            return "USUALLY_NOT_BUSY", "Detected: Usually not busy"
        elif "a little busy" in page_text:
            return "LITTLE_BUSY", "Detected: A little busy"
        elif "closed" in page_text:
            return "CLOSED", "Store appears closed"
        else:
            # Try to find any aria-label with busyness info
            try:
                wait = WebDriverWait(driver, 5)
                for selector in busyness_selectors:
                    try:
                        element = driver.find_element(By.CSS_SELECTOR, selector)
                        aria_label = element.get_attribute("aria-label")
                        if aria_label:
                            return "DETECTED", f"Aria-label: {aria_label}"
                    except:
                        continue
            except:
                pass
            
            return "UNKNOWN", "Could not determine busyness"
    
    except Exception as e:
        error_msg = f"Failed to extract busyness for {store['name']}: {str(e)}"
        logging.error(error_msg)
        return "ERROR", str(e)[:100]

# ============================================================================
# RISK SCORING
# ============================================================================

def calculate_risk_score(busyness_status, current_hour_est):
    """
    Calculate risk score based on busyness and time.
    
    Logic:
    - HIGH: Busier than usual after 10 PM EST
    - ELEVATED: Busier than usual during normal hours
    - LOW: Normal activity
    """
    is_late_night = current_hour_est >= LATE_NIGHT_START or current_hour_est < LATE_NIGHT_END
    
    if busyness_status in ["BUSIER_THAN_USUAL", "DETECTED"]:
        if is_late_night:
            return "HIGH", "🔴 DEFCON 3 - Late Night Activity Detected"
        else:
            return "ELEVATED", "🟡 Above Normal Activity"
    elif busyness_status in ["NOT_BUSY", "USUALLY_NOT_BUSY"]:
        return "LOW", "🟢 Normal Operations"
    elif busyness_status == "CLOSED":
        return "LOW", "⬜ Store Closed"
    else:
        return "UNKNOWN", "⚪ Unable to Assess"

# ============================================================================
# CSV OPERATIONS
# ============================================================================

def save_to_csv(data_rows):
    """Append data to CSV file."""
    file_exists = os.path.exists(CSV_FILE)
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        if not file_exists:
            writer.writerow([
                "Timestamp", 
                "Store_Name", 
                "Busyness_Status", 
                "Risk_Score",
                "Risk_Description",
                "Raw_Data"
            ])
        
        writer.writerows(data_rows)
    
    print(f"\n📁 Data saved to: {CSV_FILE}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution loop."""
    print("=" * 60)
    print("🏰 MONARCH CASTLE - PENTAGON PIZZA TRACKER")
    print("    Enjoy Intelligence Division (MCEI)")
    print("=" * 60)
    
    # Get current time in Pentagon timezone
    now_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
    now_est = now_utc.astimezone(PENTAGON_TZ)
    current_hour = now_est.hour
    
    print(f"\n⏰ Pentagon Local Time: {now_est.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    is_late_night = current_hour >= LATE_NIGHT_START or current_hour < LATE_NIGHT_END
    if is_late_night:
        print("🌙 LATE NIGHT MONITORING MODE ACTIVE")
    else:
        print("☀️ Standard Monitoring Mode")
    
    print(f"\n📍 Monitoring {len(TARGET_STORES)} locations...")
    print("-" * 60)
    
    driver = None
    data_rows = []
    busy_count = 0
    
    try:
        driver = create_driver()
        timestamp = now_est.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        for store in TARGET_STORES:
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            time.sleep(delay)
            
            print(f"\n🍕 Checking: {store['name']}")
            
            busyness_status, raw_data = extract_busyness(driver, store)
            risk_score, risk_desc = calculate_risk_score(busyness_status, current_hour)
            
            print(f"   Status: {busyness_status}")
            print(f"   Risk: {risk_desc}")
            
            if busyness_status in ["BUSIER_THAN_USUAL", "DETECTED"]:
                busy_count += 1
            
            data_rows.append([
                timestamp,
                store["name"],
                busyness_status,
                risk_score,
                risk_desc,
                raw_data
            ])
        
        # Save results
        if data_rows:
            save_to_csv(data_rows)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        
        if busy_count >= 2 and is_late_night:
            print("\n🚨 ALERT: DEFCON 3 - LATE NIGHT MUNCHIES DETECTED")
            print("   Multiple stores showing unusual late-night activity!")
        elif busy_count >= 2:
            print("\n⚠️ ELEVATED: Multiple busy stores detected")
        else:
            print("\n✅ STATUS: Normal operations")
        
        print(f"\nStores Busy: {busy_count}/{len(TARGET_STORES)}")
        
    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")
        print(f"\n❌ Critical error: {str(e)}")
        
    finally:
        if driver:
            driver.quit()
    
    print("\n" + "=" * 60)
    print("🏰 Monarch Castle Intelligence | System Status: COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
