import itertools

import support_functions as sf
from graph_structures import Edge


class Algorithm:
    trace_writer = 0
    scenario = 0

    def __init__(self, scenario):
        self.scenario = scenario

    def applyImmediateInfluence(self, influence, state):
        element1 = sf.findElement(state.elements, influence.element1)
        element2 = sf.findElement(state.elements, influence.element2)

        if element2.derivative == 0 and element1.value > 0:
            if influence.relation_type == 1:
                element2.derivative = sf.increaseDerivative(element2.derivative)
            else:
                element2.derivative = sf.decreaseDerivative(element2.derivative)

    def applyImmediateProportion(self, proportionality, state):
        element1 = sf.findElement(state.elements, proportionality.element1)
        element2 = sf.findElement(state.elements, proportionality.element2)
        if element2.derivative == 0:
            if element1.derivative > 0:
                if proportionality.relation_type == 1:
                    element2.derivative = sf.increaseDerivative(element2.derivative)
                else:
                    element2.derivative = sf.decreaseDerivative(element2.derivative)
            elif element1.derivative < 0:
                if proportionality.relation_type == 1:
                    element2.derivative = sf.decreaseDerivative(element2.derivative)
                else:
                    element2.derivative = sf.increaseDerivative(element2.derivative)

    def applyImmediateRelations(self, state, influences, proportionalities):
        permutations = list(itertools.permutations(influences + proportionalities))

        new_states = []
        for permutation in permutations:
            new_state = sf.copyState(state)
            for relation in permutation:
                if relation.type == "Influence":
                    self.applyImmediateInfluence(relation, new_state)
                else:
                    self.applyImmediateProportion(relation, new_state)
            new_states.append(new_state)
        return new_states

    def updateImmediateValues(self, states, scenario):
        newly_created_states = []
        quantity_constraints = scenario.quantity_constraints

        for state in states:
            temp_state = sf.copyState(state)

            for element in temp_state.elements:
                if element.value % 2 == 0 and element.derivative != 0:
                    if element.derivative == -1:
                        element.value = sf.decreaseValue(element.value)
                    elif element.derivative == 1:
                        element.value = sf.increaseValue(element.value)
            if not sf.checkStateEquality(state, temp_state):
                constraint_check = True
                for constraint in quantity_constraints:
                    if not sf.checkConstraint(constraint, temp_state):
                        constraint_check = False
                if constraint_check:
                    newly_created_states.append(temp_state)
        return newly_created_states


    def updateImmediateDerivatives(self, states, scenario):
        newly_created_states = []
        for state in states:
            newly_created_states += self.applyImmediateRelations(state, scenario.influences, scenario.proportionalities)
        return newly_created_states

    def updateValuesMultipleElements(self, state, elements_to_update, quantity_constraints):
        combinations = []
        if len(elements_to_update) != 1:
            for i in range(0, len(elements_to_update) + 1):
                combinations += list(itertools.combinations(elements_to_update, i))
        else:
            combinations = [elements_to_update]
        new_states = []

        for combination in combinations:
            new_state1 = sf.copyState(state)
            new_state2 = sf.copyState(state)
            for combination_i in combination:
                index = combination_i
                if new_state1.elements[index].derivative == -1:
                    new_state1.elements[index].value = sf.decreaseValue(new_state1.elements[index].value)
                elif new_state1.elements[index].derivative == 1:
                    new_state1.elements[index].value = sf.increaseValue(new_state1.elements[index].value)
                new_state2.elements[index].derivative = 0

            constraint_check_1 = True
            constraint_check_2 = True

            for constraint in quantity_constraints:
                if not sf.checkConstraint(constraint, new_state1):
                    constraint_check_1 = False
                if not sf.checkConstraint(constraint, new_state2):
                    constraint_check_2 = False
            if constraint_check_1:
                new_states.append(new_state1)
            if constraint_check_2:
                new_states.append(new_state2)
        return new_states

    def applyTimeInfluence(self, influence, state):
        element1 = sf.findElement(state.elements, influence.element1)
        element2 = sf.findElement(state.elements, influence.element2)

        if element1.value > 0:
            if influence.relation_type == 1:
                element2.derivative = sf.increaseDerivative(element2.derivative)
            else:
                element2.derivative = sf.decreaseDerivative(element2.derivative)

    def applyTimeProportion(self, proportionality, state):
        element1 = sf.findElement(state.elements, proportionality.element1)
        element2 = sf.findElement(state.elements, proportionality.element2)
        if element1.derivative > 0:
            if proportionality.relation_type == 1:
                element2.derivative = sf.increaseDerivative(element2.derivative)
            else:
                element2.derivative = sf.decreaseDerivative(element2.derivative)
        elif element1.derivative < 0:
            if proportionality.relation_type == 1:
                element2.derivative = sf.decreaseDerivative(element2.derivative)
            else:
                element2.derivative = sf.increaseDerivative(element2.derivative)

    def applyTimeRelations(self, state, influences, proportionalities):
        combined = influences + proportionalities
        permutations = list(itertools.permutations(combined))

        new_states = []
        for permutation in permutations:
            new_state = sf.copyState(state)
            for permutation_i in permutation:
                if permutation_i.type == "Influence":
                    self.applyTimeInfluence(permutation_i, new_state)
                else:
                    self.applyTimeProportion(permutation_i, new_state)
            new_states.append(new_state)
        return new_states

    def updateTimeValues(self, states, scenario):
        newly_created_states = []

        for state in states:
            quantity_constraints = scenario.quantity_constraints
            temp_state = sf.copyState(state)

            elements_to_update = []
            for i in range(len(temp_state.elements)):
                if temp_state.elements[i].value % 2 != 0 and temp_state.elements[i].derivative != 0:
                    elements_to_update.append(i)

            newly_created_states += self.updateValuesMultipleElements(temp_state, elements_to_update,
                                                                      quantity_constraints)
        return newly_created_states

    def updateTimeDerivatives(self, states, scenario):
        newly_created_states = []
        for state in states:
            for element_i in state.elements:
                if element_i.value == 2 and element_i.maxValue == 3:
                    element_i.derivative = 0
                elif element_i.value == 1 and element_i.maxValue == 2:
                    element_i.derivative = 0
                elif element_i.value == 0:
                    element_i.derivative = 0
            newly_created_states += self.applyTimeRelations(state, scenario.influences,
                                                            scenario.proportionalities)
        return newly_created_states

    def propagateState(self, state, scenario):
        states = [state]

        states1 = sf.removeDuplicateStates(self.updateImmediateValues(states, scenario))
        states2 = sf.removeDuplicateStates(self.updateImmediateDerivatives(states1, scenario))
        if len(states1) == 0 and len(states2) == 0:
            states.append(state)
            states1 = sf.removeDuplicateStates(self.updateTimeValues(states, scenario))
            states2 = sf.removeDuplicateStates(self.updateTimeDerivatives(states1, scenario))
        states = sf.removeDuplicateStates(states1 + states2)
        return states

    def createNewStates(self, old_states, initial_states, finalStates, edges, state_counter, scenario):
        for old_state in old_states:
            new_states = self.propagateState(old_state, scenario)

            inflow_changes = []
            for new_state in new_states:
                inflow_changes += self.addInflowChanges(new_state)
            new_states += inflow_changes
            for new_state in new_states:
                if sf.checkStateValidity(new_state):
                    result, state = sf.checkStateExistence(finalStates, new_state)
                    if not result:
                        state.id = state_counter
                        state_counter += 1
                        finalStates[state.id] = state
                        initial_states.append(state)

                    edge = Edge(old_state.id, state.id)
                    result = sf.checkEdgeValidity(old_state.id, state.id, finalStates)
                    if result:
                        result, edge = sf.checkEdgeExistence(edges, edge)
                        if not result:
                            edges.append(edge)
        return state_counter

    def addInflowChanges(self, state):
        output_states = []
        inflow = state.elements[0]

        new_state1 = sf.copyState(state)
        new_state1.elements[0].derivative = 0

        new_state2 = sf.copyState(state)
        if inflow.value == 2:
            new_state2.elements[0].derivative = -1
        elif inflow.value == 0:
            new_state2.elements[0].derivative = 1
        else:
            if inflow.derivative != 0:
                new_state2.elements[0].derivative = 0

        output_states.append(new_state1)
        output_states.append(new_state2)

        return output_states

    def runAlgorithm(self):
        final_states = {}
        edges = []

        generated_states, state_counter = sf.generateStartingStates(self.scenario)

        for generated_state in generated_states:
            final_states[generated_state.id] = generated_state

        for generated_state in generated_states:
            initial_states = [generated_state]

            stop = False
            while not stop:
                if len(initial_states) == 0:
                    stop = True
                else:
                    old_states = initial_states
                    initial_states = []
                    state_counter = self.createNewStates(old_states, initial_states, final_states, edges, state_counter,
                                                         self.scenario)

        return final_states, edges
