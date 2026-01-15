# ══════════════════════════════════════════════════════════════════════════════
# MONARCH CASTLE TECHNOLOGIES - TURKISH ELECTION PREDICTION MODEL
# ══════════════════════════════════════════════════════════════════════════════
# A "Regime-Aware" election model with Turkish-specific political logic gates.
# Backtest: 2002-2023 | Forecast: 2028
# ══════════════════════════════════════════════════════════════════════════════

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# HISTORICAL ELECTION DATA
# ══════════════════════════════════════════════════════════════════════════════

ELECTION_RESULTS = {
    # General Elections (Parliamentary until 2018, Presidential after)
    2002: {"akp": 34.3, "chp": 19.4, "system": "parliamentary", "turnout": 79.1},
    2007: {"akp": 46.6, "chp": 20.9, "system": "parliamentary", "turnout": 84.3},
    2011: {"akp": 49.8, "chp": 26.0, "system": "parliamentary", "turnout": 83.2},
    2015: {"akp": 40.9, "chp": 25.0, "system": "parliamentary", "turnout": 83.9},  # June
    2018: {"akp": 42.6, "chp": 22.6, "system": "presidential", "turnout": 86.2, 
           "alliance": {"cumhur": 52.6, "millet": 33.9}},
    2023: {"akp": 35.6, "chp": 25.3, "system": "presidential", "turnout": 87.0,
           "alliance": {"cumhur": 49.5, "millet": 35.0}},
}

# Economic data for each election year (simplified)
ECONOMIC_CONTEXT = {
    2002: {"inflation": 29.7, "gdp_growth": 6.2, "unemployment": 10.3, "usd_try": 1.6, "stability": -1.2},
    2007: {"inflation": 8.4, "gdp_growth": 4.7, "unemployment": 9.9, "usd_try": 1.3, "stability": -1.5},
    2011: {"inflation": 10.4, "gdp_growth": 8.8, "unemployment": 9.8, "usd_try": 1.7, "stability": -1.1},
    2015: {"inflation": 7.7, "gdp_growth": 6.1, "unemployment": 10.3, "usd_try": 2.7, "stability": -2.1},
    2018: {"inflation": 16.3, "gdp_growth": 2.8, "unemployment": 11.0, "usd_try": 4.8, "stability": -1.8},
    2023: {"inflation": 44.4, "gdp_growth": 4.5, "unemployment": 10.0, "usd_try": 23.5, "stability": -0.9},
}

# ══════════════════════════════════════════════════════════════════════════════
# TURKISH POLITICAL CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

class TurkishPoliticalRules:
    """
    Hardcoded political rules specific to Turkish elections.
    These override pure economic models because Turkish politics has unique dynamics.
    """
    
    # IDENTITY FLOOR: Minimum vote share regardless of economics
    INCUMBENT_FLOOR = 35.0  # AKP has never dropped below ~35% since 2002
    OPPOSITION_FLOOR = 25.0  # CHP's base is ~25%
    
    # CHARISMA PREMIUM: Iconic leaders boost votes
    CHARISMA_BONUS = {
        "erdogan": 8.0,      # Erdoğan's personal premium
        "imamoglu": 5.0,     # İmamoğlu's potential premium
        "standard": 0.0
    }
    
    # FATIGUE FACTOR: Years in power penalty
    FATIGUE_THRESHOLD = 10  # Penalty starts after 10 years
    FATIGUE_PENALTY_PER_YEAR = 0.5  # -0.5% per year after threshold
    
    # REGIME SWITCH: 2018 changed the game
    PRESIDENTIAL_SYSTEM_YEAR = 2018
    
    # SECURITY RALLY: Terror/instability causes rally around flag
    STABILITY_THRESHOLD = -1.5  # World Bank PV.EST
    SECURITY_RALLY_BONUS = 4.0  # +4% if stability drops below threshold
    
    # FISCAL POPULISM: Pre-election spending sprees
    CREDIT_VELOCITY_THRESHOLD = 40.0  # 40% credit growth = populism
    POPULISM_BONUS = 2.0  # +2% from artificial wealth effect
    
    # ECONOMIC SENSITIVITY
    INFLATION_PENALTY_THRESHOLD = 20.0  # Penalty starts above 20%
    INFLATION_PENALTY_PER_10PCT = 2.0  # -2% for every 10% above threshold
    GDP_BUFFER_PER_PCT = 0.5  # +0.5% per 1% GDP growth
    
    # ALLIANCE SYSTEM (Post-2018)
    ALLIANCE_PARTNERS = {
        "cumhur": ["akp", "mhp", "bbp", "yeniden_refah"],  # People's Alliance
        "millet": ["chp", "iyi", "saadet", "gelecek", "deva"],  # Nation Alliance
    }


