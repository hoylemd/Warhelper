import random;

class d6:
    def __init__(self, number, test):
        self.number = number
        self.test = test

    def roll(self):
        results = {'passes': 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0};

        for i in range(0, self.number):
            roll = random.randint(1, 6);
            results[roll] += 1;

            if roll >= self.test:
                results['passes'] += 1;

        return results;

    def stat(self):
        p = float(self.test - 1) / 6.0;

        return float(self.number) * p;
