import csv, pickle

with open("characters.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    key_strings = next(reader)
    keys = [key_strings.index("Name"), key_strings.index("Scale"), key_strings.index("CollisionRadius")]

    dict_array = []

    for line in reader:
        tmp_dict = {}
        tmp_dict[key_strings[keys[0]]] = line[keys[0]]
        for i in range(1, len(keys)):
            try:
                tmp_dict[key_strings[keys[i]]] = int(line[keys[i]])
            except:
                tmp_dict[key_strings[keys[i]]] = 0
        if len(tmp_dict) > 0:
            dict_array.append(tmp_dict)
        print(tmp_dict["Name"])
        try:
            print(tmp_dict["CollisionRadius"])
        except: print("error")

    print(len(dict_array))

with open("characters.pkl", 'wb') as pickle_file:
    pickle.dump(dict_array, pickle_file)

with open("spells_characters.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    key_strings = next(reader)
    keys = [key_strings.index("Name"), key_strings.index("ManaCost"), key_strings.index("SummonNumber"), key_strings.index("SummonRadius"), key_strings.index("SummonWidth"), key_strings.index("SummonCharacter")]

    dict_array = []

    for line in reader:
        tmp_dict = {}
        tmp_dict[key_strings[keys[0]]] = line[keys[0]]
        for i in range(1, len(keys)):
            try:
                tmp_dict[key_strings[keys[i]]] = int(line[keys[i]])
            except:
                tmp_dict[key_strings[keys[i]]] = 0
        if len(tmp_dict) > 0:
            dict_array.append(tmp_dict)
    print(len(dict_array))

with open("troops.pkl", 'wb') as csv_file:
    pickle.dump(dict_array, csv_file)

with open("spells_other.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    key_strings = next(reader)
    keys = [key_strings.index("Name"), key_strings.index("ManaCost"), key_strings.index("Projectile"), key_strings.index("Radius")]

    dict_array = []

    for line in reader:
        tmp_dict = {}
        tmp_dict[key_strings[keys[0]]] = line[keys[0]]
        for i in range(1, len(keys)):
            try:
                tmp_dict[key_strings[keys[i]]] = int(line[keys[i]])
            except:
                tmp_dict[key_strings[keys[i]]] = 0
        if len(tmp_dict) > 0:
            dict_array.append(tmp_dict)

    print(len(dict_array))

with open("spells.pkl", 'wb') as csv_file:
    pickle.dump(dict_array, csv_file)

with open("spells_buildings.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    key_strings = next(reader)
    keys = [key_strings.index("Name"), key_strings.index("ManaCost")]

    dict_array = []

    for line in reader:
        tmp_dict = {}
        tmp_dict[key_strings[keys[0]]] = line[keys[0]]
        for i in range(1, len(keys)):
            try:
                tmp_dict[key_strings[keys[i]]] = int(line[keys[i]])
            except:
                tmp_dict[key_strings[keys[i]]] = 0
        if (len(tmp_dict) > 0):
            dict_array.append(tmp_dict)

    print(len(dict_array))

with open("buildings.pkl", 'wb') as csv_file:
    pickle.dump(dict_array, csv_file)

with open("projectiles.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    key_strings = next(reader)
    keys = [key_strings.index("Name"), key_strings.index("Speed"), key_strings.index("Radius")]

    dict_array = []

    for line in reader:
        tmp_dict = {}
        tmp_dict[key_strings[keys[0]]] = line[keys[0]]
        for i in range(1, len(keys)):
            try:
                tmp_dict[key_strings[keys[i]]] = int(line[keys[i]])
            except:
                tmp_dict[key_strings[keys[i]]] = 0
        if (len(tmp_dict) > 0):
            dict_array.append(tmp_dict)

    print(len(dict_array))

with open("projectiles.pkl", 'wb') as csv_file:
    pickle.dump(dict_array, csv_file)
