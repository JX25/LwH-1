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
