import dice

class wounding_attack:
    def __init__(self, number, hit, wound):
        self.number = number
        self.hit = hit
        self.wound = wound

    def roll(self):
        hits = dice.d6(self.number, self.hit).roll()

        hits = hits['passes'];

        wounds = dice.d6(hits, self.wound).roll();

        return wounds;

    def stat(self):
        hits = dice.d6(self.number, self.hit).stat();

        return dice.d6(hits, self.wound).stat();


