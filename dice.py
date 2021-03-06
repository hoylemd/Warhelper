import random
import math

class d6:
    def __init__(self, number, test):
        self.number = number
        self.test = test

    def roll(self):
        results = {'passes': 0, 'fails': 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        floored = int(math.floor(self.number))

        for i in range(0, floored):
            roll = random.randint(1, 6)
            results[roll] += 1

            if roll >= self.test:
                results['passes'] += 1
            else:
                results['fails'] += 1

        return results;

    def stat(self):
        p = (7.0 - float(self.test)) / 6.0

        return float(self.number) * p

