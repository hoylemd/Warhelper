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

    def print_summary(self):
        string = ""

        string += self.name + "\n"

        statlines = {}
        for record in self.models:
            model = record['profile']
            statlines[model.name] = model.get_statline()

        # determine offset for statlines
        # print stat header
        # print statlines
        for profile in statlines:
            string += profile + " " + statlines[profile] + "\n"
        # print type
        # print compisition
        # print wargear

        return string
    def clone(self):
        new = Unit(self.name)
        for model in self.models:
            new.addModel(model['profile'], model['count'])

        return new
