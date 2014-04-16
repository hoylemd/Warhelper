
statline_header = "WS BS S  T  W  I  A  Ld Sv"

class ModelProfile:
    def __init__(self, name, ws, bs, s, t, w, i, a, ld, sv):
        self.name = name

        # stats
        self.weapon_skill = ws
        self.ballistic_skill = bs
        self.strength = s
        self.toughness = t
        self.wounds = w
        self.initiative = i
        self.attacks = a
        self.leadership = ld
        self.save = sv

        # lists
        self.wargear = []
        self.weapons = []
        self.rules = []

    def __repr__(self):
        return "ModelProfile(" + self.name + ")"

    def get_statline(self):
        string = str(self.weapon_skill) + " "
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


    def print_statline(self):
        name_length = len(self.name)
        string = (" " * name_length) + " " + statline_header + "\n"
        string += self.name + " " + self.get_statline()

        return string

    def print_summary(self):
        # statline
        string = self.print_statline() + "\n"

        # wargear
        string += "Wargear:\n"
        for thing in self.wargear:
            string += "  " + thing.name + "\n"

        # special rules
        string += "Special Rules:\n"
        for rule in self.rules:
            string += "  " + rule.name + "\n"

        return string

    def addWargear(self, item, type = None):
        self.wargear.append(item)

        if type == "weapon":
            self.weapons.append(item)

    def addSpecialRule(self, rule):
        self.rules.append(rule)
