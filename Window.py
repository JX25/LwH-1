from __future__ import unicode_literals

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PlotCanvas import PlotCanvas
from Action import Action, create_gantt_chart
from Action import Project
from Action import create_graph_image


class App(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.actions = []
        self.project = Project()
        self.create_window()

    def create_window(self):
        # labels
        nameLabel = QLabel("Nazwa akcji", self)
        durationLabel = QLabel("Czas trwania akcji", self)
        predLabel = QLabel("Poprzednicy [;]", self)
        self.criticalPathLabel = QLabel("Ścieżka krytyczna: ", self)
        self.timeLabel = QLabel("Czas trwania: ", self)
        self.messageLabel = QLabel("", self)
        self.ganttLabel = QLabel(self)
        self.graphLabel = QLabel(self)

        pixmap1 = QPixmap('gantt.jpg')
        pixmap2 = QPixmap('graph.jpg')

        self.ganttLabel.setPixmap(pixmap1)
        self.graphLabel.setPixmap(pixmap2)
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

        # web view
        self.view = QWebEngineView(self)
        self.view.setFixedWidth(800)
        self.view.setFixedHeight(600)
        url = QtCore.QUrl.fromLocalFile(r"/temp-plot.html")
        self.view.load(url)
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
        #grid.addWidget(self.ganttLabel, 0, 3, 5, 6)
        grid.addWidget(self.graphLabel, 3, 1, 3, 2)
        grid.addWidget(self.view, 0, 3, 5, 6)

        self.setLayout(grid)
        self.resize(500, 500)
        self.setWindowTitle("App")
        self.show()

    def add_action(self):
        name = self.nameEntry.text()
        duration = self.durationEntry.text()
        if self.predEntry.text() == '':
            pred = []
        else:
            pred = self.predEntry.text().split(";")
        try: #s
            self.actions.append(Action(name, duration, pred))
            self.messageLabel.setText("Dodano czynność: "+name)
        except Exception as error:
            self.messageLabel.setText(error.args[0])
            self.actions = []
        for task in self.actions:
            print(task.name + " " + str(task.duration) + " " + str(task.predecessors))

    def compute_task(self):
        if self.actions != []:
            self.project.create_network(self.actions)
            cp = self.project.get_critical_path()
            dr = self.project.get_duration()
            create_graph_image(self.actions, cp)
            self.graphLabel.setPixmap(QPixmap('images/graph.png'))
            create_gantt_chart(self.actions, cp)
            url = QtCore.QUrl.fromLocalFile(r"temp-plot.html")
            self.view.load(url)
           # self.ganttLabel.setPixmap(QPixmap('images/gantt.png'))
            self.timeLabel.setText("Czas trwania " + str(dr) + "h")
            string_cp = str(cp[0])
            for node in cp[1:]:
                string_cp += " -> " + str(node)
            self.criticalPathLabel.setText(string_cp)
        else:
            self.messageLabel.setText("Brak danych!")




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
