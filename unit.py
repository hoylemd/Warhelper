import model_profile

class Unit:
    def __init__(self, name, type):
        self.name = name
        self.models = []
        self.leader = None
        self.type = type

    def addModel(self, model, count):
        record = {'profile': model, 'count': count}
        self.models.append(record)

        if self.leader:
            if model.leadership > self.leader['profile'].leadership:
                self.leader = record
        else:
            self.leader = record

        # expire the wargear and rule lists
        self.wargear = None
        self.rules = None

    def print_feature_list(self, feature_list):
        string = ""

        # if the lists have been expired, recreate them
        if feature_list == None:
            self.compose_feature_lists()

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
        string += self.print_feature_list(self.wargear)

        # print rules
        string += "Special Rules:\n"
        if not hasattr(self, 'rules'):
            self.compose_feature_lists();
        string += self.print_feature_list(self.rules)

        return string
    def clone(self):
        new = Unit(self.name)
        for model in self.models:
            new.addModel(model['profile'], model['count'])

        return new
