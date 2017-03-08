from data_structures import Element, Influence, Proportionality, \
    QuantityConstraint


class Scenario:
    inflow = Element("I", 0, 3, 0)
    outflow = Element("O", 0, 3, 0)
    volume = Element("V", 0, 3, 0)
    height = Element("H", 0, 3, 0)
    pressure = Element("P", 0, 3, 0)
    elements = [inflow, outflow, volume, height, pressure]

    influence1 = Influence("I", "V", 1)
    influence2 = Influence("O", "V", -1)
    influences = [influence1, influence2]

    proportionality1 = Proportionality("V", "H", 1)
    proportionality2 = Proportionality("H", "P", 1)
    proportionality3 = Proportionality("P", "O", 1)
    proportionalities = [proportionality1, proportionality2, proportionality3]

    quantityConstraint1 = QuantityConstraint("V", "H")
    quantityConstraint2 = QuantityConstraint("H", "P")
    quantityConstraint3 = QuantityConstraint("P", "O")
    quantity_constraints = [quantityConstraint1, quantityConstraint2, quantityConstraint3]
