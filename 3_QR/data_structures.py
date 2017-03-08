class Element:
    name = ""
    value = 0
    maxValue = 0
    derivative = 0

    def __init__(self, name, value, maxValue, derivative):
        self.name = name
        self.value = value
        self.maxValue = maxValue
        self.derivative = derivative

    def print(self):
        print(self.name + "=" + str(self.value) + "," + str(self.derivative))

    def __hash__(self):
        return hash(self.name) ^ hash(self.value) ^ hash(self.maxValue) ^ hash(self.derivative)

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value and self.maxValue == other.maxValue and self.derivative == other.derivative


class Influence:
    type = "Influence"
    element1 = 0
    element2 = 0
    relation_type = 0

    def __init__(self, element1, element2, relation_type):
        self.element1 = element1
        self.element2 = element2
        self.relation_type = relation_type

    def toString(self):
        return "i" + str(self.element1) + str(self.element2)


class Proportionality:
    type = "Proportionality"
    element1 = 0
    element2 = 0
    relation_type = 0

    def __init__(self, element1, element2, relation_type):
        self.element1 = element1
        self.element2 = element2
        self.relation_type = relation_type

    def toString(self):
        return "p" + str(self.element1) + str(self.element2)


class ValueConstraint:
    element1 = 0
    element2 = 0

    def __init__(self, element1, element2):
        self.element1 = element1
        self.element2 = element2


class QuantityConstraint:
    element1 = 0
    element2 = 0

    def __init__(self, element1, element2):
        self.element1 = element1
        self.element2 = element2
