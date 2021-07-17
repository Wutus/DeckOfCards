from django.http import response
import card_api
from typing import List
from Card import Card

class Deck:
    """Wrapper for Deck object"""
    def __init__(self, shuffle: bool = True):
        response = card_api.deck_shuffle() if shuffle else card_api.deck_new() 
        self._id = response["deck_id"]
        self._shuffled = response["shuffled"]
        self._remaining = response["remaining"]

    @property
    def id(self):
        return self._id

    @property
    def shuffled(self):
        return self._shuffled

    @property
    def remaining(self):
        return self._remaining

    def draw(self, count: int = 1) -> List[Card]:
        response = card_api.deck_draw(self.id, count)
        self._remaining = response["remaining"]
        return [Card._from_code(card["code"]) for card in response["cards"]]