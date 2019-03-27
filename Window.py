from __future__ import unicode_literals

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
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
        nameLabel.setFixedWidth(100)
        durationLabel = QLabel("Czas trwania akcji", self)
        durationLabel.setFixedWidth(100)
        predLabel = QLabel("Poprzednicy [;]", self)
        predLabel.setFixedWidth(100)
        self.criticalPathLabel = QLabel("Ścieżka krytyczna: ", self)
        self.timeLabel = QLabel("Czas trwania: ", self)
        self.messageLabel = QLabel("", self)
        self.graphLabel = QLabel(self)

        pixmap2 = QPixmap('images/graph.png')

        self.graphLabel.setPixmap(pixmap2)
        # entries
        self.nameEntry = QLineEdit()
        self.nameEntry.setFixedWidth(150)
        self.durationEntry = QLineEdit()
        self.durationEntry.setFixedWidth(150)
        self.predEntry = QLineEdit()
        self.predEntry.setFixedWidth(150)

        # buttons
        addButton = QPushButton("Dodaj czynność", self)
        addButton.setFixedWidth(100)
        computeButton = QPushButton("Oblicz", self)
        computeButton.setFixedWidth(100)

        # buttons action
        addButton.clicked.connect(self.add_action)
        computeButton.clicked.connect(self.compute_task)

        # web view
        self.view = QWebEngineView(self)
        self.view.setMinimumWidth(800)
        self.view.setMinimumHeight(600)
        url = QtCore.QUrl.fromLocalFile(r"/temp-plot.html")
        self.view.load(url)
        # grid

        hboxRow1 =QHBoxLayout()
        hboxRow1.addWidget(nameLabel)
        hboxRow1.addWidget(self.nameEntry)
        hboxRow1.addWidget(addButton)
        hboxRow1.addStretch(1)

        hboxRow2 =QHBoxLayout()
        hboxRow2.addWidget(durationLabel)
        hboxRow2.addWidget(self.durationEntry)
        hboxRow2.addWidget(computeButton)
        hboxRow2.addStretch(1)

        hboxRow3 = QHBoxLayout()
        hboxRow3.addWidget(predLabel)
        hboxRow3.addWidget(self.predEntry)
        hboxRow3.addStretch(1)

        vboxRowLast =QVBoxLayout()
        vboxRowLast.addWidget(self.criticalPathLabel)
        vboxRowLast.addWidget(self.timeLabel)


        vboxEntryData = QVBoxLayout()
        vboxEntryData.addLayout(hboxRow1)
        vboxEntryData.addLayout(hboxRow2)
        vboxEntryData.addLayout(hboxRow3)
        vboxEntryData.addLayout(vboxRowLast)


        vboxGraphInfo = QVBoxLayout()
        vboxGraphInfo.addWidget(self.graphLabel)
        vboxGraphInfo.addStretch(1)
        vboxGraphInfo.addWidget(self.messageLabel)

        vboxLeftSide = QVBoxLayout()
        vboxLeftSide.addLayout(vboxEntryData)
        vboxLeftSide.addStretch(1)
        vboxLeftSide.addLayout(vboxGraphInfo)

        hboxFinal = QHBoxLayout()
        hboxFinal.addLayout(vboxLeftSide)
        hboxFinal.addStretch(1)
        hboxFinal.addWidget(self.view)

        self.setLayout(hboxFinal)
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
            url = QtCore.QUrl.fromLocalFile(r"/temp-plot.html")
            self.view.load(url)
           # self.ganttLabel.setPixmap(QPixmap('images/gantt.png'))
            self.timeLabel.setText("Czas trwania " + str(dr) + "h")
            string_cp = str(cp[0])
            for node in cp[1:]:
                string_cp += " -> " + str(node)
            self.criticalPathLabel.setText(string_cp)
            self.actions = []
            self.project = Project()
        else:
            self.messageLabel.setText("Brak danych!")
            self.actions = []
            self.project = Project()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
