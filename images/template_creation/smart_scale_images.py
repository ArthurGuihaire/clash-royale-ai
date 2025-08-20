common = ['Arrows', 'Zap', 'GiantSnowball', 'RoyalDelivery', 'Minions', 'Archers', 'Knight', 'SpearGoblins', 'Goblins', 'Bomber', 'Skeletons', 'Barbarians', 'ElectroSpirit', 'SkeletonDragons', 'FireSpirit', 'Bats', 'RoyalRecruits', 'RoyalGiant', 'IceSpirit', 'Berserker', 'SkeletonBarrel', 'GoblinGang', 'EliteBarbarians', 'MinionHorde', 'Firecracker', 'Rascals', 'Cannon', 'Mortar', 'Tesla']
rare = ['Fireball', 'Rocket', 'Earthquake', 'MiniPEKKA', 'Musketeer', 'Giant', 'Valkyrie', 'MegaMinion', 'BattleRam', 'Wizard', 'FlyingMachine', 'HogRider', 'RoyalHogs', 'ThreeMusketeers', 'BattleHealer', 'IceGolem', 'DartGoblin', 'Furnace', 'Zappies', 'GoblinDemolisher', 'HealSpirit', 'SuspiciousBush', 'ElixirGolem', 'GoblinCage', 'GoblinHut', 'Tombstone', 'BombTower', 'InfernoTower', 'BarbarianHut', 'ElixirCollector']
epic = ['GoblinBarrel', 'Lightning', 'Freeze', 'BarbarianBarrel', 'Poison', 'GoblinCurse', 'Rage', 'Clone', 'Tornado', 'Mirror', 'Void', 'Guards', 'BabyDragon', 'SkeletonArmy', 'Witch', 'PEKKA', 'DarkPrince', 'Prince', 'Balloon', 'GiantSkeleton', 'RuneGiant', 'GoblinGiant', 'Hunter', 'Golem', 'ElectroDragon', 'WallBreakers', 'ElectroGiant', 'Bowler', 'Executioner', 'CannonCart', 'XBow', 'GoblinDrill']
legendary = ['TheLog', 'Graveyard', 'MegaKnight', 'RamRider', 'ElectroWizard', 'InfernoDragon', 'Sparky', 'Miner', 'Princess', 'Phoenix', 'RoyalGhost', 'IceWizard', 'MagicArcher', 'Bandit', 'LavaHound', 'NightWitch', 'Lumberjack', 'SpiritEmpress', 'GoblinMachine', 'MotherWitch', 'Fisherman']
champion = ['GoldenKnight', 'SkeletonKing', 'BossBandit', 'ArcherQueen', 'MightyMiner', 'Goblinstein', 'LittlePrince', 'Monk']
evolution = ['GiantSnowball', 'GoblinBarrel', 'Zap', 'Archers', 'Barbarians', 'Bats', 'BattleRam', 'Bomber', 'DartGoblin', 'ElectroDragon', 'Executioner', 'Firecracker', 'Furnace', 'GoblinGiant', 'Hunter', 'IceSpirit', 'InfernoDragon', 'Knight', 'Lumberjack', 'MegaKnight', 'Musketeer', 'PEKKA', 'RoyalGiant', 'RoyalRecruits', 'SkeletonBarrel', 'Skeletons', 'Valkyrie', 'WallBreakers', 'Witch', 'Wizard', 'Cannon', 'GoblinCage', 'GoblinDrill', 'Mortar', 'Tesla']

for i in range(len(common)):
    common[i] += "Card_crop.png"
for i in range(len(rare)):
    rare[i] += "Card_crop.png"
for i in range(len(epic)):
    epic[i] += "Card_crop.png"
for i in range(len(legendary)):
    legendary[i] += "Card_crop.png"
for i in range(len(champion)):
    champion[i] += "Card_crop.png"
for i in range(len(evolution)):
    evolution[i] += "CardEvolution_crop.png"

import os
import subprocess
for filename in os.listdir("borderless_raw"):
    actual_name = "borderless_raw/" + filename
    output = "templates_borderless/" + filename
    intermediate = "/dev/shm/temp.png"
    for name in evolution:
        if name == filename:
            subprocess.run(["magick", actual_name, "-resize", "60%", intermediate])
            subprocess.run(["magick", intermediate, "-set", "option:distort:viewport", "%[fx:w-11-11]x%[fx:h-13-12]+11+13", "-distort", "SRT", "0", "+repage", output])
            print(f"{filename} is evolution")
            continue
    for name in common:
        if name == filename:
            subprocess.run(["magick", actual_name, "-resize", "46%", intermediate])
            subprocess.run([
    "magick", intermediate,
    "-set", "option:distort:viewport",
    "%[fx:w-0-0]x%[fx:h-0-3]+0+0",
    "-distort", "SRT", "0",
    "+repage", output
], check=True)

            print(f"{filename} is common")
            continue
    for name in rare:
        if name == filename:
            subprocess.run(["magick", actual_name, "-resize", "50%", intermediate])
            subprocess.run([
    "magick", intermediate,
    "-set", "option:distort:viewport",
    "%[fx:w-3-5]x%[fx:h-2-8]+3+2",
    "-distort", "SRT", "0",
    "+repage", output
], check=True)
            print(f"{filename} is rare")
            continue
    for name in epic:
        if name == filename:
            subprocess.run(["magick", actual_name, "-resize", "46%", intermediate])
            subprocess.run([
    "magick", intermediate,
    "-set", "option:distort:viewport",
    "%[fx:w-1-1]x%[fx:h-0-4]+1+0",
    "-distort", "SRT", "0",
    "+repage", output
], check=True)
            print(f"{filename} is epic")
            continue
    for name in legendary:
        if name == filename:
            subprocess.run(["magick", actual_name, "-resize", "48%", intermediate])
            subprocess.run([
    "magick", intermediate,
    "-set", "option:distort:viewport",
    "%[fx:w-3-1]x%[fx:h-2-3]+3+2",
    "-distort", "SRT", "0",
    "+repage", output
], check=True)

            print(f"{filename} is legendary")
            continue
    for name in champion:
        if name == filename:
            subprocess.run(["magick", actual_name, "-resize", "48%", intermediate])
            subprocess.run([
    "magick", intermediate,
    "-set", "option:distort:viewport",
    "%[fx:w-4-0]x%[fx:h-9-0]+4+9",
    "-distort", "SRT", "0",
    "+repage", output
], check=True)
            print(f"{filename} is champion")
            continue
