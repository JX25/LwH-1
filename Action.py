from criticalpath import Node

class Action:
    def __init__(self, name, duration, pred):
        self.name = name
        self.duration = duration
        self.predecessors = pred
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
        for action in actionsX:
            self.nodes.append(self.p.add(Node(action.name, action.duration)))
        for action in actionsX:
            for pre in action.predecessors:
                self.p.link(pre, action.name)
        self.p.update_all()

    def get_critical_path(self):
        return self.p.get_critical_path()

    def get_duration(self):
        return self.p.duration



