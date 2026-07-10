from magicli_tarot import get_readings, get_cards, select_model
from constants import models
import random


def test_get_readings():
    readings = get_readings()
    assert readings == sorted(readings)


def test_get_cards_count():
    rng = random.Random(42)
    spread = ["Past", "Present", "Future"]
    cards = get_cards(spread, rng)

    assert len(cards) == 3


def test_get_cards_positions():
    rng = random.Random(42)
    spread = ["Past", "Present", "Future"]
    cards = get_cards(spread, rng)

    assert [c["position"] for c in cards] == spread


def test_get_cards_unique():
    rng = random.Random(42)
    spread = ["A", "B", "C", "D", "E"]
    cards = get_cards(spread, rng)
    names = [c["card"] for c in cards]

    assert len(names) == len(set(names))


def test_orientation_values():
    rng = random.Random(42)
    cards = get_cards(["A"] * 10, rng)

    for card in cards:
        assert card["orientation"] in (
            "Upright",
            "Reversed"
        )


def test_select_model():
    rng = random.Random(42)

    for _ in range(100):
        assert select_model(None, rng) in models


def test_exact_cards():
    rng = random.Random(42)
    cards = get_cards(spread=["a", "b", "c", "d"], rng=rng)
    assert cards == [{'position': 'a', 'card': 'Temperance', 'orientation': 'Upright'},
                     {'position': 'b', 'card': 'The Empress', 'orientation': 'Upright'},
                     {'position': 'c', 'card': 'King of Wands', 'orientation': 'Upright'},
                     {'position': 'd', 'card': 'Ten of Wands', 'orientation': 'Upright'}]


def test_exact_model():
    rng = random.Random(42)
    model = select_model(None, rng)
    assert model == "gemini-3.1-flash-lite"
