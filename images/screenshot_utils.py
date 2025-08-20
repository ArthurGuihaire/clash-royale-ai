import pickle, random
from enum import Enum

with open("cards_dictionary.pkl", 'rb') as dictionary_file:
    cards_dictionary = pickle.load(dictionary_file)

class CardType(Enum):
    building = 0
    spell = 1
    troop = 2

def get_time_until_screenshot(card_name, row, column):
    match cards_dictionary[card_name]["Type"]:
        case CardType.building:
            if random.random() < 0.5:
                return 0.1
            return 0.9
        case CardType.troop:
            return 0.5
        case CardType.spell:
            delta_y = 11.5 - row
            delta_x = 8.5 - column
            distance = (delta_x * delta_x) + (delta_y * delta_y)
            return distance / cards_dictionary[card_name]["Speed"]

def screenshot_dimensions(card_name, row, column):
    