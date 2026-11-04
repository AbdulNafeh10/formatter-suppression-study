"""Explicit-unit uncertainty calculations, never IID trial-level inference."""

import math
from numbers import Integral
from statistics import NormalDist

import numpy as np


def wilson_interval(successes, trials, confidence=0.95):
    if (
        not isinstance(successes, Integral)
        or not isinstance(trials, Integral)
        or isinstance(successes, bool)
        or isinstance(trials, bool)
        or trials <= 0
        or not 0 <= successes <= trials
        or not 0 < confidence < 1
    ):
        raise ValueError(
            "Wilson requires integer 0 <= successes <= positive trials and 0 < confidence < 1"
        )
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    p = successes / trials
    denominator = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denominator
    half = (
        z
        * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials))
        / denominator
    )
    return max(0.0, center - half), min(1.0, center + half)


def finite_population_bounds(confirmed, unresolved, sampled, population):
    values = (confirmed, unresolved, sampled, population)
    if (
        any(not isinstance(v, Integral) or isinstance(v, bool) for v in values)
        or population <= 0
        or not 0 <= sampled <= population
        or not 0 <= confirmed + unresolved <= sampled
        or min(confirmed, unresolved) < 0
    ):
        raise ValueError("Invalid finite-population outcome counts")
    return (
        confirmed / population,
        (confirmed + unresolved + population - sampled) / population,
    )


def paired_bounds(black, ruff):
    """Finite paired contrast bounds; unknown statuses stay unknown."""
    if len(black) != len(ruff) or not len(black):
        raise ValueError("Nonempty aligned pairs required")
    allowed = {0, 1, None}
    if any(value not in allowed for value in list(black) + list(ruff)):
        raise ValueError("Binary indicators or None required")
    lower = sum(
        (0 if b is None else b) - (1 if r is None else r) for b, r in zip(black, ruff)
    ) / len(black)
    upper = sum(
        (1 if b is None else b) - (0 if r is None else r) for b, r in zip(black, ruff)
    ) / len(black)
    return lower, upper


def cluster_bootstrap(
    black_counts, ruff_counts, denominators, *, seed, replicates=20000
):
    """Resample whole paired clusters; return rates/differences and all draws."""
    b, r, n = [
        np.asarray(values, dtype=np.float64)
        for values in (black_counts, ruff_counts, denominators)
    ]
    if (
        b.ndim != 1
        or b.shape != r.shape
        or b.shape != n.shape
        or len(b) == 0
        or not all(np.isfinite(x).all() for x in (b, r, n))
        or np.any(n <= 0)
        or np.any(b < 0)
        or np.any(r < 0)
        or np.any(b > n)
        or np.any(r > n)
        or not isinstance(replicates, Integral)
        or replicates < 2
    ):
        raise ValueError(
            "Nonempty valid paired cluster counts and at least two replicates required"
        )
    rng = np.random.Generator(np.random.PCG64(seed))
    indexes = rng.integers(0, len(b), size=(replicates, len(b)))
    sampled_n = n[indexes].sum(axis=1)
    draws = np.column_stack(
        (b[indexes].sum(axis=1) / sampled_n, r[indexes].sum(axis=1) / sampled_n)
    )
    draws = np.column_stack((draws, draws[:, 0] - draws[:, 1]))
    point = np.array(
        [b.sum() / n.sum(), r.sum() / n.sum(), (b.sum() - r.sum()) / n.sum()]
    )
    endpoints = np.quantile(draws, [0.025, 0.975], axis=0, method="linear")
    result = {
        "clusters": len(b),
        "paired_cases": int(n.sum()),
        "seed": int(seed),
        "replicates": int(replicates),
        "level": 0.95,
        "method": "paired whole-cluster percentile bootstrap; linear quantiles",
        "interpretation": "conditional exchangeable-cluster model sensitivity; not ecosystem coverage",
        "statistics": {
            name: {
                "estimate": float(point[i]),
                "lower": float(endpoints[0, i]),
                "upper": float(endpoints[1, i]),
            }
            for i, name in enumerate(("black_rate", "ruff_rate", "black_minus_ruff"))
        },
    }
    return result, draws
