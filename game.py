from PyQt4 import QtGui, QtCore
import sys

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
        self.pos = {'X' : [], "O" : []}
        self.comb = {'X' : set(), "O" : set()}
        self.paterns = ({1, 2, 3}, {4, 5, 6}, {7, 8, 9},
                        {1, 4, 7}, {2, 5, 8}, {3, 6, 9},
                        {1, 5, 9}, {3, 5, 7})
        self.count_click = 0
        self.point = None
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.desktop = QtGui.QApplication.desktop()
        self.move((self.desktop.screenGeometry().width() - self.frameSize().width()) // 2, (self.desktop.screenGeometry().height() - self.frameSize().height()) // 2)
        self.setWindowTitle(self.mode + "Player")
        self.body()

    def body(self):
        self.w, self.h = self.geometry().width(), self.geometry().height()

    def chacking(self):
        for i, j in self.comb.items():
            for p in self.paterns:
                if j & p == p:
                    dialog = QtGui.QMessageBox(QtGui.QMessageBox.Information,
                                               "X vs O",
                                               "              {0} - WIN\nDo you want continue?".format(i),
                                               buttons = QtGui.QMessageBox.No | QtGui.QMessageBox.Yes,
                                               parent = self)
                    result = dialog.exec_()
                    if result == QtGui.QMessageBox.No:
                        self.close()
                    else:
                        self.pos = {'X' : [], "O" : []}
                        self.comb = {'X' : set(), "O" : set()}
                        self.update()

    def mousePressEvent(self, e):
        self.point = ((e.x() // (self.w // 3)) * self.w // 3,
                      (e.y() // (self.h // 3)) * self.h // 3)
        if (self.point not in self.pos["X"] and self.point not in self.pos["O"]):
            self.count_click += 1
            self.pos["X" if self.count_click % 2 == 1 else "O"].append(self.point)
            self.comb["X" if self.count_click % 2 == 1 else "O"].add((e.y() // (self.h // 3)) * 3 + (e.x() // (self.w // 3)) + 1)
            self.update()
        self.chacking()
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
                painter.drawLines(QtCore.QLine(k[0] + 10, k[1] + 10, k[0] + self.w // 3 - 10, k[1] + self.h // 3 - 10),
                                  QtCore.QLine(k[0] + 10, k[1] + self.h // 3 - 10, k[0] + self.w // 3 - 10, k[1] + 10)) if i == "X" else painter.drawEllipse(k[0] + 10, k[1] + 10, self.w // 3 - 20, self.h // 3 - 20)

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
