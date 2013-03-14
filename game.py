from PyQt4 import QtGui, QtCore
import sys, random

class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.body()
        self.menu()

    def body(self):
        self.setWindowTitle("X vs O")
        self.resize(200, 125)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.desktop = QtGui.QApplication.desktop()
        self.move((self.desktop.screenGeometry().width() - self.frameSize().width()) // 2, (self.desktop.screenGeometry().height() - self.frameSize().height()) // 2)
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

    def menu(self):
        self.menuFile = QtGui.QMenu("File")
        self.menu_single = QtGui.QAction("Single Player", None)
        self.menu_single.triggered.connect(self.single_game)
        self.menu_multi = QtGui.QAction("Multiplayer", None)
        self.menu_multi.triggered.connect(self.multi_game)
        self.menu_quit = QtGui.QAction("Quit", None)
        self.menu_quit.triggered.connect(QtGui.qApp.quit)
        self.menuFile.addAction(self.menu_single)
        self.menuFile.addAction(self.menu_multi)
        self.menuFile.addAction(self.menu_quit)

        self.menuHelp = QtGui.QMenu("Help")
        self.menu_about = QtGui.QAction("About X vs O", None)
        self.menu_about.triggered.connect(self.about)
        self.menu_qt = QtGui.QAction("About Qt", None)
        self.menu_qt.triggered.connect(self.qt)
        self.menuHelp.addAction(self.menu_about)
        self.menuHelp.addAction(self.menu_qt)

        self.menuBar().addMenu(self.menuFile)
        self.menuBar().addMenu(self.menuHelp)

    def single_game(self):
        self.single = Game("Single ")
        self.single.show()
        window.setVisible(False)

    def multi_game(self):
        self.multi = Game("Multi")
        self.multi.show()
        window.setVisible(False)

    def about(self):
        QtGui.QMessageBox.about(self, "About X vs O", "Create by Xebi4i as hometask")

    def qt(self):
        QtGui.QMessageBox.aboutQt(self)

class MainWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.body()

    def body(self):
        self.main_box = QtGui.QVBoxLayout()
        self.btn_singleplayer = QtGui.QPushButton("Single Player")
        self.btn_multiplayer = QtGui.QPushButton("Multiplayer")
        self.btn_quit = QtGui.QPushButton("Quit")
        self.main_box.addWidget(self.btn_singleplayer)
        self.main_box.addWidget(self.btn_multiplayer)
        self.main_box.addWidget(self.btn_quit)
        self.setLayout(self.main_box)

        self.btn_singleplayer.clicked.connect(self.click_single)
        self.btn_multiplayer.clicked.connect(self.click_multi)
        self.btn_quit.clicked.connect(QtGui.qApp.quit)

    def click_single(self):
        MyWindow.single_game(self)

    def click_multi(self):
        MyWindow.multi_game(self)

class Game(QtGui.QLabel):
    def __init__(self, mode, parent = None):
        QtGui.QLabel.__init__(self, parent)
        self.resize(300, 300)
        self.mode = mode
        self.pos = {'X' : set(), "O" : set()}
        self.elevants = {1 : [0, 0], 2 : [100, 0], 3 : [200, 0],
                         4 : [0, 100], 5 : [100, 100], 6 : [200, 100],
                         7 : [0, 200], 8 : [100, 200], 9 : [200, 200]}
        self.winner_comb = ({1, 2, 3}, {4, 5, 6}, {7, 8, 9},
                            {1, 4, 7}, {2, 5, 8}, {3, 6, 9},
                            {1, 5, 9}, {3, 5, 7})
        self.count_click = 0
        self.point = None
        self.died_x = None
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.desktop = QtGui.QApplication.desktop()
        self.move((self.desktop.screenGeometry().width() - self.frameSize().width()) // 2, (self.desktop.screenGeometry().height() - self.frameSize().height()) // 2)
        self.setWindowTitle(self.mode + "Player")
        self.body()

    def body(self):
        self.w, self.h = self.geometry().width(), self.geometry().height()

    def chacking(self):
        if len(self.pos["X"] | self.pos["O"]) >= 5:
            for i, j in self.pos.items():
                for p in self.winner_comb:
                    if j & p == p:
                        dialog = QtGui.QMessageBox(QtGui.QMessageBox.Information,
                                                   "X vs O",
                                                   "{0}{1} - WIN\nDo you want continue?".format(" " * 12, i),
                                                   buttons = QtGui.QMessageBox.No | QtGui.QMessageBox.Yes,
                                                   parent = self)
                        result = dialog.exec_()
                        if result == QtGui.QMessageBox.No:
                            self.close()
                        else:
                            self.pos = {'X' : set(), "O" : set()}
                            self.count_click = 0
                        self.update()
                        return
        if len(self.pos["X"] | self.pos["O"]) == 9:
            dialog = QtGui.QMessageBox(QtGui.QMessageBox.Information,
                                               "X vs O",
                                               "{0}Nobody win\nDo you want continue?".format(" " * 7),
                                               buttons = QtGui.QMessageBox.No | QtGui.QMessageBox.Yes,
                                               parent = self)
            result = dialog.exec_()
            if result == QtGui.QMessageBox.No:
                self.close()
            else:
                self.pos = {'X' : set(), "O" : set()}
                self.count_click = 0
            self.update()
            return

    def single(self):
        self.pos["X" if self.count_click % 2 == 0 else "O"].add(self.point)
        self.count_click += 1
        self.update()
        self.chacking()
    
    def multi(self):
        self.pos["X"].add(self.point)
        self.update()
        self.chacking()
        for i in self.winner_comb:
            if len(i - self.pos["O"]) == 1 and list(i - self.pos["O"])[0] not in self.pos["X"]:
                self.pos["O"].add(list(i - self.pos["O"])[0])
                self.update()
                self.chacking()
                return
            elif len(i - self.pos["X"]) == 1 and list(i - self.pos["X"])[0] not in self.pos["O"]:
                self.died_x = list(i - self.pos["X"])[0]
                continue
        if self.died_x:    
            self.pos["O"].add(self.died_x)
            self.died_x = None
            self.update()
            self.chacking()
            return
        if len(self.pos["O"]) == 0:
            self.pos["O"].add(random.choice([i for i in ({1, 3, 7, 9} - self.pos["X"])]))
            self.update()
            self.chacking()
            return
        elif len({1, 2, 3, 4, 5, 6, 7, 8, 9} - self.pos["X"] - self.pos["O"]) > 0:
            self.pos["O"].add(random.choice([i for i in ({1, 2, 3, 4, 5, 6, 7, 8, 9} - self.pos["X"] - self.pos["O"])]))
            self.update()
            self.chacking()
            return
            
    def mousePressEvent(self, e):
        self.point = (e.y() // (self.h // 3)) * 3 + (e.x() // (self.w // 3)) + 1    
        if (self.point not in self.pos["X"] | self.pos["O"]):
            if self.mode == "Single ":
                self.single()
            elif self.mode == "Multi":
                self.multi()
        e.ignore()
        QtGui.QLabel.mousePressEvent(self, e)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor("#44aaee")), 3,
                                  style = QtCore.Qt.SolidLine,
                                  cap = QtCore.Qt.RoundCap,
                                  join = QtCore.Qt.RoundJoin))
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#ffffff")))
        painter.drawLines(QtCore.QLine(self.w // 3, 0, self.w // 3, self.h),
                          QtCore.QLine(self.w // 3 * 2, 0, self.w // 3 * 2, self.h),
                          QtCore.QLine(0, self.h // 3, self.w, self.h // 3),
                          QtCore.QLine(0, self.h // 3 * 2, self.w, self.h // 3 * 2))
        for i, j in self.pos.items():
            for k in j:
                if i == "X":
                    painter.drawLines(QtCore.QLine(self.elevants[k][0] + 10, self.elevants[k][1] + 10, self.elevants[k][0] + 90, self.elevants[k][1] + 90),
                                      QtCore.QLine(self.elevants[k][0] + 10, self.elevants[k][1] + 90, self.elevants[k][0] + 90, self.elevants[k][1] + 10))
                else:
                    painter.drawEllipse(self.elevants[k][0] + 10, self.elevants[k][1] + 10, 80, 80)

    def closeEvent(self, e):
        window.setVisible(True)
        e.accept()
        QtGui.QLabel.closeEvent(self, e)

def main():
    global window
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
