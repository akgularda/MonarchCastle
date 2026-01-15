"""
MONARCH CASTLE TECHNOLOGIES
Inflation Intelligence Agency (IIA) - Price Tracker
====================================================
Scrapes real-time prices from Turkish supermarkets to build a "Shadow CPI".

Usage:
    python inflation_tracker.py

Output:
    inflation_data.csv - Appended price data
    error_log.txt - Any scraping errors
"""

import csv
import os
import random
import time
import logging
from datetime import datetime
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

# Target products to track (Turkish supermarket URLs)
# Replace these with actual product URLs from Migros, Şok, CarrefourSA, etc.
PRODUCT_URLS = [
    {
        "name": "1L Süt (Milk)",
        "url": "https://www.migros.com.tr/icim-tam-yagli-sut-1-l-p-2c9e31",
        "price_selector": "span.price"  # CSS selector for price element
    },
    {
        "name": "Ekmek (Bread)",
        "url": "https://www.sokmarket.com.tr/ekmek",
        "price_selector": "span.product-price"
    },
    {
        "name": "Ayçiçek Yağı 1L (Sunflower Oil)",
        "url": "https://www.migros.com.tr/aycicek-yagi-1l",
        "price_selector": "span.price"
    },
    {
        "name": "Yumurta 15'li (Eggs)",
        "url": "https://www.sokmarket.com.tr/yumurta-15li",
        "price_selector": "span.product-price"
    },
    {
        "name": "Şeker 1kg (Sugar)",
        "url": "https://www.migros.com.tr/toz-seker-1-kg",
        "price_selector": "span.price"
    }
]

# Output file
CSV_FILE = os.path.join(os.path.dirname(__file__), "inflation_data.csv")
ERROR_LOG = os.path.join(os.path.dirname(__file__), "error_log.txt")

# Rate limiting (seconds between requests)
MIN_DELAY = 3
MAX_DELAY = 10

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
    
    # User-Agent to avoid bot detection
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    # Additional anti-detection
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Execute CDP command to mask webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    
    return driver

# ============================================================================
# PRICE EXTRACTION
# ============================================================================

def extract_price(driver, url, selector, product_name):
    """
    Visit a product page and extract the price.
    
    Returns:
        tuple: (price_float, success_bool)
    """
    try:
        driver.get(url)
        
        # Wait for price element to load
        wait = WebDriverWait(driver, 15)
        price_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        
        # Extract and clean price text
        price_text = price_element.text.strip()
        
        # Remove currency symbols and convert to float
        # Handle Turkish format: "123,45 TL" or "123.45 ₺"
        price_clean = price_text.replace("TL", "").replace("₺", "").strip()
        price_clean = price_clean.replace(".", "").replace(",", ".")
        
        price_float = float(price_clean)
        
        print(f"✓ {product_name}: {price_float:.2f} TL")
        return price_float, True
        
    except Exception as e:
        error_msg = f"Failed to extract price for {product_name} from {url}: {str(e)}"
        logging.error(error_msg)
        print(f"✗ {product_name}: FAILED - {str(e)[:50]}")
        return None, False

# ============================================================================
# CSV OPERATIONS
# ============================================================================

def save_to_csv(data_rows):
    """Append scraped data to CSV file. Create file if it doesn't exist."""
    file_exists = os.path.exists(CSV_FILE)
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header if new file
        if not file_exists:
            writer.writerow(["Date", "Time", "Product_Name", "Price", "Source_URL"])
        
        # Write data rows
        writer.writerows(data_rows)
    
    print(f"\n📁 Data saved to: {CSV_FILE}")

# ============================================================================
# ANALYSIS
# ============================================================================

def calculate_inflation_rate():
    """Calculate % change from first entry to latest entry."""
    if not os.path.exists(CSV_FILE):
        return None
    
    try:
        import pandas as pd
        df = pd.read_csv(CSV_FILE)
        
        if len(df) < 2:
            return None
        
        # Group by product and get first/last prices
        products = df.groupby('Product_Name')
        
        total_first = 0
        total_last = 0
        
        for name, group in products:
            first_price = group.iloc[0]['Price']
            last_price = group.iloc[-1]['Price']
            total_first += first_price
            total_last += last_price
        
        if total_first > 0:
            inflation_rate = ((total_last - total_first) / total_first) * 100
            return inflation_rate
        
    except Exception as e:
        logging.error(f"Inflation calculation failed: {str(e)}")
    
    return None

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution loop."""
    print("=" * 60)
    print("🏰 MONARCH CASTLE - INFLATION INTELLIGENCE AGENCY")
    print("=" * 60)
    print(f"Scanning {len(PRODUCT_URLS)} products...")
    print()
    
    driver = None
    data_rows = []
    
    try:
        driver = create_driver()
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        for product in PRODUCT_URLS:
            # Random delay to avoid detection
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            time.sleep(delay)
            
            price, success = extract_price(
                driver,
                product["url"],
                product["price_selector"],
                product["name"]
            )
            
            if success:
                data_rows.append([
                    date_str,
                    time_str,
                    product["name"],
                    price,
                    product["url"]
                ])
        
        # Save results
        if data_rows:
            save_to_csv(data_rows)
            
            # Calculate and display inflation
            inflation = calculate_inflation_rate()
            if inflation is not None:
                print(f"\n📊 MONARCH INFLATION INDEX: {inflation:+.2f}%")
        else:
            print("\n⚠️ No data collected. Check error_log.txt for details.")
        
    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")
        print(f"\n❌ Critical error: {str(e)}")
        
    finally:
        if driver:
            driver.quit()
    
    print("\n" + "=" * 60)
    print("System Status: COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
