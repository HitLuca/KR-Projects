import os
from data_structures import Element
from graph_structures import State


def increaseDerivative(derivative):
    if derivative != 1:
        return derivative + 1
    else:
        return derivative


def decreaseDerivative(derivative):
    if derivative != -1:
        return derivative - 1
    else:
        return derivative


def increaseValue(value):
    return value + 1


def decreaseValue(value):
    return value - 1


def findElement(elements, name):
    for element in elements:
        if element.name == name:
            return element


def checkConstraint(constraint, state):
    element1 = findElement(state.elements, constraint.element1)
    element2 = findElement(state.elements, constraint.element2)
    return element1.value == element2.value


def checkStateEquality(state1, state2):
    equal = True
    for i in range(len(state1.elements)):
        if hash(state1.elements[i]) != hash(state2.elements[i]):
            equal = False
    return equal


def removeDuplicateStates(states):
    return list(set(states))


def generateStartingStates(scenario):
    state_counter = 1
    initial_states = []

    inflows = generateSinusoidalInflows()

    for inflow in inflows:
        temp_elements = copyElements(scenario.elements)
        temp_elements[0] = inflow
        state = State(state_counter, temp_elements)
        initial_states.append(state)
        state_counter += 1
    return initial_states, state_counter


def generateSinusoidalInflows():
    inflows = []
    for value in range(3):
        for derivative in range(-1, 2):
            if not ((value == 2 and derivative == 1) or (value == 0 and derivative == -1)):
                inflows.append(Element("I", value, 3, derivative))
    return inflows


def checkStateExistence(dict, other_state):
    for id, state in dict.items():
        equal = True
        for j in range(len(state.elements)):
            equal = equal and state.elements[j] == other_state.elements[j]
        if equal:
            return True, state
    return False, other_state


def checkEdgeExistence(edges, other_edge):
    for edge in edges:
        if edge == other_edge:
            return True, edge
    return False, other_edge


def checkDerivativeValidity(state):
    elements = state.elements
    return elements[1].derivative == elements[2].derivative == elements[3].derivative == elements[4].derivative


def checkStateValidity(state):
    valid = True
    for element in state.elements:
        if element.value == element.maxValue - 1 and element.derivative > 0:
            valid = False
        elif element.value == 0 and element.derivative < 0:
            valid = False
        elif element.value < 0:
            valid = False

    result = checkDerivativeValidity(state)

    return valid and result


def printState(state):
    print("###############################")
    print("Created state " + str(state.id))
    state.print()


def printEdge(edge):
    print("###############################")
    edge.print()


def checkEdgeValidity(state1, state2, states):
    state1 = states[state1]
    state2 = states[state2]
    immediate = False
    time = False
    for i in range(len(state1.elements)):
        if state1.elements[i].derivative != 0 and state2.elements[i].derivative != 0 and state1.elements[
            i].derivative != state2.elements[i].derivative:
            return False
        if state1.elements[i].value != state2.elements[i].value:
            if state1.elements[i].value % 2 == 0 and state2.elements[i].value % 2 != 0:
                immediate = True
            elif state1.elements[i].value % 2 != 0 and state2.elements[i].value % 2 == 0:
                time = True
        if state1.elements[i].derivative != state2.elements[i].derivative:
            if state1.elements[i].derivative % 2 == 0 and state2.elements[i].derivative % 2 != 0:
                immediate = True
            elif state1.elements[i].derivative % 2 != 0 and state2.elements[i].derivative % 2 == 0:
                time = True
        if time and immediate:
            return False
    return True


def copyState(state):
    elements = []
    for element in state.elements:
        elements.append(Element(element.name, element.value, element.maxValue, element.derivative))
    return State(state.id, elements)


def copyElements(elements):
    output = []
    for element in elements:
        output.append(Element(element.name, element.value, element.maxValue, element.derivative))
    return output


def writeTrace(states, edges):
    value_strings = ["0", "+", "max"]
    derivative_strings = ["neg", "zero", "pos"]

    with open("output/trace.dat", "w+") as f:
        for edge in edges:
            f.write("Transition " + edge.toString() + "\n")
            state1 = states[edge.state1_id]
            state2 = states[edge.state2_id]
            if state1.id == state2.id:
                f.write("\tNo changes\n")
            else:
                for i in range(len(state1.elements)):
                    if state1.elements[i].value != state2.elements[i].value:
                        if state1.elements[i].value % 2 == 0:
                            f.write("\tVal of " + state1.elements[i].name + ": Point to interval update (" +
                                  value_strings[state1.elements[i].value] + "," +
                                  value_strings[state2.elements[i].value] + ")\n")
                        else:
                            f.write("\tVal of " + state1.elements[i].name + ": Interval to point update (" +
                                  value_strings[state1.elements[i].value] + "," +
                                  value_strings[state2.elements[i].value] + ")\n")

                for i in range(len(state1.elements)):
                    if state1.elements[i].derivative != state2.elements[i].derivative:
                        if state1.elements[i].derivative % 2 == 0:
                            f.write("\tDer of " + state1.elements[i].name + ": Point to interval update (" +
                                  derivative_strings[
                                      state1.elements[i].derivative + 1] + "," + derivative_strings[
                                      state2.elements[i].derivative + 1] + ")\n")
                        else:
                            f.write("\tDer of " + state1.elements[i].name + ": Interval to point update (" +
                                  derivative_strings[
                                      state1.elements[i].derivative + 1] + "," + derivative_strings[
                                      state2.elements[i].derivative + 1] + ")\n")

            f.writelines("\n")


def checkOutputFolderExistence():
    if not os.path.exists("output"):
        os.makedirs("output")