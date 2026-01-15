# ══════════════════════════════════════════════════════════════════════════════
# MONARCH CASTLE TECHNOLOGIES - OFFICIAL ECONOMIC DATA SOURCE
# ══════════════════════════════════════════════════════════════════════════════
# Source: BBVA Research & Garanti BBVA IR (Forecasts as of January 2026)
# Last Update: 2026-01-15
# ══════════════════════════════════════════════════════════════════════════════

from datetime import datetime

LAST_UPDATED = "2026-01-15"
DATA_SOURCE = "BBVA Research (https://www.bbvaresearch.com/en/forecasts/)"

# ══════════════════════════════════════════════════════════════════════════════
# TÜRKIYE FORECASTS
# ══════════════════════════════════════════════════════════════════════════════
turkey_forecasts = {
    "2024": {
        "gdp_growth": 3.30,           # GDP Growth (%)
        "cpi_inflation_eop": 44.40,   # CPI Inflation End of Period (%)
        "usd_try_eop": 35.28,         # USD/TRY End of Period
        "eur_try_eop": 36.74,         # EUR/TRY End of Period
        "policy_rate_eop": 47.50,     # 1-Week Repo Rate (Policy Rate %)
        "fiscal_balance_gdp": -4.70,  # Fiscal Balance (% of GDP)
        "current_account_gdp": -0.70, # Current Account Balance (% of GDP)
        "trade_balance_gdp": -6.10,   # Foreign Trade Balance (% of GDP)
    },
    "2025": {
        "gdp_growth": 3.70,
        "cpi_inflation_eop": 31.50,
        "usd_try_eop": 43.00,
        "eur_try_eop": 50.00,
        "policy_rate_eop": 38.00,
        "fiscal_balance_gdp": -3.60,
        "current_account_gdp": -1.30,
        "trade_balance_gdp": -5.90,
    },
    "2026": {
        "gdp_growth": 4.00,
        "cpi_inflation_eop": 25.00,
        "usd_try_eop": 52.00,
        "eur_try_eop": 62.28,
        "policy_rate_eop": 32.00,
        "fiscal_balance_gdp": -3.70,
        "current_account_gdp": -1.50,
        "trade_balance_gdp": -6.40,
    }
}

