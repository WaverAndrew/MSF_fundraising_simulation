from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

from models.rail import RailInputs, compute_rail_monthly
from models.retail import RetailInputs, compute_retail_monthly


def run_monte_carlo(
    rail_inputs: Optional[RailInputs],
    retail_inputs: Optional[RetailInputs],
    months: int,
    iterations: int = 2000,
    seed: int | None = None
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    results = []

    if rail_inputs is None or retail_inputs is None:
        return pd.DataFrame({"total_net": []})

    for _ in range(iterations):
        # Rail: randomize opt-in and seasonality around actual inputs
        base_opt1 = rail_inputs.optin_web_1
        base_opt2 = rail_inputs.optin_web_2
        opt1 = np.clip(rng.beta(max(1, base_opt1 * 100), max(1, (1 - base_opt1) * 100)), 0, 1)
        opt2 = np.clip(rng.beta(max(1, base_opt2 * 100), max(1, (1 - base_opt2) * 100)), 0, 1)
        
        # Randomize seasonality around actual values
        base_season = np.array(rail_inputs.seasonality)
        seasonality = np.clip(base_season + rng.normal(0, 0.05, size=len(base_season)), 0.7, 1.3).tolist()
        
        # Randomize digital share around actual
        digital_share = np.clip(rng.normal(rail_inputs.digital_share, 0.05), 0.1, 0.99)
        
        # Create randomized rail inputs
        rail_inputs_mc = rail_inputs.model_copy()
        rail_inputs_mc.optin_web_1 = opt1
        rail_inputs_mc.optin_web_2 = opt2
        rail_inputs_mc.seasonality = seasonality
        rail_inputs_mc.digital_share = digital_share
        
        # Compute rail using actual model
        rail_df = compute_rail_monthly(rail_inputs_mc, months=months)
        net_rail = rail_df[rail_df["metric"] == "net"]["value"].sum()

        # Retail: randomize opt-in and charm prevalence around actual inputs
        base_opt_retail = retail_inputs.optin
        opt_retail = np.clip(rng.beta(max(1, base_opt_retail * 100), max(1, (1 - base_opt_retail) * 100)), 0, 1)
        base_prevalence = retail_inputs.charm_prevalence
        prevalence = np.clip(rng.normal(base_prevalence, 0.05), 0.6, 0.9)
        
        # Create randomized retail inputs
        retail_inputs_mc = retail_inputs.model_copy()
        retail_inputs_mc.optin = opt_retail
        retail_inputs_mc.charm_prevalence = prevalence
        
        # Compute retail using actual model
        retail_df = compute_retail_monthly(retail_inputs_mc, months=months)
        net_retail = retail_df[retail_df["metric"] == "net"]["value"].sum()

        results.append({"total_net": float(net_rail + net_retail)})

    return pd.DataFrame(results)




