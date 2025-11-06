from __future__ import annotations

import json
from typing import Dict, Any

import numpy as np
import pandas as pd


def run_monte_carlo(assumptions: Dict[str, Any], iterations: int = 2000, seed: int | None = None) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    results = []

    rail = assumptions["rail"]
    retail = assumptions["retail"]
    fees = assumptions["fees"]

    for _ in range(iterations):
        # Rail: randomize opt-in and seasonality a bit
        opt1 = np.clip(rng.beta(4, 96), 0, 1)  # around 4%
        opt2 = np.clip(rng.beta(2, 98), 0, 1)  # around 2%
        seasonality = np.clip(1.0 + rng.normal(0, 0.05, size=12), 0.7, 1.3).tolist()
        digital_share = np.clip(rng.normal(rail["digital_share_pct"] / 100.0, 0.05), 0.1, 0.99)

        avg_donation = 1.0 if rail["ask_type"] == "€1 fixed" else 2.0
        total_riders = rail["trenitalia_riders"] + rail["italo_riders"]
        s = np.array(seasonality)
        s = s / s.sum()
        eligible = total_riders * (rail["eligible_share_pct"]/100.0)
        exposed = eligible * digital_share
        donors = exposed * (opt1 if avg_donation <= 1.1 else opt2)
        gross = donors * avg_donation
        fee_rate = 0.0 if fees["processor"] == "Adyen Giving" else fees["rate_pct"]/100.0
        net_rail = gross * (1.0 - fee_rate) - (fees["fixed_eur"] if fees["processor"] != "Adyen Giving" else 0.0) * donors

        # Retail
        opt_retail = np.clip(rng.beta(5, 95), 0, 1)
        prevalence = np.clip(rng.uniform(0.6, 0.9), 0, 1)
        tri_mean = (0.01 + 0.50 + 0.99) / 3.0
        expected_round = tri_mean * prevalence
        annual_grocery = retail["households"] * retail["istat_monthly_spend_2023"] * 12 * (retail["grocery_share_pct"]/100.0)
        tx = annual_grocery / max(retail["avg_receipt_eur"], 0.01)
        donors_r = tx * opt_retail
        fee_rate_r = 0.0 if fees["processor"] == "Adyen Giving" else fees["rate_pct"]/100.0
        gross_r = donors_r * expected_round
        net_retail = gross_r * (1.0 - fee_rate_r) - (fees["fixed_eur"] if fees["processor"] != "Adyen Giving" else 0.0) * donors_r

        results.append({"total_net": float(net_rail + net_retail)})

    return pd.DataFrame(results)




