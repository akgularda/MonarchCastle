# ══════════════════════════════════════════════════════════════════════════════
# MONARCH CASTLE TECHNOLOGIES - INDEX DEFINITIONS & METHODOLOGIES
# ══════════════════════════════════════════════════════════════════════════════
# These are the official economic indexes developed by Monarch Castle.
# Each index has a methodology based on real economic theory.
# ══════════════════════════════════════════════════════════════════════════════

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class IndexCategory(Enum):
    CONSUMER = "Consumer & Lifestyle (B2C)"
    SME = "SME & Trade (B2B)"
    REAL_ESTATE = "Real Estate & Urban"
    MACRO = "Macro & Prestige"
    BEHAVIORAL = "Behavioral Economics"
    VIRAL = "Alternative & Viral"

# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY 1: CONSUMER & LIFESTYLE (B2C)
# Target: White-collar workers, students, inflation avoiders
# ══════════════════════════════════════════════════════════════════════════════

CONSUMER_INDEXES = {
    "IPI": {
        "name": "iPhone Parity Index",
        "code": "IPI",
        "category": IndexCategory.CONSUMER,
        "formula": "(Global_iPhone_Price_USD * Expected_FX * Tax_Multiplier) / (Monthly_Salary * Expected_Raise)",
        "methodology": "Purchase Power Parity applied to tech goods",
        "interpretation": {
            "score > 1.5": "BUY NOW - Purchasing power eroding fast",
            "score 1.0-1.5": "NEUTRAL - Wait for sales",
            "score < 1.0": "DEFER - Prices may stabilize"
        },
        "inputs": ["iPhone Price ($)", "Current FX", "Future FX (6m)", "Monthly Salary", "Expected Salary Raise (%)"],
        "source": "Apple, TCMB, TURKSTAT"
    },
    
    "DNI": {
        "name": "Date Night Inflation Index",
        "code": "DNI",
        "category": IndexCategory.CONSUMER,
        "formula": "(2 * Cinema_Ticket + Average_Dinner + Taxi_Fare) monthly change",
        "methodology": "Real youth spending basket vs official CPI",
        "interpretation": {
            "DNI > CPI + 5%": "Youth inflation significantly higher than official",
            "DNI ≈ CPI": "Official inflation reflects reality",
            "DNI < CPI": "Youth benefiting from subsidies/discounts"
        },
        "inputs": ["Cinema Ticket Price", "Average Dinner Price", "Taxi Fare (10km)"],
        "source": "Manual collection / Getir/Yemeksepeti API"
    },
    
    "PTW": {
        "name": "Protein-to-Wage Ratio",
        "code": "PTW",
        "category": IndexCategory.CONSUMER,
        "formula": "Minimum_Wage / Red_Meat_Price_Per_Kg",
        "methodology": "Pure welfare measurement - how much protein can labor buy?",
        "interpretation": {
            "PTW > 15": "Good welfare (15+ kg meat per min wage)",
            "PTW 10-15": "Moderate",
            "PTW < 10": "Protein poverty zone"
        },
        "inputs": ["Minimum Wage (TRY)", "Red Meat Price (TRY/kg)"],
        "source": "Official Gazette, TURKSTAT"
    },
    
    "SLL": {
        "name": "Starbucks Latte Line",
        "code": "SLL",
        "category": IndexCategory.CONSUMER,
        "formula": "Latte_Price / Hourly_Minimum_Wage",
        "methodology": "Labor purchasing power parity (PPP)",
        "interpretation": {
            "ratio > 1.0": "1 hour of work < 1 latte (Severe inequality)",
            "ratio 0.5-1.0": "Moderate",
            "ratio < 0.5": "Affordable luxury"
        },
        "inputs": ["Starbucks Latte Price", "Hourly Minimum Wage"],
        "source": "Starbucks Menu, Official Gazette"
    },
    
    "DSF": {
        "name": "Digital Subscription Fatigue Index",
        "code": "DSF",
        "category": IndexCategory.CONSUMER,
        "formula": "(Netflix + Spotify + YouTube + Disney+) / Disposable_Income * 100",
        "methodology": "Subscription churn risk prediction",
        "interpretation": {
            "DSF > 5%": "High churn risk - users will cancel",
            "DSF 2-5%": "Moderate",
            "DSF < 2%": "Low risk"
        },
        "inputs": ["Monthly Subscription Total", "Monthly Disposable Income"],
        "source": "Subscription prices, salary data"
    },
    
    "EFS": {
        "name": "Erasmus Feasibility Score",
        "code": "EFS",
        "category": IndexCategory.CONSUMER,
        "formula": "(EUR_FX * Average_EU_Rent) / (KYK_Grant + Family_Support)",
        "methodology": "Overseas study dream feasibility",
        "interpretation": {
            "EFS > 2.0": "IMPOSSIBLE without external funding",
            "EFS 1.0-2.0": "Feasible with part-time work",
            "EFS < 1.0": "Comfortable"
        },
        "inputs": ["EUR/TRY Rate", "Average EU Rent (€)", "KYK Grant (TRY)", "Family Support (TRY)"],
        "source": "TCMB, Erasmus data"
    },
    
    "HAI": {
        "name": "Holiday Arbitrage Index",
        "code": "HAI",
        "category": IndexCategory.CONSUMER,
        "formula": "(Antalya_Hotel_Price) vs (Greek_Island_Hotel + Visa + Ferry)",
        "methodology": "Vacation arbitrage opportunity detection",
        "interpretation": {
            "HAI > 1.0": "GO ABROAD - Turkey more expensive",
            "HAI ≈ 1.0": "Equal",
            "HAI < 1.0": "STAY LOCAL - Turkey cheaper"
        },
        "inputs": ["Antalya 5-Star Hotel (7 nights)", "Greek Island equivalent + travel"],
        "source": "Booking.com, travel sites"
    },
    
    "UCB": {
        "name": "Used Car Bubble Meter",
        "code": "UCB",
        "category": IndexCategory.CONSUMER,
        "formula": "Used_Car_Price / (New_Car_Price + SCT_Tax)",
        "methodology": "Bubble detection when used > new",
        "interpretation": {
            "UCB > 1.0": "BUBBLE - SELL used car immediately",
            "UCB 0.7-1.0": "Elevated",
            "UCB < 0.7": "Normal depreciation"
        },
        "inputs": ["Used Car Price (3 years old)", "New Car Price", "SCT Tax Amount"],
        "source": "Sahibinden.com, ODD"
    },
    
    "GHI": {
        "name": "Gamer Hardware Index",
        "code": "GHI",
        "category": IndexCategory.CONSUMER,
        "formula": "GPU_Price_TRY / (Crypto_Mining_Monthly_Revenue_TRY * 12)",
        "methodology": "ROI on gaming hardware as mining asset",
        "interpretation": {
            "GHI < 12": "BUY - GPU pays itself in under 1 year",
            "GHI 12-24": "Moderate ROI",
            "GHI > 24": "WAIT - Mining not profitable"
        },
        "inputs": ["GPU Price", "Estimated Mining Revenue/Month"],
        "source": "Amazon, Hepsiburada, Mining calculators"
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY 2: SME & TRADE (B2B)
# Target: Shop owners, small businesses, e-commerce sellers
# ══════════════════════════════════════════════════════════════════════════════

SME_INDEXES = {
    "CHI": {
        "name": "Commercial Hoarding Index",
        "code": "CHI",
        "category": IndexCategory.SME,
        "formula": "Sector_Inflation_Expectation - Commercial_Loan_Rate",
        "methodology": "Arbitrage: Store goods if they appreciate faster than financing cost",
        "interpretation": {
            "CHI > 0": "STOCK UP - Goods beat loan cost",
            "CHI ≈ 0": "Equilibrium",
            "CHI < 0": "HOLD CASH - Financing too expensive"
        },
        "inputs": ["Sector (Electronics, Textile, Auto)", "Commercial Loan Rate (%)"],
        "source": "TCMB, sector associations"
    },
    
    "MCI": {
        "name": "Menu Cost Indicator",
        "code": "MCI",
        "category": IndexCategory.SME,
        "formula": "Food_Inflation_Volatility (std dev of monthly changes)",
        "methodology": "How often restaurants must reprint menus",
        "interpretation": {
            "MCI > 3.0": "Reprint weekly",
            "MCI 1.5-3.0": "Reprint monthly",
            "MCI < 1.5": "Quarterly reprints OK"
        },
        "inputs": ["Monthly food inflation data (12 months)"],
        "source": "TURKSTAT"
    },
    
    "MWS": {
        "name": "Minimum Wage Shock Score",
        "code": "MWS",
        "category": IndexCategory.SME,
        "formula": "Labor_Cost_Increase / Expected_Revenue_Growth",
        "methodology": "Bankruptcy risk from min wage hikes",
        "interpretation": {
            "MWS > 1.5": "CRITICAL - May need layoffs",
            "MWS 1.0-1.5": "Squeeze - Cut margins",
            "MWS < 1.0": "Manageable"
        },
        "inputs": ["Current Payroll", "New Min Wage", "Expected Revenue Growth (%)"],
        "source": "Official Gazette, company data"
    },
    
    "IRM": {
        "name": "Import Reliance Meter",
        "code": "IRM",
        "category": IndexCategory.SME,
        "formula": "Import_Share_of_COGS * FX_Volatility_30d",
        "methodology": "Currency shock vulnerability",
        "interpretation": {
            "IRM > 50": "HIGH RISK - Hedge or switch suppliers",
            "IRM 20-50": "Moderate",
            "IRM < 20": "Low exposure"
        },
        "inputs": ["% of inputs imported", "30-day FX volatility"],
        "source": "Company data, TCMB"
    },
    
    "FRB": {
        "name": "Freight Rate Barometer",
        "code": "FRB",
        "category": IndexCategory.SME,
        "formula": "Fuel_Price_Change + Logistics_Index_Change",
        "methodology": "Shipping cost prediction",
        "interpretation": {
            "FRB > 10": "Shipping costs rising sharply",
            "FRB 0-10": "Moderate increase",
            "FRB < 0": "Shipping getting cheaper"
        },
        "inputs": ["Diesel Price Change (%)", "Container Rate Change (%)"],
        "source": "EPDK, Freightos"
    },
    
    "BPS": {
        "name": "Bankruptcy Probability Score (Z-Score Lite)",
        "code": "BPS",
        "category": IndexCategory.SME,
        "formula": "(Current_Assets - Current_Liabilities) / Annual_Revenue",
        "methodology": "Simplified Altman Z-Score",
        "interpretation": {
            "BPS > 0.3": "Safe zone",
            "BPS 0.1-0.3": "Gray zone",
            "BPS < 0.1": "Distress zone"
        },
        "inputs": ["Current Assets", "Current Liabilities", "Annual Revenue"],
        "source": "Financial statements"
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY 3: REAL ESTATE & URBAN
# ══════════════════════════════════════════════════════════════════════════════

REAL_ESTATE_INDEXES = {
    "ROB": {
        "name": "Rent-or-Buy Ratio",
        "code": "ROB",
        "category": IndexCategory.REAL_ESTATE,
        "formula": "Home_Price / (Monthly_Rent * 12)",
        "methodology": "Payback period in years",
        "interpretation": {
            "ROB > 25": "RENT - Buying takes 25+ years to pay off",
            "ROB 15-25": "Market equilibrium",
            "ROB < 15": "BUY - Attractive payback"
        },
        "inputs": ["Home Price", "Monthly Rent"],
        "source": "Sahibinden, REIDIN"
    },
    
    "GSM": {
        "name": "Gentrification Speedometer",
        "code": "GSM",
        "category": IndexCategory.REAL_ESTATE,
        "formula": "Third_Wave_Coffee_Shop_Count_Change + Rent_Growth_Rate",
        "methodology": "Hipster invasion = rent explosion warning",
        "interpretation": {
            "GSM > 30": "Rapid gentrification",
            "GSM 10-30": "Moderate change",
            "GSM < 10": "Stable neighborhood"
        },
        "inputs": ["New coffee shop openings", "YoY rent change (%)"],
        "source": "Foursquare, rental data"
    },
    
    "SHP": {
        "name": "Student Housing Pressure Index",
        "code": "SHP",
        "category": IndexCategory.REAL_ESTATE,
        "formula": "University_Quota / (Dorm_Beds + Rental_Units_Near_Campus)",
        "methodology": "September rent spike predictor",
        "interpretation": {
            "SHP > 5": "EXTREME pressure - rents will spike",
            "SHP 2-5": "Tight market",
            "SHP < 2": "Adequate supply"
        },
        "inputs": ["University intake", "Available housing units"],
        "source": "YÖK, rental listings"
    },
    
    "CCC": {
        "name": "Commute Cost Calculator",
        "code": "CCC",
        "category": IndexCategory.REAL_ESTATE,
        "formula": "(Commute_Hours * Hourly_Wage) + Monthly_Transport_Cost",
        "methodology": "True cost of living far from work",
        "interpretation": {
            "output": "Compare to rent difference between locations"
        },
        "inputs": ["Daily commute hours", "Hourly wage", "Monthly transport cost"],
        "source": "Google Maps, salary data"
    },
    
    "AVL": {
        "name": "Airbnb vs Long-term Rent Index",
        "code": "AVL",
        "category": IndexCategory.REAL_ESTATE,
        "formula": "(Daily_Rate * Occupancy_Days) / Monthly_Long_Term_Rent",
        "methodology": "Short-term vs long-term rental ROI",
        "interpretation": {
            "AVL > 1.5": "Airbnb significantly better",
            "AVL 0.8-1.5": "Similar returns",
            "AVL < 0.8": "Long-term tenant better"
        },
        "inputs": ["Airbnb daily rate", "Occupancy rate (%)", "Long-term monthly rent"],
        "source": "AirDNA, rental listings"
    },
    
    "EAD": {
        "name": "Earthquake Anxiety Discount",
        "code": "EAD",
        "category": IndexCategory.REAL_ESTATE,
        "formula": "(New_Building_Price - Old_Building_Price) / New_Building_Price * 100",
        "methodology": "Risk premium for old buildings",
        "interpretation": {
            "EAD > 40%": "High earthquake anxiety priced in",
            "EAD 20-40%": "Moderate",
            "EAD < 20%": "Risk underpriced"
        },
        "inputs": ["New building price (same location)", "Old building price"],
        "source": "Real estate listings"
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY 4: MACRO & PRESTIGE
# Target: Academics, politicians, consultants
# ══════════════════════════════════════════════════════════════════════════════

MACRO_INDEXES = {
    "MR": {
        "name": "Misery Radar (Modified Okun Index)",
        "code": "MR",
        "category": IndexCategory.MACRO,
        "formula": "(Food_Inflation + Rent_Increase) + Youth_Unemployment",
        "methodology": "Real street-level misery vs headline stats",
        "interpretation": {
            "MR > 80": "EXTREME MISERY",
            "MR 50-80": "High stress",
            "MR < 50": "Manageable"
        },
        "inputs": ["Food Inflation (%)", "Rent Increase (%)", "Youth Unemployment (%)"],
        "source": "TURKSTAT"
    },
    
    "ESP": {
        "name": "Election Surprise Probability",
        "code": "ESP",
        "category": IndexCategory.MACRO,
        "formula": "Economic_Confidence_Decline * FX_Volatility_Factor",
        "methodology": "Economic pain -> political change likelihood",
        "interpretation": {
            "ESP > 60": "HIGH upset probability",
            "ESP 30-60": "Competitive race",
            "ESP < 30": "Incumbent likely safe"
        },
        "inputs": ["Consumer Confidence Index", "6-month FX volatility"],
        "source": "TCMB, TURKSTAT"
    },
    
    "BDI": {
        "name": "Brain Drain Index",
        "code": "BDI",
        "category": IndexCategory.MACRO,
        "formula": "(TR_Engineer_Salary / TR_Rent) / (DE_Engineer_Salary / DE_Rent)",
        "methodology": "Is emigration economically rational?",
        "interpretation": {
            "BDI < 0.5": "STRONG incentive to leave",
            "BDI 0.5-0.8": "Moderate incentive",
            "BDI > 0.8": "Staying is rational"
        },
        "inputs": ["Turkish engineer salary", "Turkish rent", "German equivalents"],
        "source": "Glassdoor, Numbeo"
    },
    
    "DFI": {
        "name": "Dollarization Fever Index",
        "code": "DFI",
        "category": IndexCategory.MACRO,
        "formula": "FX_Deposit_Share_Change (DTH) over 3 months",
        "methodology": "Trust in local currency erosion",
        "interpretation": {
            "DFI > +5%": "Rapid dollarization (panic)",
            "DFI -2% to +5%": "Normal fluctuation",
            "DFI < -2%": "De-dollarization (confidence returning)"
        },
        "inputs": ["FX deposit share this month", "FX deposit share 3 months ago"],
        "source": "TCMB"
    },
    
    "SEE": {
        "name": "Shadow Economy Estimator",
        "code": "SEE",
        "category": IndexCategory.MACRO,
        "formula": "Electricity_Consumption_Growth - GDP_Growth",
        "methodology": "Unregistered economy proxy",
        "interpretation": {
            "SEE > 3%": "Large shadow economy",
            "SEE 0-3%": "Normal",
            "SEE < 0": "Formalization happening"
        },
        "inputs": ["Electricity consumption growth (%)", "GDP growth (%)"],
        "source": "TEİAŞ, TURKSTAT"
    },
    
    "TAR": {
        "name": "Tourism Revenue at Risk",
        "code": "TAR",
        "category": IndexCategory.MACRO,
        "formula": "Turkey_Price_Index vs Competitor_Average (Spain, Greece, Egypt)",
        "methodology": "Tourist leakage risk",
        "interpretation": {
            "TAR > 1.2": "Losing competitiveness",
            "TAR 0.8-1.2": "Competitive",
            "TAR < 0.8": "Gaining share"
        },
        "inputs": ["Turkey tourism price index", "Competitor average index"],
        "source": "Tourism ministry, booking sites"
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY 5: BEHAVIORAL ECONOMICS
# ══════════════════════════════════════════════════════════════════════════════

BEHAVIORAL_INDEXES = {
    "FOMO": {
        "name": "Fear of Missing Out Index",
        "code": "FOMO",
        "category": IndexCategory.BEHAVIORAL,
        "formula": "Social_Media_Hype_Volume / Price_Rise_Rate",
        "methodology": "Panic buying detection",
        "interpretation": {
            "FOMO > 2.0": "Extreme FOMO - bubble territory",
            "FOMO 1.0-2.0": "Elevated interest",
            "FOMO < 1.0": "Rational buying"
        },
        "inputs": ["Social media mention count", "Price increase (%)"],
        "source": "Twitter/X API, price data"
    },
    
    "CCD": {
        "name": "Consumer Confidence Divergence",
        "code": "CCD",
        "category": IndexCategory.BEHAVIORAL,
        "formula": "Survey_Optimism_Score - Actual_Spending_Growth",
        "methodology": "People lie in surveys, wallets don't",
        "interpretation": {
            "CCD > 10": "People say fine, but spending says crisis",
            "CCD -10 to 10": "Aligned",
            "CCD < -10": "Spending better than mood"
        },
        "inputs": ["Consumer confidence survey", "Retail spending growth"],
        "source": "TURKSTAT"
    },
    
    "LLE": {
        "name": "Luxury Lipstick Effect",
        "code": "LLE",
        "category": IndexCategory.BEHAVIORAL,
        "formula": "Small_Luxury_Sales_Growth during GDP_Decline",
        "methodology": "Crisis depth measurement via affordable luxuries",
        "interpretation": {
            "LLE high + GDP down": "Deep psychological crisis",
            "LLE normal": "Standard recession",
        },
        "inputs": ["Lipstick/chocolate/small luxury sales", "GDP change"],
        "source": "Retail data"
    },
    
    "HBD": {
        "name": "Herd Behavior Detector",
        "code": "HBD",
        "category": IndexCategory.BEHAVIORAL,
        "formula": "Sudden_Volume_Spike + Directional_Consensus",
        "methodology": "Trend exhaustion signal",
        "interpretation": {
            "HBD > 90%": "Everyone on same side - reversal imminent",
            "HBD 60-90%": "Strong trend",
            "HBD < 60%": "Mixed opinions"
        },
        "inputs": ["Trading volume", "Buy/sell ratio"],
        "source": "BIST, Borsa Istanbul"
    },
    
    "PI": {
        "name": "Patience Index (Time Preference)",
        "code": "PI",
        "category": IndexCategory.BEHAVIORAL,
        "formula": "Average_Term_Deposit_Maturity_Days",
        "methodology": "Society's ability to plan ahead",
        "interpretation": {
            "PI decreasing": "Panic - people want money NOW",
            "PI stable": "Normal time preference",
            "PI increasing": "Confidence in future"
        },
        "inputs": ["Average deposit maturity (days)"],
        "source": "TCMB"
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY 6: ALTERNATIVE & VIRAL
# Target: Social media engagement, fun economics
# ══════════════════════════════════════════════════════════════════════════════

VIRAL_INDEXES = {
    "MI": {
        "name": "Menemen Index",
        "code": "MI",
        "category": IndexCategory.VIRAL,
        "formula": "Tomato + Pepper + Egg + Bread price basket",
        "methodology": "Bachelor's inflation - real cost of basic meal",
        "interpretation": {
            "output": "Monthly change in TRY for one serving"
        },
        "inputs": ["Tomato (kg)", "Pepper (kg)", "Eggs (10)", "Bread (1)"],
        "source": "Migros, A101, Şok"
    },
    
    "DKI": {
        "name": "Döner Kebab Index (Turkey's Big Mac)",
        "code": "DKI",
        "category": IndexCategory.VIRAL,
        "formula": "City-by-city 100g meat döner price comparison",
        "methodology": "PPP across Turkish cities",
        "interpretation": {
            "output": "Cheapest to most expensive cities ranking"
        },
        "inputs": ["100g döner price per city"],
        "source": "Yemeksepeti, Getir"
    },
    
    "HPI": {
        "name": "Haircut Price Index",
        "code": "HPI",
        "category": IndexCategory.VIRAL,
        "formula": "Barber/Hairdresser price YoY change",
        "methodology": "Best proxy for service sector inflation",
        "interpretation": {
            "HPI > CPI": "Service inflation running hot",
            "HPI ≈ CPI": "Balanced",
            "HPI < CPI": "Services lagging (rare)"
        },
        "inputs": ["Haircut price this year", "Haircut price last year"],
        "source": "Manual survey"
    },
    
    "WCB": {
        "name": "Wedding Cost Bubble",
        "code": "WCB",
        "category": IndexCategory.VIRAL,
        "formula": "(Gold_Gifts + Wedding_Venue + White_Goods) / Median_Annual_Income",
        "methodology": "Is marriage economically impossible?",
        "interpretation": {
            "WCB > 3.0": "Marriage = 3+ years of income",
            "WCB 1.5-3.0": "Expensive but doable",
            "WCB < 1.5": "Affordable"
        },
        "inputs": ["Total wedding cost", "Median annual income"],
        "source": "Wedding industry data"
    },
    
    "DSM": {
        "name": "Dad Stress Meter",
        "code": "DSM",
        "category": IndexCategory.VIRAL,
        "formula": "(School_Fees + Shuttle + Utilities) / Monthly_Salary * 100",
        "methodology": "Family man's monthly survival ratio",
        "interpretation": {
            "DSM > 80%": "EXTREME STRESS",
            "DSM 50-80%": "High stress",
            "DSM < 50%": "Manageable"
        },
        "inputs": ["School fees", "Shuttle cost", "Utility bills", "Salary"],
        "source": "Manual survey"
    },
    
    "CFI": {
        "name": "Cat Food Inflation",
        "code": "CFI",
        "category": IndexCategory.VIRAL,
        "formula": "Premium_Cat_Food YoY price change",
        "methodology": "Hidden cost for 15M+ Turkish pet owners",
        "interpretation": {
            "output": "YoY % change"
        },
        "inputs": ["Cat food price current", "Cat food price 1 year ago"],
        "source": "Petshops, online retailers"
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# ALL INDEXES COMBINED
# ══════════════════════════════════════════════════════════════════════════════

ALL_INDEXES = {
    **CONSUMER_INDEXES,
    **SME_INDEXES,
    **REAL_ESTATE_INDEXES,
    **MACRO_INDEXES,
    **BEHAVIORAL_INDEXES,
    **VIRAL_INDEXES,
}

# ══════════════════════════════════════════════════════════════════════════════
# INDEX FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def calculate_ipi(iphone_usd_price: float, current_fx: float, future_fx_6m: float, 
                  monthly_salary: float, expected_raise_pct: float = 20.0) -> dict:
    """
    iPhone Parity Index - Should you buy tech now or wait?
    """
    tax_multiplier = 1.8  # Approx Turkish import tax + VAT
    
    current_cost = iphone_usd_price * current_fx * tax_multiplier
    future_cost = iphone_usd_price * future_fx_6m * tax_multiplier
    future_salary = monthly_salary * (1 + expected_raise_pct / 100)
    
    current_ratio = current_cost / monthly_salary
    future_ratio = future_cost / future_salary
    
    urgency_score = future_ratio / current_ratio
    
    if urgency_score > 1.2:
        decision = "BUY NOW - Purchasing power eroding"
    elif urgency_score > 1.0:
        decision = "SLIGHT URGENCY - Consider buying soon"
    else:
        decision = "WAIT - Prices may stabilize relative to income"
    
    return {
        "current_price_try": round(current_cost, 2),
        "future_price_try": round(future_cost, 2),
        "current_months_salary": round(current_ratio, 2),
        "future_months_salary": round(future_ratio, 2),
        "urgency_score": round(urgency_score, 3),
        "decision": decision
    }

def calculate_chi(sector: str, expected_sector_inflation: float, 
                  commercial_loan_rate: float) -> dict:
    """
    Commercial Hoarding Index - Should SMEs stock up on inventory?
    """
    chi_score = expected_sector_inflation - commercial_loan_rate
    
    if chi_score > 5:
        decision = "STRONG BUY - Stock up aggressively"
    elif chi_score > 0:
        decision = "BUY - Goods appreciate faster than loan cost"
    elif chi_score > -5:
        decision = "HOLD - Marginal"
    else:
        decision = "CASH - Keep liquidity"
    
    return {
        "sector": sector,
        "expected_inflation": expected_sector_inflation,
        "loan_cost": commercial_loan_rate,
        "chi_score": round(chi_score, 2),
        "decision": decision,
        "arbitrage_opportunity": chi_score > 0
    }

def calculate_misery_radar(food_inflation: float, rent_increase: float, 
                           youth_unemployment: float) -> dict:
    """
    Misery Radar - Real street-level economic stress
    """
    misery_score = food_inflation + rent_increase + youth_unemployment
    
    if misery_score > 100:
        level = "EXTREME"
        color = "red"
    elif misery_score > 70:
        level = "HIGH"
        color = "orange"
    elif misery_score > 40:
        level = "MODERATE"
        color = "yellow"
    else:
        level = "LOW"
        color = "green"
    
    return {
        "food_inflation": food_inflation,
        "rent_increase": rent_increase,
        "youth_unemployment": youth_unemployment,
        "misery_score": round(misery_score, 1),
        "level": level,
        "color": color
    }

def calculate_brain_drain(tr_salary: float, tr_rent: float,
                          de_salary: float, de_rent: float) -> dict:
    """
    Brain Drain Index - Is emigration economically rational?
    """
    tr_ratio = tr_salary / tr_rent
    de_ratio = de_salary / de_rent
    bdi = tr_ratio / de_ratio
    
    if bdi < 0.4:
        decision = "STRONG EMIGRATION INCENTIVE"
    elif bdi < 0.6:
        decision = "MODERATE INCENTIVE TO LEAVE"
    elif bdi < 0.8:
        decision = "SLIGHT INCENTIVE"
    else:
        decision = "STAYING IS RATIONAL"
    
    return {
        "turkey_salary_to_rent": round(tr_ratio, 2),
        "germany_salary_to_rent": round(de_ratio, 2),
        "bdi_score": round(bdi, 3),
        "decision": decision
    }

# ══════════════════════════════════════════════════════════════════════════════
# TEST
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("MONARCH CASTLE - INDEX DEFINITIONS")
    print("=" * 60)
    print(f"\nTotal Indexes Defined: {len(ALL_INDEXES)}")
    
    print("\n--- BY CATEGORY ---")
    for cat in IndexCategory:
        count = sum(1 for idx in ALL_INDEXES.values() if idx["category"] == cat)
        print(f"  {cat.value}: {count}")
    
    print("\n--- SAMPLE CALCULATIONS ---")
    
    # iPhone Parity Index
    ipi = calculate_ipi(
        iphone_usd_price=1199,
        current_fx=36.5,
        future_fx_6m=43.0,
        monthly_salary=50000,
        expected_raise_pct=25
    )
    print(f"\niPhone Parity Index:")
    print(f"  Current Price: {ipi['current_price_try']:,.0f} TRY")
    print(f"  Decision: {ipi['decision']}")
    
    # Commercial Hoarding Index
    chi = calculate_chi("electronics", 45.0, 48.0)
    print(f"\nCommercial Hoarding Index (Electronics):")
    print(f"  CHI Score: {chi['chi_score']}")
    print(f"  Decision: {chi['decision']}")
    
    # Misery Radar
    mr = calculate_misery_radar(35.0, 45.0, 18.0)
    print(f"\nMisery Radar:")
    print(f"  Score: {mr['misery_score']} ({mr['level']})")
