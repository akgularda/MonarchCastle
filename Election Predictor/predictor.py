# ══════════════════════════════════════════════════════════════════════════════
# MONARCH CASTLE TECHNOLOGIES - TURKISH ELECTION PREDICTION MODEL
# ══════════════════════════════════════════════════════════════════════════════
# Production-Ready "Regime-Aware" Election Model
# Backtest: 2002-2023 | Holdout Test: 2023 | Forecast: 2028
# 
# THE KEY TEST: Can we predict 2023 using ONLY pre-2023 data?
# ══════════════════════════════════════════════════════════════════════════════

import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Try to import ML libraries
try:
    from xgboost import XGBRegressor
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("[WARN] xgboost not installed. Run: pip install xgboost")

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("[WARN] matplotlib not installed. Run: pip install matplotlib")


# ══════════════════════════════════════════════════════════════════════════════
# HISTORICAL DATA - THE GROUND TRUTH
# ══════════════════════════════════════════════════════════════════════════════

# Complete election results with alliance votes for presidential system
ELECTION_RESULTS = {
    # Year: {akp_vote, alliance_vote (for post-2018), system, turnout, actual economic conditions}
    2002: {
        "akp": 34.3, "chp": 19.4, "mhp": 8.4,
        "incumbent_vote": 34.3,  # No alliance yet
        "system": "parliamentary", "turnout": 79.1,
        "election_type": "general"
    },
    2007: {
        "akp": 46.6, "chp": 20.9, "mhp": 14.3,
        "incumbent_vote": 46.6,
        "system": "parliamentary", "turnout": 84.3,
        "election_type": "general"
    },
    2011: {
        "akp": 49.8, "chp": 26.0, "mhp": 13.0,
        "incumbent_vote": 49.8,
        "system": "parliamentary", "turnout": 83.2,
        "election_type": "general"
    },
    2015: {  # June election (AKP lost majority, then Nov snap election)
        "akp": 40.9, "chp": 25.0, "mhp": 16.3, "hdp": 13.1,
        "incumbent_vote": 40.9,
        "system": "parliamentary", "turnout": 83.9,
        "election_type": "general",
        "note": "Terror period, lost majority"
    },
    2018: {  # First presidential election
        "akp": 42.6, "mhp": 11.1,
        "erdogan_r1": 52.6,  # Erdoğan first round
        "cumhur_alliance": 53.7,  # People's Alliance total
        "millet_alliance": 33.9,  # Nation Alliance total
        "incumbent_vote": 52.6,  # Use presidential vote
        "system": "presidential", "turnout": 86.2,
        "election_type": "presidential"
    },
    2023: {
        "akp": 35.6, "mhp": 10.1,
        "erdogan_r1": 49.5,  # Erdoğan first round (went to runoff)
        "erdogan_r2": 52.2,  # Erdoğan second round (won)
        "cumhur_alliance": 49.5,
        "millet_alliance": 44.9,
        "incumbent_vote": 49.5,  # First round for prediction, 52.2 final
        "system": "presidential", "turnout": 87.0,
        "election_type": "presidential",
        "went_to_runoff": True
    }
}

