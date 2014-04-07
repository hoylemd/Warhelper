
class ModelProfile:
    def __init__(self, ws, bs, s, t, w, i, a, ld, sv):
        self.weapon_skill = ws
        self.ballistic_skill = bs
        self.strength = s
        self.toughness = t
        self.wounds = w
        self.initiative = i
        self.attacks = a
        self.leadership = ld
        self.save = sv
        self.equipment = []

    def print_statline(self):
        string = "WS BS S  T  W  I  A  Ld Sv\n"
        string += str(self.weapon_skill) + " "
        string += " " + str(self.ballistic_skill) + " "
        string += " " + str(self.strength) + " "
        string += " " + str(self.toughness) + " "
        string += " " + str(self.wounds) + " "
        string += " " + str(self.initiative) + " "
        string += " " + str(self.attacks) + " "
        string += " " + str(self.leadership)
        if self.leadership < 10:
            string += " "
        string += " " + str(self.save) + "+"

        return string
