import numpy as np
from statsmodels.stats.power import NormalIndPower


def sample_size_two_proportions(p1: float, p2: float, alpha: float = 0.05, power: float = 0.8) -> float:
    effect = abs(p2 - p1)
    if effect <= 0:
        return np.inf
    pooled = (p1 * (1 - p1) + p2 * (1 - p2)) ** 0.5
    if pooled == 0:
        return np.inf
    standardized = effect / pooled
    analysis = NormalIndPower()
    n = analysis.solve_power(effect_size=standardized, alpha=alpha, power=power, alternative='two-sided')
    return n




