from enum import Enum
import pickle

class CardType(Enum):
    building = 0
    spell = 1
    troop = 2

actual_dictionary = {}

with open("cards_dict_array.pkl", 'rb') as data_file:
    dict_array = pickle.load(data_file)

for dictionary in dict_array:
    if dictionary == {}: continue
    dictionary_entry = {}
    for entry in dictionary:
        if entry != "Name":
            dictionary_entry[entry] = dictionary[entry]
    actual_dictionary[dictionary["Name"]] = dictionary_entry

with open("cards_dictionary.pkl", 'wb') as dictionary_file:
    pickle.dump(actual_dictionary, dictionary_file)