# Derived metrics for Turkey
turkey_derived = {
    "2025": {
        "real_interest_rate": turkey_forecasts["2025"]["policy_rate_eop"] - turkey_forecasts["2025"]["cpi_inflation_eop"],  # 6.5%
        "currency_depreciation_yoy": ((43.00 - 35.28) / 35.28) * 100,  # ~21.9%
        "loan_rate_commercial_est": 48.0,   # Estimated commercial loan rate
        "loan_rate_consumer_est": 55.0,     # Estimated consumer loan rate
        "ppi_inflation_est": 29.0,          # Estimated producer inflation
    },
    "2026": {
        "real_interest_rate": turkey_forecasts["2026"]["policy_rate_eop"] - turkey_forecasts["2026"]["cpi_inflation_eop"],  # 7%
        "currency_depreciation_yoy": ((52.00 - 43.00) / 43.00) * 100,  # ~20.9%
        "loan_rate_commercial_est": 38.0,
        "loan_rate_consumer_est": 45.0,
        "ppi_inflation_est": 22.0,
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# UNITED STATES FORECASTS
# ══════════════════════════════════════════════════════════════════════════════
us_forecasts = {
    "2024": {
        "gdp_growth": 2.80,
        "cpi_inflation_4q": 2.70,     # Inflation 4Q/4Q
        "cpi_inflation_avg": 3.00,    # Average annual inflation
        "fed_rate_eop": 4.50,         # Fed Funds Rate End of Period
        "fed_rate_avg": 5.27,
        "treasury_10y_eop": 4.40,     # 10-Year Treasury Yield EoP
        "treasury_10y_avg": 4.20,
    },
    "2025": {
        "gdp_growth": 2.00,
        "cpi_inflation_4q": 3.00,
        "cpi_inflation_avg": 2.80,
        "fed_rate_eop": 3.75,
        "fed_rate_avg": 4.35,
        "treasury_10y_eop": 4.20,
        "treasury_10y_avg": 4.30,
    },
    "2026": {
        "gdp_growth": 1.90,
        "cpi_inflation_4q": 2.90,
        "cpi_inflation_avg": 2.90,
        "fed_rate_eop": 3.25,
        "fed_rate_avg": 3.56,
        "treasury_10y_eop": 4.10,
        "treasury_10y_avg": 4.10,
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# EUROZONE FORECASTS
# ══════════════════════════════════════════════════════════════════════════════
eurozone_forecasts = {
    "2024": {
        "gdp_growth": 0.80,
        "cpi_inflation_eop": 2.50,
        "cpi_inflation_avg": 2.40,
        "ecb_rate_eop": 3.00,
        "ecb_rate_avg": 3.69,
        "bund_10y_eop": 2.22,
        "bund_10y_avg": 2.34,
        "usd_eur_eop": 1.05,
        "usd_eur_avg": 1.08,
    },
    "2025": {
        "gdp_growth": 1.30,
        "cpi_inflation_eop": 2.00,
        "cpi_inflation_avg": 2.10,
        "ecb_rate_eop": 2.00,
        "ecb_rate_avg": 2.21,
        "bund_10y_eop": 2.70,
        "bund_10y_avg": 2.63,
        "usd_eur_eop": 1.18,
        "usd_eur_avg": 1.13,
    },
    "2026": {
        "gdp_growth": 1.00,
        "cpi_inflation_eop": 1.90,
        "cpi_inflation_avg": 1.80,
        "ecb_rate_eop": 2.00,
        "ecb_rate_avg": 2.00,
        "bund_10y_eop": 2.80,
        "bund_10y_avg": 2.76,
        "usd_eur_eop": 1.22,
        "usd_eur_avg": 1.20,
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# COMMODITIES FORECASTS
# ══════════════════════════════════════════════════════════════════════════════
commodities_forecasts = {
    "2024": {
        "brent_oil_usd": 80.20,        # Brent Oil ($/barrel) Year Average
        "copper_usd_lb": 417.00,       # Copper (¢/lb) Year Average
        "soybean_usd_ton": 405.20,     # Soybean ($/ton) Year Average
    },
    "2025": {
        "brent_oil_usd": 68.60,
        "copper_usd_lb": 444.00,
        "soybean_usd_ton": 380.40,
    },
    "2026": {
        "brent_oil_usd": 63.30,
        "copper_usd_lb": 461.00,
        "soybean_usd_ton": 394.60,
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# SECTORAL OUTLOOK (For CHI - Commercial Hoarding Index)
# ══════════════════════════════════════════════════════════════════════════════
sectoral_outlook = {
    "automotive": {
        "import_dependency": 0.75,
        "fx_sensitivity": "High",
        "price_increase_2025": 40.0,
        "note": "High FX pass-through, ÖTV tax burden"
    },
    "electronics": {
        "import_dependency": 0.90,
        "fx_sensitivity": "Very High",
        "price_increase_2025": 45.0,
        "note": "Almost entirely imported, USD pricing"
    },
    "textile": {
        "import_dependency": 0.40,
        "fx_sensitivity": "Medium",
        "price_increase_2025": 25.0,
        "note": "Mixed local/import, labor cost sensitive"
    },
    "food_retail": {
        "import_dependency": 0.20,
        "fx_sensitivity": "Low",
        "price_increase_2025": 30.0,
        "note": "Mostly local, but sticky services inflation"
    },
    "construction": {
        "import_dependency": 0.50,
        "fx_sensitivity": "Medium-High",
        "price_increase_2025": 35.0,
        "note": "Iron/steel import dependent"
    },
    "energy": {
        "import_dependency": 0.95,
        "fx_sensitivity": "Very High",
        "price_increase_2025": 50.0,
        "note": "Oil/gas import dependent"
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# RISK FACTORS
# ══════════════════════════════════════════════════════════════════════════════
risk_factors = [
    "US-China Trade War Escalation",
    "Europe Defense Spending Pressure (Trump Factor)",
    "Sticky Service Inflation in Turkey",
    "Fed Rate Path Uncertainty",
    "Geopolitical Risks (Middle East)",
    "Turkey Credit Rating Risk",
    "Energy Price Shocks",
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_turkey_forecast(year="2025"):
    """Get Turkey economic forecast for a specific year."""
    return turkey_forecasts.get(str(year), {})

def get_inflation_spread():
    """Calculate Turkey vs Global inflation spread."""
    tr_inf = turkey_forecasts["2025"]["cpi_inflation_eop"]
    us_inf = us_forecasts["2025"]["cpi_inflation_avg"]
    eu_inf = eurozone_forecasts["2025"]["cpi_inflation_avg"]
    return {
        "turkey": tr_inf,
        "us": us_inf,
        "eurozone": eu_inf,
        "tr_vs_us_spread": tr_inf - us_inf,
        "tr_vs_eu_spread": tr_inf - eu_inf,
    }

def get_rate_differential():
    """Calculate interest rate differentials (carry trade attractiveness)."""
    tr_rate = turkey_forecasts["2025"]["policy_rate_eop"]
    us_rate = us_forecasts["2025"]["fed_rate_eop"]
    eu_rate = eurozone_forecasts["2025"]["ecb_rate_eop"]
    return {
        "turkey_rate": tr_rate,
        "us_rate": us_rate,
        "eu_rate": eu_rate,
        "tr_us_carry": tr_rate - us_rate,  # ~34.25%
        "tr_eu_carry": tr_rate - eu_rate,  # ~36%
    }

def get_chi_decision(sector="electronics"):
    """Commercial Hoarding Index - Should SMEs stock up?"""
    sector_data = sectoral_outlook.get(sector, sectoral_outlook["food_retail"])
    expected_hike = sector_data["price_increase_2025"]
    loan_cost = turkey_derived["2025"]["loan_rate_commercial_est"]
    
    chi_score = expected_hike - loan_cost
    
    return {
        "sector": sector,
        "expected_price_hike": expected_hike,
        "loan_cost": loan_cost,
        "chi_score": chi_score,
        "decision": "STOCK UP (Arbitrage)" if chi_score > 0 else "HOLD CASH",
        "reasoning": f"Price hike ({expected_hike}%) {'>' if chi_score > 0 else '<'} Loan cost ({loan_cost}%)"
    }

def get_election_inputs(year="2026"):
    """Get inputs for Election Predictor models."""
    data = turkey_forecasts.get(str(year), turkey_forecasts["2026"])
    return {
        "inflation": data["cpi_inflation_eop"],
        "gdp_growth": data["gdp_growth"],
        "currency_depreciation": turkey_derived.get(str(year), {}).get("currency_depreciation_yoy", 20.0),
        "policy_rate": data["policy_rate_eop"],
        "current_account": data["current_account_gdp"],
    }

# ══════════════════════════════════════════════════════════════════════════════
# QUICK TEST
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("MONARCH CASTLE - ECONOMIC DATA MODULE")
    print("=" * 60)
    print(f"\nData Source: {DATA_SOURCE}")
    print(f"Last Updated: {LAST_UPDATED}")
    
    print("\n--- TURKEY 2025 FORECAST ---")
    for k, v in turkey_forecasts["2025"].items():
        print(f"  {k}: {v}")
    
    print("\n--- INFLATION SPREAD ---")
    spread = get_inflation_spread()
    print(f"  Turkey: {spread['turkey']}% vs US: {spread['us']}% (Spread: {spread['tr_vs_us_spread']:.1f}%)")
    
    print("\n--- CARRY TRADE ---")
    carry = get_rate_differential()
    print(f"  TR-US Carry: {carry['tr_us_carry']:.2f}%")
    
    print("\n--- COMMERCIAL HOARDING INDEX ---")
    chi = get_chi_decision("electronics")
    print(f"  {chi['sector']}: {chi['decision']} (CHI Score: {chi['chi_score']:+.1f})")
