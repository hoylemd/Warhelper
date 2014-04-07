import random
import math
import dice
import attacks
from weapon import Weapon as Weapon
from model_profile import ModelProfile as ModelProfile
from special_rules import SpecialRule as SpecialRule

def close_enough(a, b):
    return abs(a - b) < 0.0000005

def test_d6():
    # test object
    rolls = dice.d6(10, 3)

    # expected
    expected_roll = {'passes': 7, 2: 1, 3: 2, 4: 2, 5: 3, 6: 0, 1: 2}
    expected_stat = 6.6666666

    # roll test
    roll = rolls.roll()
    roll_result = roll == expected_roll

    # stat test
    stat = rolls.stat()
    stat_result = close_enough(stat, expected_stat)

    return roll_result and stat_result

def test_wounding_attack():
    # test object
    attack = attacks.wounding_attack(10, 3, 3)

    # expected
    expected_roll = {'passes': 6, 2: 1, 3: 2, 4: 0, 5: 0, 6: 4, 1: 1, 'hits': 8}
    expected_stat = 4.44444444444

    # roll test
    roll = attack.roll();
    roll_result = roll == expected_roll

    # stat test
    stat = attack.stat()
    stat_result = close_enough(stat, expected_stat)

    return roll_result and stat_result;

bolter = None
bolt_pistol = None
def test_weapon():
    bolter = Weapon("Boltgun", 24, 4, 5, ["rapid fire"])
    expected  = "        Range S  AP Type\n"
    expected += "Boltgun  24\"  4  5  rapid fire"

    output = bolter.print_statline()

    result = output == expected

    if not result:
        print "expected:"
        print expected
        print output
        print "^- output"

    return result

power_armor = None
frag_and_krak_grenades = None
def test_wargear():
    return true

and_they_shall_know_no_fear = None
combat_squads = None
chapter_tactics = None
def test_special_rule():
    return true

def test_model_profile():
    space_marine = ModelProfile("Space Marine", 4, 4, 4, 4, 1, 4, 1, 8, 3)

    #expected profile
    expected =  "             WS BS S  T  W  I  A  Ld Sv\n"
    expected += "Space Marine 4  4  4  4  1  4  1  8  3+\n"
    expected += "Wargear:\n"
    expected += "  Bolter\n"
    expected += "  Bolt Pistol\n"
    expected += "  Power Armour\n"
    expected += "  Frag and Krak grenades\n"
    expected += "Special Rules:\n"
    expected += "  And They Shall Know No Fear\n"
    expected += "  Combat Squads\n"
    expected += "  Chapter Tactics\n"

    output = space_marine.print_summary()
    result = output == expected

    if not result:
        print "expected:"
        print expected
        print output
        print "^- output"

    return result



if __name__ == "__main__":
    random.seed(552);

    print "test d6:",
    print test_d6();
    print "test wounding attack:",
    print test_wounding_attack();
    print "test weapons:",
    print test_weapon();
    print "test model profile:",
    print test_model_profile();

