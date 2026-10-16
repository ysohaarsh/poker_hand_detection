import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pokerHandDetector"))

from PokerHandFunction import findPokerHand  # noqa: E402


@pytest.mark.parametrize(
    "hand, expected",
    [
        (["KH", "AH", "QH", "JH", "10H"], "Royal Flush"),
        (["QC", "JC", "10C", "9C", "8C"], "Straight Flush"),
        (["5C", "5S", "5H", "5D", "QH"], "Four of a Kind"),
        (["2H", "2D", "2S", "10H", "10C"], "Full House"),
        (["2D", "KD", "7D", "6D", "5D"], "Flush"),
        (["JC", "10H", "9C", "8C", "7D"], "Straight"),
        (["10H", "10C", "10D", "2D", "5S"], "Three of a Kind"),
        (["KD", "KH", "5C", "5S", "6D"], "Two Pair"),
        (["2D", "2S", "9C", "KD", "10C"], "Pair"),
        (["KD", "5H", "2D", "10C", "JH"], "High Card"),
        # Ace-low straights
        (["AC", "2H", "3D", "4S", "5C"], "Straight"),
        (["AH", "2H", "3H", "4H", "5H"], "Straight Flush"),
        # Ace-high is not a wrap-around straight
        (["QC", "KH", "AD", "2S", "3C"], "High Card"),
    ],
)
def test_find_poker_hand(hand, expected):
    assert findPokerHand(hand) == expected
