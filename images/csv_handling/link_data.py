import pickle, glob
from enum import Enum

with open("projectiles.pkl", 'rb') as f:
    projectiles = pickle.load(f)

with open("buildings.pkl", 'rb') as f:
    buildings = pickle.load(f)
    for i in range(len(buildings)):
        match buildings[i]["Name"]:
            case "Xbow":
                buildings[i]["Name"] = "X-Bow"

with open("spells.pkl", 'rb') as f:
    spells = pickle.load(f)
    for i in range(len(spells)):
        match spells[i]["Name"]:
            case "Log":
                spells[i]["Name"] = "TheLog"
            case "DarkMagic":
                spells[i]["Name"] = "Void"
            case "Snowball":
                spells[i]["Name"] = "GiantSnowball"
            case "BarbLog":
                spells[i]["Name"] = "BarbarianBarrel"

with open("troops.pkl", 'rb') as f:
    troops = pickle.load(f)

    furnace_dict = {
        "Name": "Furnace",
        "ManaCost": 3,
        "SummonNumber": 1,
        "SummonRadius": 0,
        "SummonWidth": 0
    }
    heal_spirit_dict = {
        "Name": "HealSpirit",
        "ManaCost": 1,
        "SummonNumber": 1,
        "SummonRadius": 0,
        "SummonWidth": 0
    }
    rune_giant_dict = {
        "Name": "RuneGiant",
        "ManaCost": 4,
        "SummonNumber": 1,
        "SummonRadius": 0,
        "SummonWidth": 0
    }
    ice_golem_dict = {
        "Name": "IceGolem",
        "ManaCost": 2,
        "SummonNumber": 1,
        "SummonRadius": 0,
        "SummonWidth": 0
    }

    troops.append(furnace_dict)
    troops.append(heal_spirit_dict)
    troops.append(rune_giant_dict)
    troops.append(ice_golem_dict)

    for i in range(len(troops)):
        match troops[i]["Name"]:
            case "SkeletonBalloon":
                troops[i]["Name"] = "SkeletonBarrel"
            case "AxeMan":
                troops[i]["Name"] = "Executioner"
            case "MiniSparkys":
                troops[i]["Name"] = "Zappies"
            case "Wallbreakers":
                troops[i]["Name"] = "WallBreakers"
            case "Archer":
                troops[i]["Name"] = "Archers"
            case "RageBarbarian":
                troops[i]["Name"] = "Lumberjack"
            case "MovingCannon":
                troops[i]["Name"] = "CannonCart"
            case "AngryBarbarians":
                troops[i]["Name"] = "EliteBarbarians"
            case "WitchMother":
                troops[i]["Name"] = "MotherWitch"
            case "DarkWitch":
                troops[i]["Name"] = "NightWitch"
            case "Ghost":
                troops[i]["Name"] = "RoyalGhost"
            case "IceSpirits":
                troops[i]["Name"] = "IceSpirit"
            case "SkeletonWarriors":
                troops[i]["Name"] = "Guards"
            case "DartBarrell":
                troops[i]["Name"] = "FlyingMachine"
            case "BlowdartGoblin":
                troops[i]["Name"] = "DartGoblin"
            case "Assassin":
                troops[i]["Name"] = "Bandit"
            case "FireSpirits":
                troops[i]["Name"] = "FireSpirit"
            case "ZapMachine":
                troops[i]["Name"] = "Sparky"
            case "EliteArcher":
                troops[i]["Name"] = "MagicArcher"

class CardType(Enum):
    building = 0
    spell = 1
    troop = 2

final_dict_array = [{}]

for filename in glob.glob("templates_borderless/*.png"):
    if filename.endswith("Evolution_crop.png"): continue
    card_name = filename.split("Card")[0][21:]
    exists = False
    tmp_dict = {}
    for dictionary in buildings:
        if dictionary["Name"].lower() == card_name.lower():
            exists = True
            tmp_dict = dictionary
            tmp_dict["Type"] = CardType.building
            tmp_dict["Name"] = card_name
    for dictionary in spells:
        if dictionary["Name"].lower() == card_name.lower():
            exists = True
            tmp_dict = dictionary
            tmp_dict["Type"] = CardType.spell
            tmp_dict["Name"] = card_name
            for projectile_dictionary in projectiles:
                if projectile_dictionary["Name"] == tmp_dict["projectile"]:
                    tmp_dict["Speed"] = projectile_dictionary["Speed"]

    for dictionary in troops:
        if dictionary["Name"].lower() == card_name.lower():
            exists = True
            tmp_dict = dictionary
            tmp_dict["Type"] = CardType.troop
            tmp_dict["Name"] = card_name

    if not exists:
        print(f"Missing entry for {card_name}")
        continue

    final_dict_array.append(tmp_dict)

with open("cards_dict_array.pkl", 'wb') as dictionary_file:
    pickle.dump(final_dict_array, dictionary_file)