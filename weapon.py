
class Weapon:
    def __init__(self, name, range, s, ap, types):
        self.name = name

        # stats
        self.range = range
        self.strength = s
        self.armour_piercing = ap
        self.types= types

    # method to determine number of shots given distance
    # doubles as range check
    def shots(self, distance):
        if distance < self.range:
            for type in self.types:
                if type == "rapid fire":
                    if (float(distance) <( self.range / 2.0)):
                        return 2

                separated = type.split(" ")

                if (int(separated[1])):
                    return int(separated[1])

            return 1;

        else:
            return 0;

    def print_statline(self):
        name_length = len(self.name)
        header = (" " * name_length) + " Range S  AP Type\n"
        statline = self.name + " "

        # compensate for ranges < 100
        if self.range < 100:
            statline += " "
        statline += str(self.range) + "\"" + "  "

        # handle D and X weapons
        if self.strength == 11:
            statline += "D"
        elif self.strength == 0:
            statline == "X"
        else:
            statline += str(self.strength)

        # compensate for Strength 10
        if self.strength != 10:
            statline += " "

        statline += " "

        # handle AP -
        if self.armour_piercing == 7:
            statline += "-"
        else:
            statline += str(self.armour_piercing)

        statline += "  "

        # prepare for multiple types
        multiple = False
        statline_length = len(statline)

        # add types
        for type in self.types:
            if multiple:
                statline += ",\n" + (" " * statline_length)
            statline += type
            multiple = True

        return header + statline




