"""
MONARCH CASTLE - DATA COLLECTOR
Fetches real data from various APIs and saves to JSON for static display.
Run this script periodically to update all data.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Try to import optional dependencies
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    print("[WARN] yfinance not installed. Run: pip install yfinance")

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("[WARN] requests not installed. Run: pip install requests")


ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def save_json(filename, data):
    """Save data to JSON file"""
    filepath = DATA_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"[OK] Saved {filepath}")


def fetch_fear_greed_crypto():
    """Fetch Crypto Fear & Greed Index from alternative.me"""
    if not HAS_REQUESTS:
        return None
    
    try:
        url = "https://api.alternative.me/fng/?limit=7"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        result = {
            "fetched_at": datetime.now().isoformat(),
            "source": "alternative.me",
            "current": {
                "value": int(data["data"][0]["value"]),
                "classification": data["data"][0]["value_classification"],
                "timestamp": data["data"][0]["timestamp"]
            },
            "history": [
                {
                    "value": int(d["value"]),
                    "classification": d["value_classification"],
                    "date": datetime.fromtimestamp(int(d["timestamp"])).strftime("%Y-%m-%d")
                }
                for d in data["data"]
            ]
        }
        return result
    except Exception as e:
        print(f"[ERROR] Crypto Fear/Greed: {e}")
        return None


def fetch_vix():
    """Fetch VIX (Volatility Index) from Yahoo Finance"""
    if not HAS_YFINANCE:
        return None
    
    try:
        vix = yf.Ticker("^VIX")
        hist = vix.history(period="7d")
        
        if hist.empty:
            return None
        
        result = {
            "fetched_at": datetime.now().isoformat(),
            "source": "Yahoo Finance",
            "current": {
                "value": round(hist['Close'].iloc[-1], 2),
                "date": hist.index[-1].strftime("%Y-%m-%d")
            },
            "history": [
                {
                    "date": idx.strftime("%Y-%m-%d"),
                    "close": round(row['Close'], 2)
                }
                for idx, row in hist.iterrows()
            ]
        }
        return result
    except Exception as e:
        print(f"[ERROR] VIX: {e}")
        return None


def fetch_oil_prices():
    """Fetch Brent Crude Oil prices from Yahoo Finance"""
    if not HAS_YFINANCE:
        return None
    
    try:
        oil = yf.Ticker("BZ=F")
        hist = oil.history(period="1mo")
        
        if hist.empty:
            return None
        
        # Calculate trend
        first_price = hist['Close'].iloc[0]
        last_price = hist['Close'].iloc[-1]
        change_pct = ((last_price - first_price) / first_price) * 100
        
        result = {
            "fetched_at": datetime.now().isoformat(),
            "source": "Yahoo Finance",
            "ticker": "BZ=F",
            "name": "Brent Crude Oil",
            "current": {
                "price": round(last_price, 2),
                "date": hist.index[-1].strftime("%Y-%m-%d"),
                "change_1m_pct": round(change_pct, 2),
                "trend": "up" if change_pct > 0 else "down"
            },
            "history": [
                {
                    "date": idx.strftime("%Y-%m-%d"),
                    "close": round(row['Close'], 2)
                }
                for idx, row in hist.tail(14).iterrows()
            ]
        }
        return result
    except Exception as e:
        print(f"[ERROR] Oil: {e}")
        return None


def fetch_baltic_dry():
    """Fetch Baltic Dry Index proxy (BDRY ETF) from Yahoo Finance"""
    if not HAS_YFINANCE:
        return None
    
    try:
        # BDRY is an ETF that tracks the Baltic Dry Index
        bdi = yf.Ticker("BDRY")
        hist = bdi.history(period="3mo")
        
        if hist.empty:
            return None
        
        # Calculate trend
        first_price = hist['Close'].iloc[0]
        last_price = hist['Close'].iloc[-1]
        change_pct = ((last_price - first_price) / first_price) * 100
        
        result = {
            "fetched_at": datetime.now().isoformat(),
            "source": "Yahoo Finance",
            "ticker": "BDRY",
            "name": "Baltic Dry Index (ETF Proxy)",
            "current": {
                "price": round(last_price, 2),
                "date": hist.index[-1].strftime("%Y-%m-%d"),
                "change_3m_pct": round(change_pct, 2),
                "trend": "up" if change_pct > 0 else "down",
                "signal": "Economic expansion" if change_pct > 10 else ("Economic contraction" if change_pct < -10 else "Stable")
            },
            "history": [
                {
                    "date": idx.strftime("%Y-%m-%d"),
                    "close": round(row['Close'], 2)
                }
                for idx, row in hist.tail(30).iterrows()
            ]
        }
        return result
    except Exception as e:
        print(f"[ERROR] Baltic Dry: {e}")
        return None


def fetch_sp500():
    """Fetch S&P 500 data from Yahoo Finance"""
    if not HAS_YFINANCE:
        return None
    
    try:
        sp = yf.Ticker("^GSPC")
        hist = sp.history(period="1mo")
        
        if hist.empty:
            return None
        
        first_price = hist['Close'].iloc[0]
        last_price = hist['Close'].iloc[-1]
        change_pct = ((last_price - first_price) / first_price) * 100
        
        result = {
            "fetched_at": datetime.now().isoformat(),
            "source": "Yahoo Finance",
            "ticker": "^GSPC",
            "name": "S&P 500",
            "current": {
                "price": round(last_price, 2),
                "date": hist.index[-1].strftime("%Y-%m-%d"),
                "change_1m_pct": round(change_pct, 2)
            }
        }
        return result
    except Exception as e:
        print(f"[ERROR] S&P 500: {e}")
        return None


def calculate_sentiment_index():
    """Calculate Cloudy & Shiny (Fear/Greed) composite index"""
    # Load component data
    crypto_file = DATA_DIR / "crypto_fear_greed.json"
    vix_file = DATA_DIR / "vix.json"
    
    crypto_score = 50  # Default neutral
    vix_score = 50  # Default neutral
    stock_score = 50  # Default neutral
    
    try:
        if crypto_file.exists():
            with open(crypto_file) as f:
                crypto_data = json.load(f)
                crypto_score = crypto_data["current"]["value"]
        
        if vix_file.exists():
            with open(vix_file) as f:
                vix_data = json.load(f)
                vix_value = vix_data["current"]["value"]
                # Invert VIX: High VIX = Fear, Low VIX = Greed
                # VIX ranges roughly 10-80, normalize to 0-100 inverted
                vix_score = max(0, min(100, 100 - ((vix_value - 10) / 0.7)))
        
        # For stock fear/greed, use a simple approximation based on S&P 500 momentum
        sp_file = DATA_DIR / "sp500.json"
        if sp_file.exists():
            with open(sp_file) as f:
                sp_data = json.load(f)
                change = sp_data["current"]["change_1m_pct"]
                # Map -10% to +10% change to 0-100 score
                stock_score = max(0, min(100, 50 + (change * 5)))
    except Exception as e:
        print(f"[ERROR] Sentiment calculation: {e}")
    
    # Weighted average
    composite = (stock_score * 0.4) + (crypto_score * 0.3) + (vix_score * 0.3)
    composite = round(composite, 1)
    
    # Classify
    if composite <= 20:
        classification = "Extreme Fear"
        emoji = "☁️"
        condition = "STORMY"
    elif composite <= 40:
        classification = "Fear"
        emoji = "🌧️"
        condition = "RAINY"
    elif composite <= 60:
        classification = "Neutral"
        emoji = "🌤️"
        condition = "CLOUDY"
    elif composite <= 80:
        classification = "Greed"
        emoji = "⛅"
        condition = "CLEARING"
    else:
        classification = "Extreme Greed"
        emoji = "☀️"
        condition = "SHINY"
    
    result = {
        "fetched_at": datetime.now().isoformat(),
        "composite_score": composite,
        "classification": classification,
        "condition": condition,
        "emoji": emoji,
        "components": {
            "stock_fear_greed": round(stock_score, 1),
            "crypto_fear_greed": crypto_score,
            "vix_inverted": round(vix_score, 1)
        },
        "weights": {
            "stock": 0.4,
            "crypto": 0.3,
            "vix": 0.3
        }
    }
    
    return result


def get_nato_data():
    """Return NATO defense spending data (official 2023 data)"""
    # Source: NATO Secretary General's Annual Report 2023
    # https://www.nato.int/nato_static_fl2014/assets/pdf/2023/7/pdf/230707-def-exp-2023-en.pdf
    
    data = {
        "fetched_at": datetime.now().isoformat(),
        "source": "NATO Secretary General Annual Report 2023",
        "target_pct": 2.0,
        "year": 2023,
        "countries": [
            {"name": "United States", "flag": "🇺🇸", "spending_bn": 886.0, "pct_gdp": 3.49, "meets_target": True},
            {"name": "Poland", "flag": "🇵🇱", "spending_bn": 31.6, "pct_gdp": 3.90, "meets_target": True},
            {"name": "Greece", "flag": "🇬🇷", "spending_bn": 9.4, "pct_gdp": 3.01, "meets_target": True},
            {"name": "United Kingdom", "flag": "🇬🇧", "spending_bn": 68.5, "pct_gdp": 2.07, "meets_target": True},
            {"name": "Estonia", "flag": "🇪🇪", "spending_bn": 1.1, "pct_gdp": 2.73, "meets_target": True},
            {"name": "Lithuania", "flag": "🇱🇹", "spending_bn": 1.8, "pct_gdp": 2.54, "meets_target": True},
            {"name": "Latvia", "flag": "🇱🇻", "spending_bn": 1.0, "pct_gdp": 2.27, "meets_target": True},
            {"name": "Romania", "flag": "🇷🇴", "spending_bn": 7.9, "pct_gdp": 2.44, "meets_target": True},
            {"name": "Hungary", "flag": "🇭🇺", "spending_bn": 4.4, "pct_gdp": 2.43, "meets_target": True},
            {"name": "Slovakia", "flag": "🇸🇰", "spending_bn": 2.3, "pct_gdp": 2.03, "meets_target": True},
            {"name": "France", "flag": "🇫🇷", "spending_bn": 53.6, "pct_gdp": 1.90, "meets_target": False},
            {"name": "Türkiye", "flag": "🇹🇷", "spending_bn": 21.5, "pct_gdp": 1.31, "meets_target": False},
            {"name": "Germany", "flag": "🇩🇪", "spending_bn": 68.0, "pct_gdp": 1.57, "meets_target": False},
            {"name": "Italy", "flag": "🇮🇹", "spending_bn": 32.0, "pct_gdp": 1.46, "meets_target": False},
            {"name": "Canada", "flag": "🇨🇦", "spending_bn": 26.9, "pct_gdp": 1.38, "meets_target": False},
            {"name": "Spain", "flag": "🇪🇸", "spending_bn": 17.0, "pct_gdp": 1.26, "meets_target": False},
        ],
        "summary": {
            "total_spending_bn": 1341.0,
            "countries_meeting_target": 11,
            "countries_below_target": 20,
            "avg_pct_gdp": 2.03
        }
    }
    
    # Sort by % GDP
    data["countries"] = sorted(data["countries"], key=lambda x: x["pct_gdp"], reverse=True)
    
    return data


def main():
    print("=" * 50)
    print("MONARCH CASTLE - DATA COLLECTOR")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 50)
    
    # Fetch and save all data
    print("\n[1/7] Fetching Crypto Fear & Greed Index...")
    data = fetch_fear_greed_crypto()
    if data:
        save_json("crypto_fear_greed.json", data)
    
    print("\n[2/7] Fetching VIX...")
    data = fetch_vix()
    if data:
        save_json("vix.json", data)
    
    print("\n[3/7] Fetching Oil Prices...")
    data = fetch_oil_prices()
    if data:
        save_json("oil_prices.json", data)
    
    print("\n[4/7] Fetching Baltic Dry Index...")
    data = fetch_baltic_dry()
    if data:
        save_json("baltic_dry.json", data)
    
    print("\n[5/7] Fetching S&P 500...")
    data = fetch_sp500()
    if data:
        save_json("sp500.json", data)
    
    print("\n[6/7] Getting NATO Data...")
    data = get_nato_data()
    save_json("nato_spending.json", data)
    
    print("\n[7/7] Calculating Sentiment Index...")
    data = calculate_sentiment_index()
    save_json("sentiment_index.json", data)
    
    print("\n" + "=" * 50)
    print("DATA COLLECTION COMPLETE")
    print(f"Files saved to: {DATA_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
