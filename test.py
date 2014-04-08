import random
import math
import dice
import attacks
from wargear import Wargear as Wargear
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

def test_boltgun():
    boltgun = Weapon("Boltgun", 24, 4, 5, ["rapid fire"])
    expected  = "        Range S  AP Type\n"
    expected += "Boltgun  24\"  4  5  rapid fire"

    output = boltgun.print_statline()

    result = output == expected

    if not result:
        print "expected:"
        print expected
        print output
        print "^- output"

    return result

def test_plasmagun():
    weapon = Weapon("Plasmagun", 24, 7, 2, ["rapid fire", "gets hot"])
    expected  = "          Range S  AP Type\n"
    expected += "Plasmagun  24\"  7  2  rapid fire,\n"
    expected += "                      gets hot"

    output = weapon.print_statline()

    result = output == expected

    if not result:
        print "expected:"
        print expected
        print output
        print "^- output"

    return result

def test_power_armour():
    power_armour = Wargear("Power Armour", "3+ armour save")
    expected_name = "Power Armour"
    expected_description = "3+ armour save"

    result = (power_armour.name == expected_name)
    result = result and (power_armour.description == expected_description)

    if not result:
        print power_armour.name + "/" + expected_name
        print power_armour.description + "/" + expected_description

    return result

and_they_shall_know_no_fear = None
combat_squads = None
chapter_tactics = None
def test_special_rule():
    return true

def test_model_profile():
    space_marine = ModelProfile("Space Marine", 4, 4, 4, 4, 1, 4, 1, 8, 3)
    space_marine.addWargear(Weapon("Boltgun", 24, 4, 5, ["rapid fire"]), "weapon")
    space_marine.addWargear(Weapon("Bolt Pistol", 12, 4, 5, ["pistol"]), "weapon")
    space_marine.addWargear(Wargear("Power Armour", "3+ armour save"), "wargear")
    space_marine.addWargear(Wargear("Frag and Krak grenades", "Assault and krag grenades"),
        "wargear")
    space_marine.addSpecialRule(SpecialRule("And They Shall Know No Fear",
        "Automatic regroup, No sweeping advances"))
    space_marine.addSpecialRule(SpecialRule("Combat Squads",
        "10-man squads may separate into 2 5-man squads at deployment"))
    space_marine.addSpecialRule(SpecialRule("Chapter Tactics",
        "Special rules per chapter"))

    #expected profile
    expected =  "             WS BS S  T  W  I  A  Ld Sv\n"
    expected += "Space Marine 4  4  4  4  1  4  1  8  3+\n"
    expected += "Wargear:\n"
    expected += "  Boltgun\n"
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
    print test_boltgun();
    print "test plasmagun:",
    print test_plasmagun();
    print "test power armour:",
    print test_power_armour()
    print "test model profile:",
    print test_model_profile();

