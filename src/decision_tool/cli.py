

      
  from __future__ import annotations

from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd

from decision_tool.core import score_and_rank

# Set to False if you don't want to show the plot window
PLOT = True


def ask_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter an integer.")


def ask_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number.")


def ask_yes_no(prompt: str) -> bool:
    while True:
        resp = input(prompt).strip().lower()
        if resp in ("yes", "y"):
            return True
        if resp in ("no", "n"):
            return False
        print("Please answer 'yes' or 'no'.")


def build_dataframe(criteria: List[str], alternatives: List[str], data: Dict[str, List[float]]) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df.insert(0, "Alternative", alternatives)
    return df


def main() -> None:
    num_alternatives = ask_int("Enter the number of alternatives: ")
    while num_alternatives <= 0:
        num_alternatives = ask_int("Please enter a positive number of alternatives: ")

    criteria = input(
        "Enter criteria names separated by commas (e.g. Cost,Quality,Reliability,Sustainability): "
    ).split(",")
    criteria = [c.strip() for c in criteria if c.strip()]
    if not criteria:
        print("No criteria provided. Exiting.")
        return

    criteria_type: Dict[str, bool] = {}
    for c in criteria:
        criteria_type[c] = ask_yes_no(f"Is higher value better for {c}? (yes/no): ")

    alternatives: List[str] = []
    data: Dict[str, List[float]] = {c: [] for c in criteria}

    for i in range(num_alternatives):
        name = input(f"Enter name of alternative {i+1}: ").strip()
        while not name or name in alternatives:
            name = input("Please enter a unique, non-empty name: ").strip()
        alternatives.append(name)

        for c in criteria:
            value = ask_float(f"Enter {c} value for {name}: ")
            data[c].append(value)

    df = build_dataframe(criteria, alternatives, data)

    weights: Dict[str, float] = {}
    print("\nEnter weights for each criterion. They must sum to 1.\n")
    for c in criteria:
        w = ask_float(f"Enter weight for {c} (0-1): ")
        while w < 0 or w > 1:
            w = ask_float("Please enter a weight between 0 and 1: ")
        weights[c] = w

    # Compute ranking (core logic)
    try:
        result = score_and_rank(df, criteria, criteria_type, weights)
    except ValueError as e:
        print(f"\nError: {e}")
        return

    ranked = result.ranked

    print("\nRanking of alternatives:")
    print(ranked[["Alternative", "Score"]])

    print("\nRecommended option:")
    print(result.recommended)

    if PLOT:
        plt.figure(figsize=(8, 5))
        plt.bar(ranked["Alternative"], ranked["Score"])
        plt.xlabel("Alternative")
        plt.ylabel("Score")
        plt.title("Ranking of Alternatives")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
