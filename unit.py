import math
import dice
import model_profile
import attacks

class NullModelException(Exception):
    def __repr__(self):
        "Null model passed - you must specify a model profile to add to a unit."

class Unit:
    def __init__(self, name, type):
        self.name = name
        self.models = []
        self.leader = None
        self.type = type
        self.alive = False

    # method to determine the leader for the unit
    def chooseLeader(self):
        """Read the model list and assigned the one with the highest Ld to the leader attribute"""
        best = None

        for record in self.models:
            if best:
                if record['profile'].leadership > best['profile'].leadership:
                    best = record
            else:
                best = record

        self.leader = best

    def addModel(self, model, count):
        # check that a model was passed
        if (model == None):
            raise NullModelException

        # mark this unit as alive
        self.alive = True

        record = {'profile': model, 'count': count, 'wounds': 0}
        self.models.append(record)

        # choose the new leader
        self.chooseLeader()

        # expire the wargear and rule lists
        self.wargear = None
        self.rules = None

    def destroy(self):
        """Handle the event of a unit being wiped out"""

        self.alive = False

    # method to remove a model record
    def removeModel(self, model):
        """Remove a provided model record.
            Calls the destroy handler or leader chooser as appropriate.
        """
        # remove the model
        self.models.remove(model)

        # call death method if this unit is destroyed
        if len(self.models) == 0:
            self.destroy()
        else:
            # otherwise, find the new leader
            self.chooseLeader()

    def count_members(self):
        """Count the total members of the unit"""
        count = 0
        for record in self.models:
            count += record['count']

        return count

    def print_feature_list(self, feature_list_name):
        string = ""

        feature_list = None

        if feature_list_name == "wargear":
            feature_list = self.wargear
        elif feature_list_name == "rules":
            feature_list = self.rules
        else:
            raise Exception(
                "Invalid feature list (" + feature_list_name + "). must be 'wargear' or 'rules'");

        # if the lists have been expired, recreate them, and recurse
        if feature_list == None:
            self.compose_feature_lists()
            return self.print_feature_list(feature_list_name);

        for item in feature_list:
            string += "  " + item
            if len(feature_list[item]) < len(self.models):
                string += "("
                subsequent = False
                for profile in feature_list[item]:
                    if subsequent:
                        string += ", "
                    else:
                        subsequent = True
                    string += profile.name
                string += " only)"
            string += "\n"
        return string

    def compose_feature_lists(self):
        wargear = {}
        rules = {}
        for record in self.models:
            model_gear = record['profile'].wargear

            for item in model_gear:
                if item.name in wargear.keys():
                    wargear[item.name].append(record['profile'])
                else:
                    wargear[item.name] = [record['profile']]

            model_rules = record['profile'].rules
            for rule in model_rules:
                if rule.name in rules.keys():
                    rules[rule.name].append(record['profile'])
                else:
                    rules[rule.name] = [record['profile']]

        self.wargear = wargear
        self.rules = rules

    def print_summary(self):
        string = ""

        # unit name
        string += self.name + "\n"

        statlines = {}
        offset = 0;
        for record in self.models:
            model = record['profile']
            statlines[model.name] = model.get_statline()
            # determine longest profile name
            if len(model.name) > offset:
                offset = len(model.name)

        # print statlines
        string += (" " * (offset + 1)) + model_profile.statline_header + "\n"
        for profile in statlines:
            string += profile
            # align the statlines
            string += " " * (offset - len(profile))
            string += " " + statlines[profile] + "\n"

        # print type
        string += "Unit Type: " + self.type + "\n"

        # print composition
        string += "Unit Composition:\n"
        for record in self.models:
            string += "  " + str(record['count']) + " " + record['profile'].name + "\n"

        # print wargear
        string += "Wargear:\n"
        if not hasattr(self, 'wargear'):
            self.compose_feature_lists();
        string += self.print_feature_list("wargear")

        # print rules
        string += "Special Rules:\n"
        if not hasattr(self, 'rules'):
            self.compose_feature_lists();
        string += self.print_feature_list("rules")

        return string

    def get_majority_toughness(self):
        majority = None
        for record in self.models:
            if not majority:
                majority = record
            else:
                if record['count'] > majority['count']:
                    majority = record
                elif record['count'] == majority['count']:
                    if record['profile'].toughness > majority['profile'].toughness:
                        majority = record

        return majority['profile'].toughness

    def take_wounds(self, attack):
        """ Take saves on inflicted wounds, apply wounds, and remove casualties

        Arguments:
            attack: a WoundingAttack object describing the attack

        Returns:
            the total number of unsaved wounds suffered by the unit
        """

        unsaved = 0
        remaining_wounds = attack.wounds['passes']

        while remaining_wounds and self.alive:
            # determine the number of wounds we can roll for now
            model = self.models[0]
            wounds_to_take = remaining_wounds
            wounds_characteristic = model['profile'].wounds
            max_wounds = model['count'] * wounds_characteristic - model['wounds'];
            if wounds_to_take > max_wounds:
                wounds_to_take = max_wounds
            remaining_wounds -= wounds_to_take

            save = model['profile'].best_save(attack)

            # roll the dice
            roll = dice.d6(wounds_to_take, save).roll()

            # inflict casualties
            casualties = roll['fails']
            unsaved += casualties
            # handle wounded models first
            if model['wounds']:
                to_go = wounds_characteristic - model['wounds']
                if casualties >= to_go:
                    model['wounds'] = 0
                    model['count'] -= 1
                else :
                    model['wounds'] += to_go

                casualties -= to_go

            # handle further casualties
            if casualties:
                model['count'] -= math.floor(casualties / model['profile'].wounds)

                # add leftover wounds
                model['wounds'] = casualties % model['profile'].wounds

            # remove eradicated models
            if model['count'] < 1:
                self.removeModel(model)

        return unsaved

    # generates a dict of attacks versus a target unit
    def attack(self, target, weapons, range):
        tests = {}

        # initialize the dict
        for weapon in weapons:
            tests[weapon] = []

        for record in self.models:
            profile = record['profile']
            this_attack = None
            i = 0

            # find the highest-priority weapon for this model
            while (this_attack == None and i < len(weapons)):
                weapon = weapons[i]
                for held_weapon in profile.weapons:
                    if held_weapon.name == weapon:

                        # determine hit roll
                        hit_roll = 7 - profile.ballistic_skill

                        # determine wound roll
                        wound_roll = attacks.roll_to_wound(
                            held_weapon.strength,
                            target.get_majority_toughness());
                        # build the attack object
                        this_attack = attacks.WoundingAttack(
                            held_weapon.shots(range) * record['count'],
                            hit_roll,
                            wound_roll,
                            held_weapon)
                        tests[weapon].append(this_attack)
                i += 1

        return tests

    def stat_wounds(self, attack):
        ''' calculate casualty statistics of this attack '''

        remaining_wounds = attack.stat()['wounds']
        model = self.models[0]
        save = model['profile'].best_save(attack)

        return remaining_wounds - dice.d6(remaining_wounds, save).stat()

    def clone(self):
        '''
        clone this unit profile
        '''
        new = Unit(self.name)
        for model in self.models:
            new.addModel(model['profile'], model['count'])

        return new
