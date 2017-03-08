import matplotlib.pyplot as plt
import networkx as nx
import pydotplus

class Plotter:
    def __init__(self, states, edges):
        self.states = states
        self.edges = edges
        g = nx.DiGraph()
        for key, state in states.items():
            g.add_node(state.id)
        for edge in edges:
            g.add_edge(edge.state1_id, edge.state2_id)

        self.g = g

    def drawGraph(self):
        pos = nx.circular_layout(self.g)
        nx.draw(self.g, pos)
        nx.draw_networkx_labels(self.g, pos)

    def setTitle(self, title):
        if title == "I":
            plt.title("Inflow")
        elif title == "O":
            plt.title("Outflow")
        elif title == "H":
            plt.title("Height")
        elif title == "P":
            plt.title("Pressure")
        elif title == "V":
            plt.title("Volume")

    def drawLegend(self):
        elements = 5
        axis = range(0, len(self.states) + 2)

        labels = [""]
        for i in range(0, len(self.states)):
            labels.append(i+1)
        labels.append("")

        for key, state in self.states.items():
            for j in range(elements):
                value = state.elements[j].value
                derivative = state.elements[j].derivative

                plt.subplot(5, 1, j + 1)
                if derivative == 0:
                    plt.plot(key, value, 'o', color="#cccccc", ms=10, clip_on=False)
                elif derivative == 1:
                    plt.plot(key, value, '^', color="#cccccc", ms=10, clip_on=False)
                else:
                    plt.plot(key, value, 'v', color="#cccccc", ms=10, clip_on=False)

        for j in range(elements):
            ax = plt.subplot(5, 1, j + 1)
            title = self.states[1].elements[j].name
            self.setTitle(title)

            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)

            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')

            plt.yticks([0, 1, 2], [0, "+", "max"])
            plt.ylim(-0.4, 2.4)
            plt.xticks(axis, labels, rotation=90)


    def plot(self):
        fig = plt.figure(0)
        fig.canvas.set_window_title('States graph')
        self.drawGraph()
        fig = plt.figure(1)
        fig.canvas.set_window_title('States details')
        self.drawLegend()

        plt.tight_layout()
        plt.show()

    def save(self):
        nx.drawing.nx_pydot.write_dot(self.g, 'output/graph.dot')
        gdot = pydotplus.graph_from_dot_file('output/graph.dot')
        gdot.write_png('output/graph.png')

        plt.figure()
        self.drawLegend()
        plt.tight_layout()
        plt.savefig('output/legend.png', format='png')

