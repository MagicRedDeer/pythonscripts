
import sip

sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import PyQt4.QtCore as core
import PyQt4.QtGui as gui
import time
import sys


class Task(object):

    def __init__(self, adap):
        self.adap = adap

    def go(self):
        self.adap.msg('Starting...')
        for i in range(10):
            time.sleep(0.5)
            self.adap.msg('Step %s'%i)
        self.adap.done()


class TaskAdapter(core.QObject):

    workdone = core.pyqtSignal()
    update = core.pyqtSignal(str)

    def done(self):
        print 'done'
        self.update.emit('done')
        self.workdone.emit()

    def msg(self, msg):
        print msg
        self.update.emit(msg)

    def start(self):
        Task(self).go()

class Diag(gui.QDialog):

    update = core.pyqtSignal(str)

    def __init__(self):
        super(Diag, self).__init__()
        self.layout = gui.QVBoxLayout(self)
        self.label = gui.QLabel(self)
        self.btn = gui.QPushButton('PressMe', self)
        self.browseButton = gui.QPushButton('Browse', self)
        self.browseButton.clicked.connect(self.browse)
        self.btn.clicked.connect(self.go)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.browseButton)
        self.setLayout(self.layout)
        self.thread = None
        self.timer = core.QTimer(self)

    def go(self):
        if self.thread:
            self.label.setText('ignore request')
            return
        self.thread = core.QThread(self)
        self.adap = TaskAdapter()
        self.adap.moveToThread(self.thread)
        self.thread.finished.connect(self.adap.deleteLater)
        self.adap.workdone.connect(self.thread.terminate)
        self.thread.started.connect(self.adap.start)
        self.adap.update.connect(self._update)
        self.thread.start()

    def _update(self, msg):
        if msg=='done':
            self.thread.terminate()
            self.thread.deleteLater()
            self.thread = None
        self.label.setText(msg)

    def browse(self):
        self.timer.stop()
        filename = gui.QFileDialog.getOpenFileNames(self, 'Select Folder', '',
                '*.ma *.mb *.txt')
        if filename:
            self.label.setText(filename[0])

    def closeEvent_(self, event):
        self.thread.terminate()


if __name__ == '__main__':
    app = gui.QApplication(sys.argv)
    win = Diag()
    win.show()
    app.exec_()

