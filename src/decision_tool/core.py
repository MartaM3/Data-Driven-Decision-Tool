from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd


@dataclass(frozen=True)
class DecisionResult:
    ranked: pd.DataFrame
    recommended: str


def normalize_data(
    df: pd.DataFrame,
    criteria: List[str],
    criteria_type: Dict[str, bool],
) -> pd.DataFrame:
    """
    Normalize criteria columns to [0,1].
    If criteria_type[c] is False => lower is better; invert before scaling.
    """
    normalized_df = df.copy()

    for c in criteria:
        if c not in normalized_df.columns:
            raise ValueError(f"Missing criterion column: {c}")

        # Convert to numeric (fails fast if non-numeric)
        normalized_df[c] = pd.to_numeric(normalized_df[c], errors="raise")

        if not criteria_type.get(c, True):
            normalized_df[c] = df[c].max() - df[c]

        max_val = normalized_df[c].max()
        if max_val == 0:
            # Avoid division by zero; if all values are 0 after transform, keep zeros
            normalized_df[c] = 0.0
        else:
            normalized_df[c] = normalized_df[c] / max_val

    return normalized_df


def validate_weights(weights: Dict[str, float], criteria: List[str], tol: float = 0.01) -> None:
    """
    Validate that weights match criteria and sum to ~1.
    Raises ValueError if invalid.
    """
    missing = [c for c in criteria if c not in weights]
    if missing:
        raise ValueError(f"Missing weights for criteria: {missing}")

    total = sum(weights[c] for c in criteria)
    if abs(total - 1.0) > tol:
        raise ValueError(f"Weights must sum to 1 (±{tol}). Current sum: {total:.4f}")


def score_and_rank(
    df: pd.DataFrame,
    criteria: List[str],
    criteria_type: Dict[str, bool],
    weights: Dict[str, float],
) -> DecisionResult:
    """
    Compute weighted score and return ranked dataframe + recommended alternative.
    Expects df to include a column 'Alternative' and columns for each criterion.
    """
    if "Alternative" not in df.columns:
        raise ValueError("DataFrame must include an 'Alternative' column.")

    validate_weights(weights, criteria)

    normalized = normalize_data(df, criteria, criteria_type)

    scored = df.copy()
    scored["Score"] = 0.0
    for c in criteria:
        scored["Score"] += normalized[c] * float(weights[c])

    ranked = scored.sort_values(by="Score", ascending=False).reset_index(drop=True)
    recommended = str(ranked.loc[0, "Alternative"])

    return DecisionResult(ranked=ranked, recommended=recommended)
