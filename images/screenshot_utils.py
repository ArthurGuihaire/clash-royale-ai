import pickle, random, numpy
from enum import Enum
from card_types_enum import CardType

import sys
sys.modules['__main__'].CardType = CardType

with open("cards_dictionary.pkl", 'rb') as dictionary_file:
    cards_dictionary = pickle.load(dictionary_file)

def sc_units_to_pixels(tiles_coordinates):
    x = tiles_coordinates[0] * 0.02875 # 28.75 pixels per tile
    y = tiles_coordinates[1] * 0.02315 # 23.15 pixels per tile
    return (x, y)

def get_time_until_screenshot(card_name, row, column):
    match cards_dictionary[card_name]["Type"]:
        case CardType.building:
            if random.random() < 0.5:
                return 0.1
            return 0.9
        case CardType.troop:
            return 0.25
        case CardType.spell:
            try:
                if cards_dictionary[card_name]["Speed"] == 0:
                    return 0.5
            except:
                return 0.5
            else:
                delta_y = 11.5 - row
                delta_x = 8.5 - column
                distance = (delta_x * delta_x) + (delta_y * delta_y)
                return distance / cards_dictionary[card_name]["Speed"]

def screenshot_dimensions(card_name, coordinates):
    match cards_dictionary[card_name]["Type"]:
        case CardType.building:
            # manually enter building size
            return
        case CardType.troop:
            size = (cards_dictionary[card_name]["Size"], cards_dictionary[card_name]["Size"] * 1.6)
            summon_number = cards_dictionary[card_name]["SummonNumber"]
            if (summon_number <= 1):
                return [(sc_units_to_pixels(coordinates-size), sc_units_to_pixels(coordinates+size))]
            elif cards_dictionary[card_name]["SummonRadius"] >= 1:
                summon_radius = cards_dictionary[card_name]["SummonRadius"]
                coordinates = numpy.empty((summon_number, 2), dtype=numpy.float64)
                return_array = numpy.empty((summon_number, 2, 2), dtype=numpy.float64)
                interval = numpy.pi * 2 / summon_radius
                half_pi = numpy.pi / 2
                for i in range(summon_number):
                    coordinates[i][0] = numpy.cos(i*interval + half_pi)
                    coordinates[i][1] = numpy.sin(i*interval + half_pi)
                    return_array[i] = (sc_units_to_pixels(coordinates[i]-size), sc_units_to_pixels(coordinates[i]+size))
                return return_array

            elif cards_dictionary[card_name]["SummonWidth"]:
                summon_width = cards_dictionary[card_name]["SummonWidth"]
                distance = summon_width/(summon_number - 1)
                positions_x_range = range(coordinates[0] - summon_width / 2, coordinates[0] + summon_width / 2 + 1, distance)
                coordinates_array = [(x_pos, coordinates[1]) for x_pos in positions_x_range]
                return_array = [(sc_units_to_pixels(coordinates_value - size), sc_units_to_pixels(coordinates_value + size)) for coordinates_value in coordinates_array]
                return return_array
            else:
                print(f"{card_name} spawns multiple units, but unspecified configuration")

        case CardType.spell:
            radius = cards_dictionary[card_name]["Radius"]
            return [(coordinates - (radius, radius), coordinates + (radius, radius))]
