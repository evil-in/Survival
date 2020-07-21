import random
from .magic import Spell
import pprint
from .inventory import item

class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, item):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.item = item
        self.actions = ["Attack", "Magic", "Items"]


    def generate_damage(self):
        r = random.randrange(self.atkl, self.atkh)
        return r


    def generate_spelldamage(self, i):
        mgl = self.magic[i]["dmg"] - 5
        mgh = self.magic[i]["dmg"] + 5
        return random.randrange(mgl, mgh)


    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
            return self.hp


    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.get_max_hp():
            self.hp = self.get_max_hp()
            #restores full health


    def get_hp(self):
        return self.hp


    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp


    def get_max_mp(self):
        return self.maxmp


    def reduce_mp(self, cost):
        self.mp -= cost


    def get_spell_mp_cost(self, i):
        return self.magic[i]["cost"]


    def choose_action(self):
        i = 1
        print("\n" + bcolors.BOLD + self.name + bcolors.ENDC)
        print( "\n    " + bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS!" + bcolors.ENDC)
        for item in self.actions:
            print(str(i) + ":", item)
            i +=1


    def choose_magic(self):
        i = 1

        print( "\n    " + bcolors.OKBLUE + bcolors.BOLD + "    MAGIC!" + bcolors.ENDC)
        for spell in self.magic:
            print(str(i) + ":", spell.name, ["cost:", str(spell.cost)])
            i += 1


    def choose_item(self):
        i = 1
        print("\n    " + bcolors.OKGREEN + bcolors.BOLD + "    ITEMS!" + bcolors.ENDC)
        for item in self.item:
            print(str(i) + ".", item["items"].name + ":", item["items"].description,
                  " (x" + str(item["quantity"]) + ")")
            i += 1


    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp():
                print("        " + str(i) + "." + enemy.name)
                i += 1

        choice = int(input("    Choose target:")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = " "
        bar_ticks = (self.hp/self.maxhp) * 100 / 2
        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "


        #code of adding whitespace
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = " "

        if len(hp_string) < 11:
            decreased = 7 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print(bcolors.BOLD + self.name + "                      " +
              current_hp + "|" + bcolors.FAIL + hp_bar + bcolors.ENDC +  "|")

    def get_stats(self):  # The character dashboard with HP/MP view
        #to create a working HP bar
        hp_bar = " "
        hp_bar_ticks = (self.hp/self.maxhp) * 100 /4
        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        #to create a working MP bar
        mp_bar = " "
        mp_bar_ticks = (self.mp / self.maxmp) * 100 / 10
        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        #to add whitspace to HP bar
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = " "

        if len(hp_string) < 7: #cox hp_string is 7 characters long
            decreased = 7 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        #whitespace for MP
        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = " "

        if len(mp_string) < 7:
            dec = 7 - len(mp_string)
            while dec >0:
                current_mp += " "
                dec -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        print(bcolors.BOLD + self.name + "                      " +
              current_hp + "|" + bcolors.OKGREEN + hp_bar + bcolors.ENDC +
              "|         "+ current_mp + "|" + bcolors.OKBLUE + mp_bar + "|" + bcolors.ENDC)


    def choose_enemy_spell(self):
        spell = ""
        magic_dmg = 0
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        #magic_dmg = spell.generate_spelldamage[magic_choice]
        if spell == "Fire":
            magic_dmg = 100
        elif spell == "Meteor":
            magic_dmg = 200
        elif spell == "Quake":
            magic_dmg = 240

        return magic_dmg



