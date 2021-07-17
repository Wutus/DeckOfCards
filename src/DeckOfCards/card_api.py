from functools import cache
import requests
from typing import Dict, Optional, Union

class DeckOfCardsImproperUseException(Exception):
    """Exception for Deck of Cards inccorect usage"""

class DeckOfCardsApiConnectionException(Exception):
    """Exception for Deck of Cards API connection error"""
    def __init__(self, response):
        self.response = response

class DeckOfCardsApiBehaviourException(Exception):
    """Exception for Deck of Cards API behaviour error"""
    def __init__(self, response_json):
        self.response_obj = response_json

values = {
    "api_base_url": "https://deckofcardsapi.com/api/",
    "image_base_url": "https://deckofcardsapi.com/static/img/",
    "card_image_extension": "png"
}

def image_url(code: str) -> str:
    return f"{values['image_base_url']}{code}.{values['card_image_extension']}"

@cache
def get_image_content(code: str) -> bytes:
    image_location = image_url(code)
    response = requests.get(image_location)
    return response.content

def api_url(path: str) -> str:
    return values["api_base_url"] + path

def api_get(path: str, params: Optional[Dict[Union[str, int], object]] = None) -> str:
    base_url = api_url(path)
    response = requests.get(base_url, params=params)
    if not response.ok:
        raise DeckOfCardsApiBehaviourException(response)
    response_obj = response.json()
    if not response_obj["success"]:
        raise DeckOfCardsApiBehaviourException(response_obj)
    return response_obj

def deck_new():
    return api_get("deck/new/")

def deck_shuffle(id: str = None, deck_count: int = None) -> Dict[str, object]:
    if id is not None and deck_count is not None:
        raise DeckOfCardsImproperUseException("Cannot pass deck count for existing deck")
    if id is None:
        id = "new"
    return api_get(f"deck/{id}/shuffle/", params={"deck_count": deck_count})

def deck_draw(id: str = None, count: int = 1):
    if id is None:
        id = "new"
    return api_get(f"deck/{id}/draw/", params={"count": count})