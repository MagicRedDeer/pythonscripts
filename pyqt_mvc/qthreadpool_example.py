import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore as core
from PyQt4 import QtGui as gui

import time
import random

class DeferredJob(core.QRunnable):

    class _QObject(core.QObject):
        done = core.pyqtSignal(int)
        def __init__(self, parent=None):
            super(DeferredJob._QObject, self).__init__(parent=parent)

    def __init__(self, info):
        core.QRunnable.__init__(self)
        self._obj = DeferredJob._QObject()
        self.done = self._obj.done
        self.info = info

    def run(self):
        time.sleep(1 + random.random() * 2)
        self.done.emit(self.info)

class Window(gui.QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.layout = gui.QVBoxLayout(self)
        self.text = gui.QTextEdit(self)
        self.button = gui.QPushButton('Start', self)
        self.abort_button = gui.QPushButton('Abort', self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.abort_button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.button_clicked)
        self.abort_button.clicked.connect(self.abort)
        self.jobs = {}

        self.threadpool = core.QThreadPool.globalInstance()
        self.threadpool = core.QThreadPool(self)
        self.threadpool.setMaxThreadCount(5)

    def button_clicked(self):
        self.text.append('start ...')
        self.text.repaint()
        self.jobs = {}
        for i in range(10):
            j = DeferredJob(i)
            self.jobs[i] = j
            #j.setAutoDelete(False)
            j.done.connect(self.thread_done)
            self.threadpool.start(j)

    def abort(self):
        pass

    def thread_done(self, info):
        self.text.append('%s done' %info)
        self.text.repaint()
        del self.jobs[info]
        if not self.threadpool.activeThreadCount():
            self.text.append('all done')


if __name__ == '__main__':
    import sys
    app = gui.QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()