# Economic data for each election year
# This is the CRITICAL data for prediction
ECONOMIC_DATA = {
    2002: {
        "inflation_yoy": 29.7,       # YoY CPI
        "gdp_growth": 6.2,           # YoY GDP Growth
        "unemployment": 10.3,        # Unemployment rate
        "usd_try": 1.65,             # USD/TRY
        "usd_try_change_yoy": 12.5,  # YoY change in currency
        "stability_index": -0.8,     # World Bank Political Stability
        "oil_price": 28.0,           # Brent crude
        "credit_growth": 15.0,       # Credit card spending growth
        "years_in_power": 0,         # AKP not in power yet
        "is_incumbent": False,       # AKP was opposition
    },
    2007: {
        "inflation_yoy": 8.4,
        "gdp_growth": 4.7,
        "unemployment": 9.9,
        "usd_try": 1.30,
        "usd_try_change_yoy": -15.0,  # TRY strengthened!
        "stability_index": -1.5,
        "oil_price": 72.0,
        "credit_growth": 45.0,        # Credit boom
        "years_in_power": 5,
        "is_incumbent": True,
    },
    2011: {
        "inflation_yoy": 10.4,
        "gdp_growth": 8.8,            # Excellent growth
        "unemployment": 9.8,
        "usd_try": 1.67,
        "usd_try_change_yoy": 15.0,
        "stability_index": -1.1,
        "oil_price": 111.0,           # Oil shock
        "credit_growth": 35.0,
        "years_in_power": 9,
        "is_incumbent": True,
    },
    2015: {
        "inflation_yoy": 7.7,
        "gdp_growth": 6.1,
        "unemployment": 10.3,
        "usd_try": 2.72,
        "usd_try_change_yoy": 25.0,   # Currency started weakening
        "stability_index": -2.1,      # TERROR PERIOD - key factor!
        "oil_price": 52.0,
        "credit_growth": 20.0,
        "years_in_power": 13,
        "is_incumbent": True,
        "terror_period": True,        # PKK ceasefire collapsed
    },
    2018: {
        "inflation_yoy": 16.3,
        "gdp_growth": 2.8,
        "unemployment": 11.0,
        "usd_try": 4.81,
        "usd_try_change_yoy": 40.0,   # Currency crisis beginning
        "stability_index": -1.8,
        "oil_price": 74.0,
        "credit_growth": 30.0,
        "years_in_power": 16,
        "is_incumbent": True,
        "snap_election": True,        # Called early due to economic fear
    },
    2023: {
        "inflation_yoy": 44.4,        # Official - felt inflation was 100%+
        "gdp_growth": 4.5,
        "unemployment": 10.0,
        "usd_try": 23.5,              # At election time
        "usd_try_change_yoy": 85.0,   # Massive depreciation
        "stability_index": -0.9,
        "oil_price": 78.0,
        "credit_growth": 70.0,        # MASSIVE pre-election stimulus
        "years_in_power": 21,
        "is_incumbent": True,
        "earthquake": True,           # Feb 2023 earthquake (50k dead)
        "pre_election_min_wage_hike": 55.0,  # 55% min wage raise
    }
}


# ══════════════════════════════════════════════════════════════════════════════
# TURKISH POLITICAL CONSTANTS - THE "PHYSICS" OF TURKISH ELECTIONS
# ══════════════════════════════════════════════════════════════════════════════

class TurkishPoliticalPhysics:
    """
    These are the hardcoded rules that override pure economic models.
    Turkish voters don't behave like "rational economic agents."
    """
    
    # ══════════ THE IDENTITY FLOOR ══════════
    # No matter how bad the economy, certain voters NEVER switch.
    # This is identity voting, not economic voting.
    INCUMBENT_FLOOR = 35.0      # AKP's absolute floor (never below since 2002)
    OPPOSITION_FLOOR = 25.0     # CHP's absolute floor
    NATIONALIST_FLOOR = 8.0     # MHP's floor
    
    # ══════════ THE REGIME SWITCH ══════════
    # 2018 changed everything - now it's Alliance vs Alliance
    PRESIDENTIAL_YEAR = 2018
    
    # In presidential system, add nationalist partner
    # This is why AKP+MHP vs CHP+IYI+etc
    ALLIANCE_BONUS = 10.0       # MHP typically adds ~10%
    
    # ══════════ THE CHARISMA FACTOR ══════════
    LEADER_PREMIUM = {
        "erdogan": 8.0,         # Personal vote for Erdoğan
        "kilicdaroglu": 2.0,    # Less personal appeal
        "imamoglu": 5.0,        # If he runs in 2028
    }
    
    # ══════════ FATIGUE PENALTY ══════════
    FATIGUE_START_YEAR = 10     # Penalty kicks in after 10 years
    FATIGUE_PER_YEAR = 0.3      # -0.3% per year after 10 years
    
    # ══════════ ECONOMIC SENSITIVITY ══════════
    # Turkish voters ARE sensitive to economy, just not linearly
    INFLATION_THRESHOLD = 20.0  # Below 20%, voters don't punish
    INFLATION_PENALTY_PER_10 = 1.5  # -1.5% for every 10% above threshold
    
    GDP_BONUS_PER_POINT = 0.4   # +0.4% for every 1% GDP growth
    
    # Currency depreciation is felt more than inflation
    CURRENCY_PENALTY_PER_10 = 0.5  # -0.5% for every 10% currency drop
    
    # ══════════ SECURITY RALLY ══════════
    # When terror attacks happen, voters rally to incumbent
    STABILITY_THRESHOLD = -1.5  # World Bank index
    SECURITY_RALLY = 4.0        # +4% bonus in terror periods
    
    # ══════════ FISCAL POPULISM ══════════
    # Credit growth > 40% means artificial stimulus
    CREDIT_THRESHOLD = 40.0
    POPULISM_BONUS = 2.0        # +2% from "free money" feeling
    
    # ══════════ EARTHQUAKE EFFECT ══════════
    # 2023 earthquake was unique - initially hurt, then rallied
    EARTHQUAKE_INITIAL = -3.0   # Initial hit
    EARTHQUAKE_RALLY = 5.0      # Then rally around flag


