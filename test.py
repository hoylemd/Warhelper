import random
import math
import dice
import attacks
from wargear import Wargear as Wargear
from weapon import Weapon as Weapon
from special_rules import SpecialRule as SpecialRule
from model_profile import ModelProfile as ModelProfile
from unit import *

def close_enough(a, b):
    res = abs(a - b)

    if res < 0.005:
        return True
    else:
#        print res
        return False


def test_d6():
    # test object
    rolls = dice.d6(10, 3)

    # expected
    expected_roll = {'passes': 7, 'fails': 3, 2: 1, 3: 2, 4: 2, 5: 3, 6: 0, 1: 2}
    expected_stat = 6.6666666

    # roll test
    roll = rolls.roll()
    roll_result = roll == expected_roll

    # stat test
    stat = rolls.stat()
    stat_result = close_enough(stat, expected_stat)

    return roll_result and stat_result

def test_WoundingAttack():
    # test object
    attack = attacks.WoundingAttack(10, 3, 3, None)

    # expected
    expected_roll = {
        'hits': {'passes': 8, 'fails': 2, 2: 0, 3: 2, 4: 2, 5: 1, 6: 3, 1: 2},
        'wounds': {'passes': 6, 'fails': 2, 2: 1, 3: 2, 4: 0, 5: 0, 6: 4, 1: 1}
    }
    expected_stat = {
        'hits': 6.6666,
        'wounds': 4.4444
    }

    # roll test
    roll = attack.roll()
    roll_result = roll == expected_roll

    # stat test
    stat = attack.stat()
    stat_result = (close_enough(stat['hits'], expected_stat['hits']) and
        close_enough(stat['wounds'], expected_stat['wounds']))

    result = roll_result and stat_result

    if not result:
        message = "False\n"

        message += "  Roll: expected: " + str(expected_roll) + ", got: " + str(roll) + "\n"
        message += "  Stat: expected: " + str(expected_stat) + ", got: " + str(stat)
    else:
        message = "True"

    return message

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

def test_special_rule():
    return True

def make_space_marine():
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

    return space_marine

def test_model_profile():
    space_marine = make_space_marine()

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

def test_armour_save():
    model = make_space_marine()
    expected = 3

    # ape a lasgun attack
    attack = attacks.WoundingAttack(1, 4, 5, Weapon("Lasgun", 24, 3, 0, ["rapid fire"]))

    output = model.best_save(attack)
    result = output == expected

    return result

def test_cover_save():
    model = make_space_marine()
    expected = 5

    # ape a hot shot lasgun attack
    attack = attacks.WoundingAttack(1, 4, 5, Weapon("Hot-Shot Lasgun", 24, 3, 3, ["rapid fire"]), 5)

    output = model.best_save(attack)
    result = output == expected

    if not result:
        message = "False\n"
        message += "  expected: " + str(expected) + " got: " + str(output)
    else:
        message = "True"

    return message

def tactical_squad():
    marine = make_space_marine()
    sergeant = ModelProfile("Space Marine Sergeant", 4, 4, 4, 4, 1, 4, 1, 8, 3)
    sergeant.addWargear(Weapon("Close Combat Weapon", 0, 4, 0, ["melee"]), "weapon")
    sergeant.addWargear(Weapon("Bolt Pistol", 12, 4, 5, ["pistol"]), "weapon")
    sergeant.addWargear(Wargear("Power Armour", "3+ armour save"), "wargear")
    sergeant.addWargear(Wargear("Frag and Krak grenades", "Assault and krag grenades"),
        "wargear")
    sergeant.addSpecialRule(SpecialRule("And They Shall Know No Fear",
        "Automatic regroup, No sweeping advances"))
    sergeant.addSpecialRule(SpecialRule("Combat Squads",
        "10-man squads may separate into 2 5-man squads at deployment"))
    sergeant.addSpecialRule(SpecialRule("Chapter Tactics",
        "Special rules per chapter"))

    unit = Unit("Space Marine Tactical Squad", "infantry")
    unit.addModel(marine, 9)
    unit.addModel(sergeant, 1)

    return unit

