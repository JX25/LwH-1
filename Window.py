from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton
from PlotCanvas import PlotCanvas
from Action import Action


class App(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.actions = []
        self.create_window()

    def create_window(self):
        # labels
        nameLabel = QLabel("Nazwa akcji", self)
        durationLabel = QLabel("Czas trwania akcji", self)
        predLabel = QLabel("Poprzednicy [;]", self)
        self.criticalPathLabel = QLabel("Ścieżka krytyczna: ", self)
        self.timeLabel = QLabel("Czas trwania: ", self)
        self.messageLabel = QLabel("", self)

        # entries
        self.nameEntry = QLineEdit()
        self.durationEntry = QLineEdit()
        self.predEntry = QLineEdit()

        # buttons
        addButton = QPushButton("Dodaj czynność", self)
        computeButton = QPushButton("Oblicz", self)

        # buttons action
        addButton.clicked.connect(self.add_action)
        computeButton.clicked.connect(self.compute_task)

        #canvas gantt
        canvas = PlotCanvas(self, width=5, height=6)

        # grid
        grid = QGridLayout()

        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(durationLabel, 1, 0)
        grid.addWidget(predLabel, 2, 0)
        grid.addWidget(self.criticalPathLabel, 3, 0)
        grid.addWidget(self.timeLabel, 4, 0)
        grid.addWidget(self.messageLabel, 5, 0)
        grid.addWidget(self.nameEntry, 0, 1)
        grid.addWidget(self.durationEntry, 1, 1)
        grid.addWidget(self.predEntry, 2, 1)
        grid.addWidget(addButton, 0, 2)
        grid.addWidget(computeButton, 1, 2)
        grid.addWidget(canvas, 0, 3, 5, 6)

        self.setLayout(grid)
        self.resize(600, 300)
        self.setWindowTitle("App")
        self.show()

    def add_action(self):
        name = self.nameEntry.text()
        duration = self.durationEntry.text()
        pred = self.predEntry.text().split(";")

        try:
            self.actions.append(Action(name, duration, pred))
        except Exception as error:
            self.messageLabel.setText(error.args[0])
            self.actions = []

        for task in self.actions:
            print(task.name + " " + str(task.duration) + " " + str(task.predecessors))

    def compute_task(self):
        return


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
