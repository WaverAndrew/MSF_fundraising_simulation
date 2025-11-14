from typing import List, Literal

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, model_validator


AskType = Literal["€1 fixed", "€2 fixed", "€1 or €2 choice"]


class RailInputs(BaseModel):
    trenitalia_riders: int = Field(ge=0)
    italo_riders: int = Field(ge=0)
    digital_share: float = Field(ge=0.0, le=1.0)
    eligible_share: float = Field(ge=0.0, le=1.0)
    ask_type: AskType
    choice_share_eur1: float = Field(0.7, ge=0.0, le=1.0)
    optin_web_1: float = Field(0.04, ge=0.0, le=1.0)
    optin_web_2: float = Field(0.02, ge=0.0, le=1.0)
    optin_pos: float = Field(0.015, ge=0.0, le=1.0)
    seasonality: List[float] = Field(default_factory=lambda: [1.0] * 12)
    fee_rate: float = Field(0.0, ge=0.0, le=1.0)
    fee_fixed: float = Field(0.0, ge=0.0)
    processor: str = "Adyen Giving"

    @model_validator(mode="after")
    def validate_seasonality(self):
        if len(self.seasonality) != 12:
            raise ValueError("Seasonality must have 12 values")
        return self


def _avg_donation(ask_type: AskType, choice_share_eur1: float) -> float:
    if ask_type == "€1 fixed":
        return 1.0
    if ask_type == "€2 fixed":
        return 2.0
    return 1.0 * choice_share_eur1 + 2.0 * (1.0 - choice_share_eur1)


def compute_rail_monthly(inputs: RailInputs, months: int = 12) -> pd.DataFrame:
    total_riders = inputs.trenitalia_riders + inputs.italo_riders
    seasonality = np.array(inputs.seasonality, dtype=float)
    seasonality = seasonality / seasonality.sum()
    avg_donation = _avg_donation(inputs.ask_type, inputs.choice_share_eur1)
    
    # Adjust seasonality for partial year
    if months < 12:
        seasonality = seasonality[:months]
        seasonality = seasonality / seasonality.sum()

    rows = []
    for m in range(months):
        monthly_riders = total_riders * seasonality[m]
        eligible = monthly_riders * inputs.eligible_share
        exposed_digital = eligible * inputs.digital_share

        # Assume all donations happen on digital in this model; POS shown as separate opt-in level
        # Effective opt-in approximated by weighted average of €1/€2 rates
        if avg_donation <= 1.05:
            optin = inputs.optin_web_1
        elif avg_donation >= 1.95:
            optin = inputs.optin_web_2
        else:
            # blend
            w1 = (2.0 - avg_donation)
            w2 = (avg_donation - 1.0)
            optin = (inputs.optin_web_1 * w1 + inputs.optin_web_2 * w2)

        donors = exposed_digital * optin
        gross = donors * avg_donation
        net = gross * (1.0 - inputs.fee_rate) - inputs.fee_fixed * donors

        rows.extend([
            {"month": m + 1, "year": 1, "operator": "all", "channel": "digital", "metric": "riders", "value": monthly_riders},
            {"month": m + 1, "year": 1, "operator": "all", "channel": "digital", "metric": "eligible", "value": eligible},
            {"month": m + 1, "year": 1, "operator": "all", "channel": "digital", "metric": "exposed_digital", "value": exposed_digital},
            {"month": m + 1, "year": 1, "operator": "all", "channel": "digital", "metric": "donors", "value": donors},
            {"month": m + 1, "year": 1, "operator": "all", "channel": "digital", "metric": "gross", "value": gross},
            {"month": m + 1, "year": 1, "operator": "all", "channel": "digital", "metric": "net", "value": net},
        ])

    # Split annual net by operator proportionally by riders for the bar chart
    df = pd.DataFrame(rows)
    ratio_tr = inputs.trenitalia_riders / max(total_riders, 1)
    ratio_it = inputs.italo_riders / max(total_riders, 1)
    annual_net = df[df["metric"] == "net"]["value"].sum()
    rows_extra = [
        {"month": 0, "year": 1, "operator": "Trenitalia", "channel": "digital", "metric": "net", "value": annual_net * ratio_tr},
        {"month": 0, "year": 1, "operator": "Italo", "channel": "digital", "metric": "net", "value": annual_net * ratio_it},
    ]
    df = pd.concat([df, pd.DataFrame(rows_extra)], ignore_index=True)
    return df