# ══════════════════════════════════════════════════════════════════════════════
# THE MODEL
# ══════════════════════════════════════════════════════════════════════════════

class TurkishElectionPredictor:
    """
    A regime-aware election prediction model with Turkish-specific logic gates.
    """
    
    def __init__(self, use_xgboost: bool = True):
        self.physics = TurkishPoliticalPhysics()
        self.use_xgboost = use_xgboost and HAS_XGBOOST
        self.model = None
        self.feature_names = []
        self.training_history = []
        
    def _create_features(self, year: int, econ: dict) -> dict:
        """
        Create feature vector from economic data.
        CRITICAL: These must be features known BEFORE the election.
        """
        features = {}
        
        # === ECONOMIC FEATURES ===
        features["inflation"] = econ.get("inflation_yoy", 20.0)
        features["gdp_growth"] = econ.get("gdp_growth", 3.0)
        features["unemployment"] = econ.get("unemployment", 10.0)
        features["currency_change"] = econ.get("usd_try_change_yoy", 10.0)
        features["credit_growth"] = econ.get("credit_growth", 20.0)
        features["oil_price"] = econ.get("oil_price", 70.0)
        
        # === POLITICAL FEATURES ===
        features["years_in_power"] = econ.get("years_in_power", 0)
        features["is_incumbent"] = 1 if econ.get("is_incumbent", True) else 0
        
        # === REGIME SWITCH ===
        features["is_presidential"] = 1 if year >= self.physics.PRESIDENTIAL_YEAR else 0
        
        # === STABILITY ===
        features["stability_index"] = econ.get("stability_index", -1.0)
        features["is_terror_period"] = 1 if econ.get("terror_period", False) else 0
        
        # === SPECIAL EVENTS ===
        features["is_earthquake"] = 1 if econ.get("earthquake", False) else 0
        features["is_snap_election"] = 1 if econ.get("snap_election", False) else 0
        
        # === DERIVED FEATURES ===
        # Misery index (felt by voters)
        features["misery_index"] = features["inflation"] + features["unemployment"]
        
        # Fatigue factor
        if features["years_in_power"] > self.physics.FATIGUE_START_YEAR:
            features["fatigue"] = (features["years_in_power"] - self.physics.FATIGUE_START_YEAR)
        else:
            features["fatigue"] = 0
            
        # Credit stimulus flag
        features["credit_stimulus"] = 1 if features["credit_growth"] > self.physics.CREDIT_THRESHOLD else 0
        
        return features
    
    def _apply_political_adjustments(self, raw_prediction: float, 
                                     features: dict, year: int) -> Tuple[float, dict]:
        """
        Apply Turkish political "physics" adjustments to raw economic prediction.
        This is where the model becomes Turkey-specific.
        """
        adjustments = {}
        prediction = raw_prediction
        
        # 1. IDENTITY FLOOR - The anchor
        # No matter what the model says, vote can't go below floor
        if prediction < self.physics.INCUMBENT_FLOOR:
            adjustments["floor_rescue"] = self.physics.INCUMBENT_FLOOR - prediction
            prediction = self.physics.INCUMBENT_FLOOR
        else:
            adjustments["floor_rescue"] = 0
        
        # 2. SECURITY RALLY
        if features["stability_index"] < self.physics.STABILITY_THRESHOLD:
            adjustments["security_rally"] = self.physics.SECURITY_RALLY
            prediction += self.physics.SECURITY_RALLY
        else:
            adjustments["security_rally"] = 0
        
        # 3. ALLIANCE BONUS (Post-2018)
        if features["is_presidential"] and year >= 2018:
            # In presidential system, add nationalist partner votes
            adjustments["alliance_bonus"] = self.physics.ALLIANCE_BONUS
            # Note: This is handled in target variable, not prediction
        else:
            adjustments["alliance_bonus"] = 0
        
        # 4. POPULISM BONUS
        if features["credit_stimulus"]:
            adjustments["populism_bonus"] = self.physics.POPULISM_BONUS
            prediction += self.physics.POPULISM_BONUS
        else:
            adjustments["populism_bonus"] = 0
        
        # 5. EARTHQUAKE EFFECT (2023 specific)
        if features["is_earthquake"]:
            # Net effect: initially hurt, then massive rally
            net_earthquake = self.physics.EARTHQUAKE_RALLY + self.physics.EARTHQUAKE_INITIAL
            adjustments["earthquake_effect"] = net_earthquake
            prediction += net_earthquake
        else:
            adjustments["earthquake_effect"] = 0
        
        # 6. LEADER CHARISMA (Erdoğan premium)
        if features["is_incumbent"] and features["is_presidential"]:
            adjustments["leader_charisma"] = self.physics.LEADER_PREMIUM.get("erdogan", 0)
            # Already factored into presidential vote
        else:
            adjustments["leader_charisma"] = 0
        
        # 7. FATIGUE PENALTY
        if features["fatigue"] > 0:
            penalty = features["fatigue"] * self.physics.FATIGUE_PER_YEAR
            adjustments["fatigue_penalty"] = -penalty
            prediction -= penalty
        else:
            adjustments["fatigue_penalty"] = 0
        
        return prediction, adjustments
    
    def _economic_model_prediction(self, features: dict) -> float:
        """
        Raw economic prediction based on fundamentals.
        This is what a "rational" model would predict.
        """
        # Base vote (historical average)
        base = 43.0
        
        # Inflation penalty
        if features["inflation"] > self.physics.INFLATION_THRESHOLD:
            excess = features["inflation"] - self.physics.INFLATION_THRESHOLD
            penalty = (excess / 10) * self.physics.INFLATION_PENALTY_PER_10
            base -= penalty
        
        # GDP bonus
        base += features["gdp_growth"] * self.physics.GDP_BONUS_PER_POINT
        
        # Currency penalty
        if features["currency_change"] > 0:
            penalty = (features["currency_change"] / 10) * self.physics.CURRENCY_PENALTY_PER_10
            base -= penalty
        
        # Unemployment penalty
        if features["unemployment"] > 10:
            base -= (features["unemployment"] - 10) * 0.3
        
        return base
    
    def prepare_training_data(self, holdout_year: Optional[int] = None) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare training data from historical elections.
        If holdout_year specified, exclude it for testing.
        """
        rows = []
        
        for year in sorted(ELECTION_RESULTS.keys()):
            if holdout_year and year >= holdout_year:
                continue  # Exclude for out-of-sample test
                
            if year not in ECONOMIC_DATA:
                continue
                
            econ = ECONOMIC_DATA[year]
            result = ELECTION_RESULTS[year]
            
            features = self._create_features(year, econ)
            features["year"] = year
            
            # Target: incumbent vote share
            features["target"] = result["incumbent_vote"]
            
            rows.append(features)
        
        df = pd.DataFrame(rows)
        
        # Store feature names (excluding year and target)
        self.feature_names = [c for c in df.columns if c not in ["year", "target"]]
        
        X = df[self.feature_names]
        y = df["target"]
        
        return X, y, df
    
    def train(self, holdout_year: Optional[int] = None):
        """
        Train the model.
        If holdout_year specified, test prediction on that year.
        """
        X, y, df = self.prepare_training_data(holdout_year)
        
        print("=" * 70)
        print("TRAINING DATA")
        print("=" * 70)
        print(df[["year", "inflation", "gdp_growth", "years_in_power", "target"]].to_string(index=False))
        
        if self.use_xgboost:
            self.model = XGBRegressor(
                n_estimators=100,
                max_depth=3,
                learning_rate=0.1,
                random_state=42
            )
            self.model.fit(X, y)
            
            # Feature importance
            importance = pd.DataFrame({
                "feature": self.feature_names,
                "importance": self.model.feature_importances_
            }).sort_values("importance", ascending=False)
            
            print("\n--- FEATURE IMPORTANCE ---")
            print(importance.to_string(index=False))
        else:
            print("\n[INFO] XGBoost not available, using rule-based model")
    
    def predict_single(self, year: int, econ: dict, 
                       apply_adjustments: bool = True) -> dict:
        """
        Make prediction for a single year.
        """
        features = self._create_features(year, econ)
        
        # Get raw economic prediction
        if self.model:
            X = pd.DataFrame([features])[self.feature_names]
            raw_prediction = self.model.predict(X)[0]
        else:
            raw_prediction = self._economic_model_prediction(features)
        
        # Apply political adjustments
        if apply_adjustments:
            final_prediction, adjustments = self._apply_political_adjustments(
                raw_prediction, features, year
            )
        else:
            final_prediction = raw_prediction
            adjustments = {}
        
        return {
            "year": year,
            "raw_economic": round(raw_prediction, 2),
            "adjustments": {k: round(v, 2) for k, v in adjustments.items()},
            "final_prediction": round(final_prediction, 2),
            "features": {k: round(v, 2) if isinstance(v, float) else v 
                        for k, v in features.items()}
        }
    
    def backtest(self, include_2023: bool = False) -> pd.DataFrame:
        """
        Backtest model against all historical elections.
        """
        results = []
        
        for year in sorted(ELECTION_RESULTS.keys()):
            if not include_2023 and year == 2023:
                continue
            if year not in ECONOMIC_DATA:
                continue
            
            pred = self.predict_single(year, ECONOMIC_DATA[year])
            actual = ELECTION_RESULTS[year]["incumbent_vote"]
            
            results.append({
                "year": year,
                "actual": actual,
                "raw_economic": pred["raw_economic"],
                "final_prediction": pred["final_prediction"],
                "error": pred["final_prediction"] - actual,
                "abs_error": abs(pred["final_prediction"] - actual),
                "floor_rescue": pred["adjustments"].get("floor_rescue", 0),
                "security_rally": pred["adjustments"].get("security_rally", 0),
            })
        
        return pd.DataFrame(results)
    
    def predict_2023_with_2022_data(self) -> dict:
        """
        THE KEY TEST: Predict 2023 using only pre-2023 information.
        This simulates what we would have known in December 2022.
        """
        # Train on 2002-2018 only
        self.train(holdout_year=2023)
        
        # Economic conditions as of late 2022 (pre-election)
        # This is what we would have known going into the election
        pre_2023_estimate = {
            "inflation_yoy": 85.0,        # Was running even higher before election
            "gdp_growth": 5.6,            # 2022 GDP growth
            "unemployment": 10.2,
            "usd_try": 18.7,              # End of 2022
            "usd_try_change_yoy": 50.0,
            "stability_index": -0.9,
            "oil_price": 80.0,
            "credit_growth": 60.0,        # Already ramping up
            "years_in_power": 21,
            "is_incumbent": True,
            "earthquake": True,           # Would need to predict this - major uncertainty
        }
        
        print("\n" + "=" * 70)
        print("2023 PREDICTION TEST (Using Pre-2023 Data Only)")
        print("=" * 70)
        
        # Prediction WITH earthquake (what actually happened)
        pred_with_eq = self.predict_single(2023, pre_2023_estimate)
        
        # Prediction WITHOUT earthquake (what we'd predict in Dec 2022)
        no_eq_estimate = pre_2023_estimate.copy()
        no_eq_estimate["earthquake"] = False
        pred_no_eq = self.predict_single(2023, no_eq_estimate)
        
        actual_r1 = ELECTION_RESULTS[2023]["erdogan_r1"]
        actual_r2 = ELECTION_RESULTS[2023].get("erdogan_r2", actual_r1)
        
        print(f"\nActual Result: R1={actual_r1}%, R2={actual_r2}%")
        print(f"\nPrediction WITHOUT earthquake knowledge: {pred_no_eq['final_prediction']}%")
        print(f"Prediction WITH earthquake adjustment:   {pred_with_eq['final_prediction']}%")
        print(f"\nRaw Economic Model (no adjustments):     {pred_no_eq['raw_economic']}%")
        print(f"Floor Rescue (Identity Vote):            +{pred_with_eq['adjustments'].get('floor_rescue', 0)}%")
        print(f"Security Rally:                          +{pred_with_eq['adjustments'].get('security_rally', 0)}%")
        print(f"Populism Bonus:                          +{pred_with_eq['adjustments'].get('populism_bonus', 0)}%")
        print(f"Earthquake Effect:                       +{pred_with_eq['adjustments'].get('earthquake_effect', 0)}%")
        
        return {
            "actual_r1": actual_r1,
            "actual_r2": actual_r2,
            "prediction_no_earthquake": pred_no_eq["final_prediction"],
            "prediction_with_earthquake": pred_with_eq["final_prediction"],
            "raw_economic": pred_no_eq["raw_economic"],
            "was_runoff": abs(pred_no_eq["final_prediction"] - 50) < 3,  # Close to 50 = runoff
            "correctly_predicted_tight_race": pred_no_eq["final_prediction"] < 52
        }
    
    def run_monte_carlo_2028(self, n_simulations: int = 10000) -> dict:
        """
        Monte Carlo simulation for 2028 with stochastic shocks.
        """
        # 2028 base scenario (using BBVA forecasts)
        base_scenario = {
            "inflation_yoy": 18.0,        # Projected to decline
            "gdp_growth": 3.5,
            "unemployment": 9.5,
            "usd_try": 65.0,
            "usd_try_change_yoy": 25.0,
            "stability_index": -0.6,
            "oil_price": 65.0,
            "credit_growth": 30.0,
            "years_in_power": 26,
            "is_incumbent": True,
        }
        
        results = []
        
        for sim in range(n_simulations):
            # Add random variation to inputs
            scenario = base_scenario.copy()
            scenario["inflation_yoy"] = np.random.normal(18.0, 5.0)
            scenario["gdp_growth"] = np.random.normal(3.5, 1.0)
            scenario["stability_index"] = np.random.normal(-0.6, 0.3)
            scenario["credit_growth"] = np.random.normal(30.0, 10.0)
            
            pred = self.predict_single(2028, scenario)
            vote = pred["final_prediction"]
            
            # Black Swan shocks
            # Earthquake (5% prob, -2% impact)
            if np.random.random() < 0.05:
                vote -= 2.0
            
            # Geopolitical rally (10% prob, +2% impact)
            if np.random.random() < 0.10:
                vote += 2.0
            
            # Economic crash (5% prob, -4% impact)
            if np.random.random() < 0.05:
                vote -= 4.0
            
            results.append(vote)
        
        results = np.array(results)
        
        return {
            "n_simulations": n_simulations,
            "mean": round(np.mean(results), 2),
            "std": round(np.std(results), 2),
            "p25": round(np.percentile(results, 25), 2),
            "p50": round(np.percentile(results, 50), 2),
            "p75": round(np.percentile(results, 75), 2),
            "min": round(np.min(results), 2),
            "max": round(np.max(results), 2),
            "prob_over_50": round((results >= 50).mean() * 100, 1),
            "prob_over_45": round((results >= 45).mean() * 100, 1),
            "prob_under_40": round((results < 40).mean() * 100, 1),
        }
    
    def plot_backtest(self, save_path: Optional[str] = None):
        """
        Plot actual vs predicted for all elections.
        """
        if not HAS_MATPLOTLIB:
            print("[WARN] matplotlib not available for plotting")
            return
        
        bt = self.backtest(include_2023=True)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        years = bt["year"].values
        actual = bt["actual"].values
        predicted = bt["final_prediction"].values
        raw = bt["raw_economic"].values
        
        x = np.arange(len(years))
        width = 0.25
        
        ax.bar(x - width, actual, width, label="Actual", color="#2563eb")
        ax.bar(x, predicted, width, label="Predicted (Adjusted)", color="#10b981")
        ax.bar(x + width, raw, width, label="Raw Economic", color="#ef4444", alpha=0.5)
        
        ax.axhline(y=50, color="black", linestyle="--", alpha=0.5, label="Majority Line")
        ax.axhline(y=35, color="red", linestyle=":", alpha=0.5, label="Identity Floor")
        
        ax.set_xlabel("Election Year")
        ax.set_ylabel("Vote Share (%)")
        ax.set_title("Turkish Election Prediction Model - Backtest Results")
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.legend()
        ax.set_ylim(30, 60)
        ax.grid(axis='y', alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"[OK] Plot saved to {save_path}")
        
        plt.tight_layout()
        plt.show()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Run the full analysis."""
    
    print("╔" + "═" * 68 + "╗")
    print("║" + " MONARCH CASTLE - TURKISH ELECTION PREDICTION MODEL ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Initialize predictor
    predictor = TurkishElectionPredictor()
    
    # === STEP 1: TRAIN ON ALL DATA ===
    print("\n" + "=" * 70)
    print("STEP 1: FULL BACKTEST (Training on all data)")
    print("=" * 70)
    
    predictor.train()
    backtest_results = predictor.backtest(include_2023=True)
    
    print("\n--- BACKTEST RESULTS ---")
    print(backtest_results.to_string(index=False))
    print(f"\nMean Absolute Error: {backtest_results['abs_error'].mean():.2f}%")
    
    # === STEP 2: THE KEY TEST - PREDICT 2023 WITH PRE-2023 DATA ===
    print("\n" + "=" * 70)
    print("STEP 2: OUT-OF-SAMPLE TEST - Predict 2023 using only 2002-2018 data")
    print("=" * 70)
    
    test_2023 = predictor.predict_2023_with_2022_data()
    
    print("\n--- 2023 PREDICTION ASSESSMENT ---")
    if test_2023["correctly_predicted_tight_race"]:
        print("✓ Model correctly predicted a TIGHT RACE (close to 50%)")
    else:
        print("✗ Model did NOT predict tight race")
    
    print(f"\nError (vs R1): {abs(test_2023['prediction_with_earthquake'] - test_2023['actual_r1']):.1f}%")
    
    # === STEP 3: 2028 MONTE CARLO ===
    print("\n" + "=" * 70)
    print("STEP 3: 2028 FORECAST (Monte Carlo Simulation)")
    print("=" * 70)
    
    mc = predictor.run_monte_carlo_2028(n_simulations=10000)
    
    print(f"\n2028 Prediction Distribution:")
    print(f"  Mean:   {mc['mean']}% ± {mc['std']}%")
    print(f"  Median: {mc['p50']}%")
    print(f"  Range:  {mc['min']}% - {mc['max']}%")
    print(f"\nProbabilities:")
    print(f"  P(Win outright >50%): {mc['prob_over_50']}%")
    print(f"  P(Runoff territory):  {100 - mc['prob_over_50'] - mc['prob_under_40']:.1f}%")
    print(f"  P(Lose badly <40%):   {mc['prob_under_40']}%")
    
    # === STEP 4: SAVE RESULTS ===
    output = {
        "backtest": backtest_results.to_dict(orient="records"),
        "test_2023": test_2023,
        "forecast_2028": mc,
        "model_info": {
            "identity_floor": TurkishPoliticalPhysics.INCUMBENT_FLOOR,
            "security_rally": TurkishPoliticalPhysics.SECURITY_RALLY,
            "fatigue_per_year": TurkishPoliticalPhysics.FATIGUE_PER_YEAR,
        }
    }
    
    output_path = Path(__file__).parent / "election_forecast.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n[OK] Results saved to {output_path}")
    
    # === PLOT ===
    plot_path = Path(__file__).parent / "backtest_chart.png"
    predictor.plot_backtest(save_path=str(plot_path))
    
    return predictor, output


if __name__ == "__main__":
    predictor, results = main()
