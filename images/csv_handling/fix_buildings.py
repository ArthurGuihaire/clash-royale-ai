import pickle
from enum import Enum

class CardType(Enum):
    building = 0
    spell = 1
    troop = 2

with open("cards_dictionary.pkl", 'rb') as dictionary_file:
    cards_dictionary = pickle.load(dictionary_file)

for dictionary_entry in cards_dictionary:
    if cards_dictionary[dictionary_entry]["Type"] == CardType.building:
        cards_dictionary[dictionary_entry]["Radius"] = int(input(f"Width for {dictionary_entry}: "))

with open("cards_dicitonary.pkl", 'wb') as dictionary_file:
    pickle.dump(cards_dictionary, dictionary_file)