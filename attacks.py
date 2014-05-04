import dice

class WoundingAttack:
    def __init__(self, number, hit, wound, weapon, cover_save=0):
        self.number = number
        self.hit = hit
        self.wound = wound
        self.weapon = weapon
        self.cover_save = cover_save

        # attributes to log hits and wounds
        self.hits = None
        self.wounds = None

    def __repr__(self):
        string = "Wounding attack ("
        string += str(self.number) + " attacks, "
        string += str(self.hit) + "+ to hit, "
        string += str(self.wound) + "+ to wound)"

        if self.hits and self.wounds:
            string += "\n  " + str(self.hits['passes']) + " hits, "
            string += str(self.wounds['passes']) + " wounds.\n"

        return string

    def roll(self):
        """Roll the dice for this attack, returning a dict:
            hits: dict of hit results
            wounds: dict of wound results

            Also stores the results in self.hits and self.wounds
        """

        hits = dice.d6(self.number, self.hit).roll()

        self.hits = hits

        wounds = dice.d6(hits['passes'], self.wound).roll()

        self.wounds = wounds

        return {'hits': hits, 'wounds': wounds}

    def stat(self):
        hits = dice.d6(self.number, self.hit).stat();
        wounds = dice.d6(hits, self.wound).stat();

        return {'hits': hits, 'wounds': wounds}

def roll_to_wound(strength, toughness):
    difference = strength - toughness
    if difference > 1:
        return 2
    if difference == 1:
        return 3
    if difference == 0:
        return 4
    if difference == -1:
        return 5
    if difference > -4:
        return 6
    else:
        return 0