def make_guardsman():
    guardsman = ModelProfile("Guardsman", 3, 3, 3, 3, 1, 3, 1, 7, 5)
    guardsman.addWargear(Weapon("Lasgun", 24, 3, 0, ["rapid fire"]), "weapon")
    guardsman.addWargear(Wargear("Flak Armour", "5+ armour save"), "wargear")
    guardsman.addWargear(Wargear("Frag grenades", "Assault grenades"),
        "wargear")
    guardsman.addSpecialRule(SpecialRule("Combined Squad",
        "Units with this rule may choose to merge into a single unit at deployment."))
    return guardsman

def make_guard_sergeant():
    sergeant = ModelProfile("Guardsman", 3, 3, 3, 3, 1, 3, 2, 8, 5)
    sergeant.addWargear(Weapon("Close Combat Weapon", 0, 3, 0, ["melee"]), "weapon")
    sergeant.addWargear(Weapon("Laspistol", 12, 3, 0, ["pistol"]), "weapon")
    sergeant.addWargear(Wargear("Flak Armour", "5+ armour save"), "wargear")
    sergeant.addWargear(Wargear("Frag grenades", "Assault grenades"),
        "wargear")
    sergeant.addSpecialRule(SpecialRule("Combined Squad",
        "Units with this rule may choose to merge into a single unit at deployment."))
    return sergeant

def guard_blob():
    guardsman = make_guardsman()
    sergeant = make_guard_sergeant()

    unit = Unit("Imperial Guard Infantry Blob", "infantry")
    unit.addModel(guardsman, 27)
    unit.addModel(sergeant, 3)

    return unit

def test_unit():
    unit = tactical_squad()

    expected = "Space Marine Tactical Squad\n"
    expected += "                      WS BS S  T  W  I  A  Ld Sv\n"
    expected += "Space Marine Sergeant 4  4  4  4  1  4  1  8  3+\n"
    expected += "Space Marine          4  4  4  4  1  4  1  8  3+\n"
    expected += "Unit Type: infantry\n"
    expected += "Unit Composition:\n"
    expected += "  9 Space Marine\n"
    expected += "  1 Space Marine Sergeant\n"
    expected += "Wargear:\n"
    expected += "  Frag and Krak grenades\n"
    expected += "  Boltgun(Space Marine only)\n"
    expected += "  Close Combat Weapon(Space Marine Sergeant only)\n"
    expected += "  Bolt Pistol\n"
    expected += "  Power Armour\n"
    expected += "Special Rules:\n"
    expected += "  And They Shall Know No Fear\n"
    expected += "  Combat Squads\n"
    expected += "  Chapter Tactics\n"

    output = unit.print_summary()
    result = output == expected

    return result

def test_null_model():
    unit = Unit("No models!", "infantry")
    try:
        unit.addModel(None, 5)
    except NullModelException as e:
        return True

    return False

