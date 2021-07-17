from card_api import api_get
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from Deck import Deck

deck = Deck()

while deck.remaining > 0:
    card = deck.draw()[0]
    print(f"{card.value=} {card.suit=} {card.code=}")
    plt.imshow(mpimg.imread(card.image))
    plt.show()
    plt.clf()