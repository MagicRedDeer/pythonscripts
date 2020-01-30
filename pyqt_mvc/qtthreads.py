

import Qt.QtCore as core
import Qt.QtGui as gui
import Qt.QtWidgets as widgets
import time
import sys


class UpdateThread(core.QThread):
    def __init__(self, parent, interval=1):
        super(UpdateThread, self).__init__(parent=parent)
        self.interval = interval
        self.parent = parent

    def run(self):
        while(1):
            time.sleep(self.interval)
            self.parent.signal.emit(time.time())


class TimePiece(widgets.QLabel):
    signal = core.Signal(int, name='update_time')

    def __init__(self, parent):
        super(TimePiece, self).__init__(parent=parent)
        self.setText('Hello')
        self.t = time.time()
        self.timer = core.QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)
        # self.thread = UpdateThread(self)
        # self.signal.connect(self.updateTime)
        # self.thread.start()

    def updateTime(self, tm=None):
        tm = time.gmtime(tm)
        self.setText(time.asctime(tm))

class Diag(widgets.QDialog):
    def __init__(self):
        super(Diag, self).__init__()
        self.layout = widgets.QVBoxLayout(self)
        self.layout.addWidget(TimePiece(self))
        time.sleep(0.25)
        self.layout.addWidget(TimePiece(self))
        time.sleep(0.25)
        self.layout.addWidget(TimePiece(self))
        time.sleep(0.25)
        self.layout.addWidget(TimePiece(self))
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)
    win = Diag()
    win.show()
    app.exec_()
