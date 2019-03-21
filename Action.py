from criticalpath import Node
import matplotlib.pyplot as plt
import networkx as nx
import plotly.plotly as py
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import plotly.offline
import plotly.io as pio
import plotly.graph_objs as go


class Action:
    def __init__(self, name, duration, pred):
        self.name = name
        self.duration = int(duration)   
        self.predecessors = pred
        self.start = ""
        self.finish = ""
        if not self.is_number():
            raise Exception("Wprowadzona wartość nie jest liczbą!")
        if self.exist_loop():
            raise Exception("Zadanie zapętlone!")

    def is_number(self):
        tmp = self.duration
        if isinstance(float(tmp), float) or isinstance(int(tmp), int):
            return True
        return False

    def exist_loop(self):
        if self.name in self.predecessors:
            return True
        return False

# testing part
actionsX = []
actionsX.append(Action("START", 0, []))
actionsX.append(Action("A", 4, ['START']))
actionsX.append(Action("B", 6, ['START']))
actionsX.append(Action("C", 4, ['B']))
actionsX.append(Action("D", 12, ['A']))
actionsX.append(Action("E", 7, ['A', 'C']))
actionsX.append(Action("F", 9, ['B']))
actionsX.append(Action("G", 5, ['E', 'F']))
actionsX.append(Action("END", 0, ['D', 'G']))


class Project:
    def __init__(self):
        self.p = Node('project')
        self.nodes = []

    def create_network(self, actions):
        for action in actions:
            self.nodes.append(self.p.add(Node(action.name, action.duration)))
        for action in actions:
            for pre in action.predecessors:
                self.p.link(pre, action.name)
        self.p.update_all()

    def get_critical_path(self):
        return self.p.get_critical_path()

    def get_duration(self):
        return self.p.duration

def create_graph_image(actions, critic_path):
    G = nx.Graph()
    str_critic_path = [str(node) for node in critic_path]
    for action in actions:
        for pred in action.predecessors:
            dr = [act.duration for act in actions if act.name == pred]
            G.add_edge(pred, action.name, weight=dr[0])

    cp = [(u, v) for (u, v) in G.edges(data=False) if u in str_critic_path and v in str_critic_path]
    np = [(u, v) for (u, v) in G.edges(data=False) if u not in str_critic_path or v not in str_critic_path]

    position = nx.spring_layout(G, k=3)

    nx.draw_networkx_nodes(G, position, node_size=700)

    nx.draw_networkx_edges(G, position, edgelist=cp, edge_color='r', style='dashed')
    nx.draw_networkx_edges(G, position, edgelist=np)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, position, edge_labels=labels)
    nx.draw_networkx_labels(G, position, font_size=20)

    plt.axis('off')
    plt.savefig('images/graph.png', dpi=100)


def create_gantt_chart(actions, critic_path):
    py.plotly.tools.set_credentials_file(username='dracco25', api_key='STCeveETjYeliL6PMwAH')
    str_critic_path = [str(node) for node in critic_path]
    now = datetime.now()
    actions[0].start = datetime.strftime(now, "%d-%m-%Y")
    actions[0].finish = datetime.strptime(actions[0].start, "%d-%m-%Y") + timedelta(days=actions[0].duration)
    for action in actions[1:]:
        older = actions[0].finish
        for pred in action.predecessors:
            _pred = [act for act in actions if act.name == pred][0]
            if _pred.finish > older:
                older = _pred.finish
        action.start = older
        action.finish = action.start + timedelta(days=action.duration)

    tasks = []
    for action in actions[1:-1]:
        tasks.append(dict(Task=action.name, Start=action.start, Finish=action.finish, Resource="Critical" if action.name in str_critic_path else "NotCritical"))
    colors = {'Critical': 'rgb(0, 255, 100)',
              'NotCritical': 'rgb(220, 0, 0)',
            }
    fig = ff.create_gantt(tasks, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True)
   # img_bytes = pio.to_image(fig, format='png')
    plotly.offline.plot(fig, auto_open=True)
    #py.iplot(fig, filename='gantt-group-tasks-together', world_readable=True)
#    pio.write_image(fig, 'images/gantt.png')


