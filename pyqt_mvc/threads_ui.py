from Qt import QtCore, QtGui, QtWidgets
import time

class Manager(QtCore.QObject):
    pass

class Worker(QtCore.QObject):
    threadInfo = QtCore.Signal(object, object)
    done = QtCore.Signal()

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent=parent)

    @QtCore.Slot()
    def emitInfo(self):
        self.threadInfo.emit(self.objectName(), QtCore.QThread.currentThreadId())

    def run(self):
        print QtCore.QThread.currentThreadId(), 'from thread', self.objectName(), 'busy'
        time.sleep(10)
        print QtCore.QThread.currentThreadId(), 'from thread', self.objectName(), 'done'

class WorkerThread(QtCore.QThread):
    worker = None

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent=parent)

    def setWorker(self, worker):
        self.unsetWorker()
        self.worker = worker
        self.started.connect(worker.run)
        self.worker.done.connect(self.done)

    def unsetWorker(self):
        if self.worker:
            self.started.disconnect(self.worker.run)
            self.worker.done.disconnect(self.done)
            self.worker = None

    def done(self):
        self.unsetWorker()

class Window(QtWidgets.QWidget):
    num = 0
    def __init__(self):
        super(Window, self).__init__()

        self.launchButton = QtWidgets.QPushButton('Launch', self)
        self.launchButton.clicked.connect(self.launch)

        self.infoButton = QtWidgets.QPushButton('Info', self)
        self.infoButton.clicked.connect(self.info)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.launchButton)
        layout.addWidget(self.infoButton)

        self.thread = WorkerThread(self)
        # self.thread.start()

    def launch(self):
        self.num+=1
        worker = Worker(self)
        worker.setObjectName('Worker' + str(self.num))
        self.thread.setWorker(worker)
        self.thread.start()

    def info(self):
        if self.thread.worker:
            print self.thread.worker.objectName()
        else:
            print 'no worker'

    def closeEvent(self, event):
        self.thread.quit()
        self.thread.wait()

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
