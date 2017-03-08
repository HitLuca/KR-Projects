from algorithm import Algorithm
from graph_plotter import Plotter
from scenario import Scenario
import support_functions as sf

scenario = Scenario()
algorithm = Algorithm(scenario)
states, edges = algorithm.runAlgorithm()
graph_plotter = Plotter(states, edges)

sf.checkOutputFolderExistence()

sf.writeTrace(states, edges)
print("Trace saved to output/trace.dat")

graph_plotter.save()
print("Graph structure saved to output/graph.dot")
print("Graph plot saved to output/graph.png")
print("Legenda saved to output/legend.png")

graph_plotter.plot()
