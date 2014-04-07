import random
import math
import dice
import attacks
from model_profile import ModelProfile as ModelProfile

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

def test_model_profile():
    space_marine = ModelProfile(4, 4, 4, 4, 1, 4, 1, 8, 3)

    #expected profile
    expected = "WS BS S  T  W  I  A  Ld Sv\n4  4  4  4  1  4  1  8  3+"

    return space_marine.print_statline() == expected;


if __name__ == "__main__":
    random.seed(552);

    print "test d6:",
    print test_d6();
    print "test wounding attack:",
    print test_wounding_attack();
    print "test model profile:",
    print test_model_profile();

