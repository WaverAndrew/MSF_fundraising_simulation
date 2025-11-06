from enum import Enum
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field


class RetailMethod(str, Enum):
    TOP_DOWN = "top_down"
    DIRECT = "direct"


class RetailInputs(BaseModel):
    method: RetailMethod = RetailMethod.TOP_DOWN
    monthly_spend: float = Field(ge=0.0)
    grocery_share: float = Field(ge=0.0, le=1.0)
    avg_receipt: float = Field(ge=0.5)
    households: int = Field(ge=0)
    daily_receipts: int = Field(0, ge=0)
    stores: int = Field(0, ge=0)
    active_days: int = Field(ge=1, le=366)
    charm_prevalence: float = Field(ge=0.0, le=1.0)
    optin: float = Field(ge=0.0, le=1.0)
    fee_rate: float = Field(0.0, ge=0.0, le=1.0)
    fee_fixed: float = Field(0.0, ge=0.0)
    processor: str = "Adyen Giving"
    triangular_min: float = 0.01
    triangular_mode: float = 0.50
    triangular_max: float = 0.99
    payment_card_share: float = 0.7


def simulate_roundup_distribution(inputs: RetailInputs, n: int = 10000, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    samples = rng.triangular(inputs.triangular_min, inputs.triangular_mode, inputs.triangular_max, size=n)
    return samples * inputs.charm_prevalence


def _expected_roundup(inputs: RetailInputs) -> float:
    # Expected value of triangular(min, mode, max) is (a+b+c)/3
    tri_mean = (inputs.triangular_min + inputs.triangular_mode + inputs.triangular_max) / 3.0
    return tri_mean * inputs.charm_prevalence


def _transactions(inputs: RetailInputs) -> int:
    if inputs.method == RetailMethod.TOP_DOWN:
        annual_grocery = inputs.households * inputs.monthly_spend * 12.0 * inputs.grocery_share
        tx = int(annual_grocery / max(inputs.avg_receipt, 0.01))
        return tx
    return int(inputs.daily_receipts * inputs.stores * inputs.active_days)


def compute_retail_monthly(inputs: RetailInputs) -> pd.DataFrame:
    tx = _transactions(inputs)
    expected_round = _expected_roundup(inputs)
    donors = tx * inputs.optin
    gross = donors * expected_round
    net = gross * (1.0 - inputs.fee_rate) - inputs.fee_fixed * donors

    # simple split between online and in-store using payment mix
    online_share = inputs.payment_card_share
    in_store_share = 1.0 - online_share

    rows = []
    for m in range(12):
        rows.extend([
            {"month": m + 1, "year": 1, "channel": "all", "metric": "transactions", "value": tx/12.0},
            {"month": m + 1, "year": 1, "channel": "all", "metric": "donors", "value": donors/12.0},
            {"month": m + 1, "year": 1, "channel": "all", "metric": "gross", "value": gross/12.0},
            {"month": m + 1, "year": 1, "channel": "all", "metric": "net", "value": net/12.0},
            {"month": m + 1, "year": 1, "channel": "online", "metric": "net", "value": net/12.0 * online_share},
            {"month": m + 1, "year": 1, "channel": "in_store", "metric": "net", "value": net/12.0 * in_store_share},
        ])
    return pd.DataFrame(rows)




