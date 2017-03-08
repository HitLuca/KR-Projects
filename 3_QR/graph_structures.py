class State:
    id = 0
    elements = 0

    def __init__(self, id, elements):
        self.id = id
        self.elements = elements

    def print(self):
        for element in self.elements:
            element.print()

    def __hash__(self):
        tot_hash = hash(self.id)
        for element in self.elements:
            tot_hash ^= hash(element)
        return tot_hash

    def __eq__(self, other):
        equal = self.id == other.id
        for i in range(len(self.elements)):
            equal = equal and self.elements[i] == other.elements[i]
        return equal


class Edge:
    state1_id = 0
    state2_id = 0

    def __init__(self, state1, state2):
        self.state1_id = state1
        self.state2_id = state2

    def print(self):
        print(str(self.state1_id) + "->" + str(self.state2_id))

    def toString(self):
        return str(self.state1_id) + "->" + str(self.state2_id)

    def __hash__(self):
        return hash(self.state1_id) ^ hash(self.state2_id)

    def __eq__(self, other):
        return self.state1_id == other.state1_id and self.state2_id == other.state2_id
