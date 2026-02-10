import pandas as pd

from decision_tool.core import score_and_rank


def test_score_and_rank_returns_score_and_recommended():
    df = pd.DataFrame(
        {
            "Alternative": ["A", "B", "C"],
            "Cost": [10, 14, 9],
            "Quality": [7, 9, 6],
        }
    )

    criteria = ["Cost", "Quality"]
    criteria_type = {"Cost": False, "Quality": True}  # lower cost better, higher quality better
    weights = {"Cost": 0.5, "Quality": 0.5}

    result = score_and_rank(df, criteria, criteria_type, weights)

    assert "Score" in result.ranked.columns
    assert len(result.ranked) == 3
    assert result.recommended in ["A", "B", "C"]
