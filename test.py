import dice;

if __name__ == "__main__":
    five_space_marines_rapid_fire_bolters = dice.d6(10, 3);

    print five_space_marines_rapid_fire_bolters.roll();
    print five_space_marines_rapid_fire_bolters.stat();

