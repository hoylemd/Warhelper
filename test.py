import random;
import dice;
import math;

if __name__ == "__main__":
    five_space_marines_rapid_fire_bolters = dice.d6(10, 3);

    expected_marines_shots = {'passes': 7, 2: 1, 3: 2, 4: 2, 5: 3, 6: 0, 1: 2};

    random.seed(552);

    shots = five_space_marines_rapid_fire_bolters.roll();
    print shots == expected_marines_shots;

    expected = five_space_marines_rapid_fire_bolters.stat();

    print abs(expected - 6.6666666) < 0.000005;