# ══════════════════════════════════════════════════════════════════════════════
# ELECTION MODEL
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ElectionScenario:
    """Input parameters for prediction"""
    year: int
    inflation: float
    gdp_growth: float
    unemployment: float
    usd_try: float
    stability_index: float
    years_in_power: int
    candidate_type: str = "erdogan"  # erdogan, imamoglu, standard
    system_type: str = "presidential"  # parliamentary, presidential
    credit_velocity: float = 20.0
    is_terror_period: bool = False
    opposition_unified: bool = True


class TurkishElectionPredictor:
    """
    Production-ready election prediction model with Turkish-specific logic gates.
    """
    
    def __init__(self):
        self.rules = TurkishPoliticalRules()
        self.predictions_history = []
    
    def _economic_base_prediction(self, scenario: ElectionScenario) -> float:
        """
        Calculate base economic prediction.
        Standard economic voting theory: People punish incumbents for inflation,
        reward for growth.
        """
        base = 45.0  # Historical average
        
        # Inflation penalty
        if scenario.inflation > self.rules.INFLATION_PENALTY_THRESHOLD:
            excess = scenario.inflation - self.rules.INFLATION_PENALTY_THRESHOLD
            penalty = (excess / 10) * self.rules.INFLATION_PENALTY_PER_10PCT
            base -= penalty
        
        # GDP buffer
        base += scenario.gdp_growth * self.rules.GDP_BUFFER_PER_PCT
        
        # Unemployment penalty
        if scenario.unemployment > 10:
            base -= (scenario.unemployment - 10) * 0.3
        
        return base
    
    def _apply_charisma_premium(self, base: float, candidate: str) -> float:
        """Add personal vote premium for iconic leaders."""
        bonus = self.rules.CHARISMA_BONUS.get(candidate, 0)
        return base + bonus
    
    def _apply_fatigue_factor(self, base: float, years_in_power: int) -> float:
        """Deduct for voter fatigue after 10+ years."""
        if years_in_power > self.rules.FATIGUE_THRESHOLD:
            excess_years = years_in_power - self.rules.FATIGUE_THRESHOLD
            penalty = excess_years * self.rules.FATIGUE_PENALTY_PER_YEAR
            return base - penalty
        return base
    
    def _apply_security_rally(self, base: float, stability: float) -> float:
        """Add rally-around-flag bonus during instability."""
        if stability < self.rules.STABILITY_THRESHOLD:
            return base + self.rules.SECURITY_RALLY_BONUS
        return base
    
    def _apply_populism_boost(self, base: float, credit_velocity: float) -> float:
        """Add bonus for pre-election spending sprees."""
        if credit_velocity > self.rules.CREDIT_VELOCITY_THRESHOLD:
            return base + self.rules.POPULISM_BONUS
        return base
    
    def _apply_identity_floor(self, prediction: float) -> float:
        """
        CRITICAL: The Identity Floor.
        Turkish voters have strong identity-based voting. The incumbent
        party has a sociological floor of ~35% that almost never breaks.
        """
        return max(prediction, self.rules.INCUMBENT_FLOOR)
    
    def predict(self, scenario: ElectionScenario) -> Dict:
        """
        Full prediction pipeline with all Turkish logic gates.
        """
        # Step 1: Raw economic prediction
        raw_economic = self._economic_base_prediction(scenario)
        
        # Step 2: Apply charisma
        with_charisma = self._apply_charisma_premium(raw_economic, scenario.candidate_type)
        
        # Step 3: Apply fatigue
        with_fatigue = self._apply_fatigue_factor(with_charisma, scenario.years_in_power)
        
        # Step 4: Apply security rally
        with_security = self._apply_security_rally(with_fatigue, scenario.stability_index)
        
        # Step 5: Apply populism boost
        with_populism = self._apply_populism_boost(with_security, scenario.credit_velocity)
        
        # Step 6: Apply identity floor (THE KEY ADJUSTMENT)
        final_prediction = self._apply_identity_floor(with_populism)
        
        # Calculate how much the identity floor "saved" the prediction
        floor_rescue = final_prediction - with_populism if with_populism < self.rules.INCUMBENT_FLOOR else 0
        
        # Predict winner
        if scenario.system_type == "presidential":
            wins = final_prediction >= 50.0
        else:
            wins = final_prediction >= 40.0  # Parliamentary majority threshold
        
        result = {
            "year": scenario.year,
            "raw_economic_prediction": round(raw_economic, 2),
            "adjustments": {
                "charisma_bonus": round(with_charisma - raw_economic, 2),
                "fatigue_penalty": round(with_fatigue - with_charisma, 2),
                "security_rally": round(with_security - with_fatigue, 2),
                "populism_boost": round(with_populism - with_security, 2),
                "identity_floor_rescue": round(floor_rescue, 2),
            },
            "final_prediction": round(final_prediction, 2),
            "prediction_outcome": "WIN" if wins else "LOSE/RUNOFF",
            "confidence_interval": (
                round(final_prediction - 3.0, 2),
                round(final_prediction + 3.0, 2)
            )
        }
        
        self.predictions_history.append(result)
        return result
    
    def run_monte_carlo(self, base_scenario: ElectionScenario, 
                        n_simulations: int = 10000) -> Dict:
        """
        Monte Carlo simulation for 2028 prediction with uncertainty.
        Introduces stochastic shocks.
        """
        results = []
        
        for _ in range(n_simulations):
            # Create scenario with random variations
            sim_scenario = ElectionScenario(
                year=base_scenario.year,
                inflation=np.random.normal(base_scenario.inflation, 5.0),
                gdp_growth=np.random.normal(base_scenario.gdp_growth, 1.0),
                unemployment=np.random.normal(base_scenario.unemployment, 1.0),
                usd_try=base_scenario.usd_try,
                stability_index=np.random.normal(base_scenario.stability_index, 0.3),
                years_in_power=base_scenario.years_in_power,
                candidate_type=base_scenario.candidate_type,
                system_type=base_scenario.system_type,
                credit_velocity=np.random.normal(base_scenario.credit_velocity, 10),
            )
            
            prediction = self.predict(sim_scenario)
            vote = prediction["final_prediction"]
            
            # Black Swan Events
            # Earthquake shock (5% probability, -2% impact)
            if np.random.random() < 0.05:
                vote -= 2.0
            
            # Geopolitical rally (10% probability, +2% impact)
            if np.random.random() < 0.10:
                vote += 2.0
            
            results.append(vote)
        
        results = np.array(results)
        
        return {
            "n_simulations": n_simulations,
            "mean_prediction": round(np.mean(results), 2),
            "std_deviation": round(np.std(results), 2),
            "percentile_25": round(np.percentile(results, 25), 2),
            "percentile_50": round(np.percentile(results, 50), 2),
            "percentile_75": round(np.percentile(results, 75), 2),
            "probability_over_50": round((results >= 50).mean() * 100, 1),
            "probability_over_45": round((results >= 45).mean() * 100, 1),
            "worst_case": round(np.min(results), 2),
            "best_case": round(np.max(results), 2),
        }
    
    def backtest(self) -> List[Dict]:
        """
        Backtest model against historical elections.
        """
        backtest_results = []
        
        for year, actual in ELECTION_RESULTS.items():
            econ = ECONOMIC_CONTEXT.get(year, {})
            
            scenario = ElectionScenario(
                year=year,
                inflation=econ.get("inflation", 20),
                gdp_growth=econ.get("gdp_growth", 3),
                unemployment=econ.get("unemployment", 10),
                usd_try=econ.get("usd_try", 5),
                stability_index=econ.get("stability", -1),
                years_in_power=year - 2002,
                candidate_type="erdogan" if year >= 2014 else "standard",
                system_type=actual.get("system", "parliamentary"),
                credit_velocity=25 if year in [2018, 2023] else 15,
            )
            
            prediction = self.predict(scenario)
            
            # Compare with actual alliance vote in presidential system
            if year >= 2018:
                actual_vote = actual.get("alliance", {}).get("cumhur", actual["akp"])
            else:
                actual_vote = actual["akp"]
            
            error = prediction["final_prediction"] - actual_vote
            
            backtest_results.append({
                "year": year,
                "actual": actual_vote,
                "predicted": prediction["final_prediction"],
                "error": round(error, 2),
                "abs_error": round(abs(error), 2),
            })
        
        # Calculate overall accuracy
        mean_abs_error = np.mean([r["abs_error"] for r in backtest_results])
        
        return {
            "results": backtest_results,
            "mean_absolute_error": round(mean_abs_error, 2),
            "accuracy_assessment": "GOOD" if mean_abs_error < 4 else "NEEDS CALIBRATION"
        }


