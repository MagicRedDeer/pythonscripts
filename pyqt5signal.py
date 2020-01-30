from PyQt5 import QtWidgets, QtCore


import os


class Widget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vboxLayout = QtWidgets.QVBoxLayout(self)
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        QtCore.QObject.connect(
                self.timer, QtCore.pyqtSignal("timeout()"), self.timer_fired)

    @QtCore.pyqtSlot()
    def timer_fired(self):
        print('timer was fired')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = Widget()
    win.show()
    app.exec_()