def unit_shooting(unit, target, weapons, range, expected):
    string = ""
    firing = unit.attack(target, weapons, range)
    ok = True

    for weapon in firing:
        string += weapon + ": \n"
        expected_stat = expected['stat'][weapon]
        expected_roll = expected['roll'][weapon]

        for model in firing[weapon]:
            sample_stat = model.stat()
            sample_roll = model.roll()
            unsaved_roll = target.take_wounds(model)
            unsaved_stat = target.stat_wounds(model)

            string += "  " + repr(model) + "\n"

            stat_ok = ((close_enough(sample_stat['hits'], expected_stat['hits']))
                and (close_enough(sample_stat['wounds'], expected_stat['wounds']))
                and (close_enough(unsaved_stat, expected_stat['unsaved'])))

            if stat_ok:
                string += "  stat OK\n"
            else:
                string += "  stat Wrong:\n"
                string += "   hits: " + str(sample_stat['hits']) + " output, "
                string += str(expected_stat['hits']) + " expected\n"
                string += "   wounds: " + str(sample_stat['wounds']) + " output, "
                string += str(expected_stat['wounds']) + " expected\n"
                string += "   unsaved: " + str(unsaved_stat) + " output, "
                string += str(expected_stat['unsaved']) + " expected\n"

            roll_ok = ((sample_roll['hits']['passes'] == expected_roll['hits'])
                and (sample_roll['wounds']['passes'] == expected_roll['wounds'])
                and (unsaved_roll == expected_roll['unsaved']))

            if roll_ok:
                string += "  roll OK\n"
            else:
                string += "  roll Wrong:\n"
                string += "   hits: " + str(sample_roll['hits']) + " output, "
                string += str(expected_roll['hits']) + " expected\n"
                string += "   wounds: " + str(sample_roll['wounds']) + " output, "
                string += str(expected_roll['wounds']) + " expected\n"
                string += "   unsaved: " + str(unsaved_roll) + " output, "
                string += str(expected_roll['unsaved']) + " expected\n"

        expected_survivors = expected['roll']['survivors']

        ok = ok and stat_ok and roll_ok

    survivors_ok = target.count_members() == expected_survivors
    if survivors_ok:
        string += "  casualties OK\n"
    else:
        string += "  casualties Wrong:\n"
        string += "   " + str(target.count_members()) + " output, "
        string += str(expected_survivors) + " expected\n"

    return {'result': ok and survivors_ok, 'output': string}

def test_shooting_attack():
    result = True
    expected = {
        'tac_squad': {
            'stat' : {
                'Boltgun' : {'shots': 18, 'hits': 12, 'wounds': 8, 'unsaved': 8},
                'Bolt Pistol' : {'shots': 1, 'hits': 0.6666, 'wounds': 0.4436, 'unsaved': 0.4436},
                'survivors' : 21.564
                },
            'roll' : {
                'Boltgun' : {'shots': 18, 'hits': 12, 'wounds': 8, 'unsaved': 8},
                'Bolt Pistol' : {'shots': 1, 'hits': 0, 'wounds': 0, 'unsaved': 0},
                'survivors' : 22
                },
            },
        'blob': {
            'stat' : {
                'Lasgun' : {'shots': 38, 'hits': 19, 'wounds': 6.3333, 'unsaved': 2.1111},
                'Laspistol' : {'shots': 3, 'hits': 1.5, 'wounds': 0.5, 'unsaved': 0.165},
                'survivors' : 7.766
                 },
            'roll' : {
                'Lasgun' : {'shots': 38, 'hits': 20, 'wounds': 7, 'unsaved': 4},
                'Laspistol' : {'shots': 3, 'hits': 0, 'wounds': 0, 'unsaved': 0},
                'survivors' : 6
                }
            }
        }

    string = ""
    tac_squad = tactical_squad()
    blob = guard_blob()
    tac_squad_result = unit_shooting(
        tac_squad, blob, ['Boltgun', 'Bolt Pistol'], 11, expected['tac_squad'])
    tac_squad_ok = tac_squad_result['result'];
    string += tac_squad_result['output'];

    blob_result = unit_shooting(
        blob, tac_squad, ['Lasgun', 'Laspistol'], 11, expected['blob'])
    blob_ok = blob_result['result'];
    string += blob_result['output'];

    result = tac_squad_ok and blob_ok

    return {'result': result, 'output': string}

if __name__ == "__main__":
    random.seed(552)

    print "test d6:",
    print test_d6()
    print "test wounding attack:",
    print test_WoundingAttack()
    print "test weapons:",
    print test_boltgun()
    print "test plasmagun:",
    print test_plasmagun()
    print "test power armour:",
    print test_power_armour()
    print "test model profile:",
    print test_model_profile()
    print "test unit:",
    print test_unit()
    print "test armour save:",
    print test_armour_save()
    print "test cover save:",
    print test_cover_save()
    print "test null model:",
    print test_null_model()
    # print test zero model count
    # print test leader
    print "test shooting attack:",
    test_shooting_result = test_shooting_attack()
    print test_shooting_result['result']
    if not test_shooting_result['result']:
        print test_shooting_result['output']

