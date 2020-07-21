from classes.game import Person,bcolors
from classes.magic import Spell
from classes.inventory import item
import random

#Creating black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 40, 240, "black")

#Create White magic
cure = Spell("Cure", 22, 120, "white")
cura = Spell("Cura", 48, 200, "white")
#changed magic into a file and spell a class

#create some items
potion = item("Potion", "potion", "Heals 50 HP", 50)
hipotion = item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = item("Super-Potion", "potion", "Heals 350 HP", 350)
elixer = item("Elixer", "elixer", "Fully restores HP/MP of one party member", 500)
hielixer = item("Mega Elixer", "elixer", "Fully restores party's HP/MP", 500)

grenade = item("Grenade", "attack", "Deals 300 damage", 340)

player_spells = [fire, thunder, blizzard,
                 meteor, cure, cura, quake]
enemy_spells = [fire, meteor, quake]
player_items = [{"items": potion, "quantity": 15},
                {"items": hipotion, "quantity": 5},
                {"items": superpotion, "quantity": 5},
                {"items": elixer, "quantity": 5},
                {"items": hielixer, "quantity": 2},
                {"items": grenade, "quantity": 5}]

#Instantiate people
player1 = Person("  Artemis", 500, 200, 200, 34, player_spells, player_items) #creating a character to play
player2 = Person("    Gavin", 500, 200, 200, 34, player_spells, player_items)
player3 = Person("Zebronics", 500, 200, 200, 34, player_spells, player_items)
#creating an enemy to attack player
enemy1 = Person("      Mulch", 400, 240, 350, 56, [enemy_spells], [])
enemy2 = Person("Grim Reaper", 720, 320, 420, 45, [enemy_spells], [])
enemy3 = Person("       Opal", 400, 240, 350, 56, [enemy_spells], [])
players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i=0

while running:
    print("===========================================================================================================")
    print("NAME                                HP                                      MP")
    for player in players:
        player.get_stats()
        print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        print("\n" + bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
        player.choose_action()
        choice = input("Choose action for " + player.name.replace(" ", ""))
        index = int(choice) - 1  #to reduce the i variable from n to n-1 coz it starts at 1 and not 0
        print(player.name +" chooses ", choice)

        if index == 0:  # when attack is chosen
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print(player.name.replace(" ", "") + " attacked " + enemies[enemy].name.replace(" ", "") + " for ", dmg, " points of damage.")
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:  # when magic is chosen as action
            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1
            if magic_choice == -1:  # if nothing was selected
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n Not enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for ", str(magic_dmg), " HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + "has died.")
                    del enemies[enemy]

        elif index == 2:  # to choose an item from inventory
            player.choose_item()
            item_choice = int(input("Choose item:")) - 1

            if item_choice == -1:  # if no item is selected
                continue

            item = player.item[item_choice]["items"]  # this is what is used in game.py in the for loop
            #to tell the player when the stock is over
            if player.item[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left." + bcolors.ENDC)
                continue

            player.item[item_choice]["quantity"] -= 1
            #to reduce the inventory of the chosen item by 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for ", str(item.prop), " HP." + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "Mega Elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.get_max_hp()
                    player.mp = player.get_max_mp()
                print(bcolors.OKGREEN + "\n" + item.name + " Fully restores HP/MP" + bcolors.ENDC)
            
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals ", str(item.prop), " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]


        else:
            continue


    #automating enemy attacks
    for enemy in enemies:
        enemy_choice = 0 #random.randrange(0, 2)
        if enemy_choice == 0: #Enemy choosing attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for " + str(enemy_dmg))
            players[target].take_damage(enemy_dmg)

        elif enemy_choice == 1: #Enemy choosing magic
            magic_dmg = enemy.choose_enemy_spell()
            #enemy.reduce_mp(spell.cost)
            #enemies do not reduce MP, cause we're not counting MP

            #Based on enemies choice of magic
            #magic_dmg = enemy.choose_enemy_spell()
            target = random.randrange(0, 3)
            players[target].take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + " 's" + " deals ", str(magic_dmg),
                      "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has died.")
                del players[target]

    # When an enemy/player dies
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if battle is over
    if defeated_enemies == 2:  # Check if player won
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:  #Check if player lost
        print(bcolors.FAIL + bcolors.BOLD + " Your enemies have defeated you!" + bcolors.ENDC)
        running = False
