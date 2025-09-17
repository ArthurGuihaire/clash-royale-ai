import screenshot_utils
from enum import Enum
from card_types_enum import CardType
print(screenshot_utils.screenshot_dimensions("Knight", (5, 5)))

'''import pickle, json
from enum import Enum
class CardType(Enum):
    building = 0
    spell = 1
    troop = 2

with open('cards_dictionary.pkl', 'rb') as dictionary_file:
    dicitonary = pickle.load(dictionary_file)

def converter(o):
    if isinstance(o, CardType):
        return o.name   # or o.value if you prefer
    return str(o)       # fallback for other non-serializables

with open("dictionary.json", "w") as file:
    json.dump(dicitonary, file, indent=2, default=converter)
'''