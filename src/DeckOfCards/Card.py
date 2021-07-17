# %%
from enum import Enum, IntEnum, auto
from functools import cache
from io import BytesIO
import requests
import card_api

class CardValue(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    @property
    def code(self):
        return _value_code_dict[self]

_value_code_dict = {
    CardValue.ACE: "A",
    CardValue.TWO: "2",
    CardValue.THREE: "3",
    CardValue.FOUR: "4",
    CardValue.FIVE: "5",
    CardValue.SIX: "6",
    CardValue.SEVEN: "7",
    CardValue.EIGHT: "8",
    CardValue.NINE: "9",
    CardValue.TEN: "0",
    CardValue.JACK: "J",
    CardValue.QUEEN: "Q",
    CardValue.KING: "K"
}

_code_value_dict = {v:k for k,v in _value_code_dict.items()}

class CardSuit(Enum):
    HEARTS = auto()
    SPADES = auto()
    CLUBS = auto()
    DIAMONDS = auto()

    @property
    def code(self):
        return _suit_code_dict[self]

_suit_code_dict = {
    CardSuit.HEARTS: "H",
    CardSuit.SPADES: "S",
    CardSuit.CLUBS: "C",
    CardSuit.DIAMONDS: "D"
}

_code_suit_dict = {v:k for k,v in _suit_code_dict.items()}

# %%
class Card:
    """Wrapper for class object"""
    def __init__(self, card_value, card_suit):
        self._card_value = card_value
        self._card_suit = card_suit

    @staticmethod
    @cache
    def _from_code(code):
        if len(code) != 2 or code[0] not in _code_value_dict or code[1] not in _code_suit_dict:
            return card_api.DeckOfCardsImproperUseException(f"Invalid card code {code}")
        return Card(_code_value_dict[code[0]], _code_suit_dict[code[1]])

    @property
    def suit(self) -> CardSuit:
        return self._card_suit

    @property
    def value(self) -> CardValue:
        return self._card_value

    @property
    def code(self) -> str:
        return self.value.code + self.suit.code

    @property
    def image(self):
        image_bytes = card_api.get_image_content(self.code)
        return BytesIO(image_bytes)

    def __eq__(self, other):
        return isinstance(other, Card) and self.code == other.code