# ══════════════════════════════════════════════════════════════════════════════
# PREDICT 2028
# ══════════════════════════════════════════════════════════════════════════════

def predict_2028():
    """
    Main prediction for 2028 Turkish Presidential Election.
    """
    predictor = TurkishElectionPredictor()
    
    # 2028 Scenario (based on BBVA forecasts + assumptions)
    scenario_2028 = ElectionScenario(
        year=2028,
        inflation=18.0,  # Projected to decline from 2026
        gdp_growth=3.5,
        unemployment=9.5,
        usd_try=65.0,    # Projected
        stability_index=-0.6,
        years_in_power=26,  # 2002-2028
        candidate_type="erdogan",  # Assuming Erdoğan runs
        system_type="presidential",
        credit_velocity=35.0,  # Moderate pre-election boost
    )
    
    # Single prediction
    prediction = predictor.predict(scenario_2028)
    
    # Monte Carlo
    monte_carlo = predictor.run_monte_carlo(scenario_2028, n_simulations=10000)
    
    # Backtest
    backtest = predictor.backtest()
    
    return {
        "scenario": {
            "year": 2028,
            "inflation": scenario_2028.inflation,
            "gdp_growth": scenario_2028.gdp_growth,
            "usd_try": scenario_2028.usd_try,
            "years_in_power": scenario_2028.years_in_power,
        },
        "point_prediction": prediction,
        "monte_carlo_simulation": monte_carlo,
        "backtest": backtest,
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("MONARCH CASTLE - TURKISH ELECTION PREDICTION MODEL")
    print("=" * 70)
    
    results = predict_2028()
    
    print("\n--- 2028 SCENARIO ---")
    for k, v in results["scenario"].items():
        print(f"  {k}: {v}")
    
    print("\n--- POINT PREDICTION ---")
    pred = results["point_prediction"]
    print(f"  Raw Economic Model: {pred['raw_economic_prediction']}%")
    print(f"  Adjustments:")
    for adj, val in pred["adjustments"].items():
        if val != 0:
            print(f"    {adj}: {val:+.1f}%")
    print(f"  FINAL PREDICTION: {pred['final_prediction']}%")
    print(f"  Outcome: {pred['prediction_outcome']}")
    
    print("\n--- MONTE CARLO (10,000 simulations) ---")
    mc = results["monte_carlo_simulation"]
    print(f"  Mean: {mc['mean_prediction']}% ± {mc['std_deviation']}%")
    print(f"  Range: {mc['worst_case']}% - {mc['best_case']}%")
    print(f"  P(>50%): {mc['probability_over_50']}%")
    print(f"  P(>45%): {mc['probability_over_45']}%")
    
    print("\n--- BACKTEST (2002-2023) ---")
    bt = results["backtest"]
    print(f"  Mean Absolute Error: {bt['mean_absolute_error']}%")
    print(f"  Assessment: {bt['accuracy_assessment']}")
    
    # Save results
    output_path = Path(__file__).parent / "data" / "election_forecast_2028.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[OK] Results saved to {output_path}")
