import logging
import time
import sys

from multiprocessing.pool import ThreadPool

import Qt.QtCore as core
import Qt.QtWidgets as widgets


class QLoggerText(logging.Handler, widgets.QTextEdit):
    appended = core.Signal(logging.LogRecord)

    def __init__(self, parent=None):
        widgets.QTextEdit.__init__(self, parent=parent)
        logging.Handler.__init__(self)
        self.appended.connect(self._appended)
        self.loggers = []

    def _appended(self, record):
        self.append(self.format(record))

    def emit(self, record):
        #self.appended.emit(self.format(record))
        self.appended.emit(record)

    def addLogger(self, logger):
        if logger not in self.loggers:
            self.loggers.append(logger)
            logger.addHandler(self)

    def removeLogger(self, logger):
        if logger in self.loggers:
            self.loggers.remove(logger)
            logger.removeHandler(self)

    def setLevel(self, level, setLoggerLevels=True):
        super(QLoggerText, self).setLevel(level)
        if setLoggerLevels:
            for logger in self.loggers:
                logger.setLevel(level)


class QTextLogHandler(logging.Handler, core.QObject):
    appended = core.Signal(str)

    def __init__(self, text):
        core.QObject.__init__(self, parent=text)
        logging.Handler.__init__(self)
        self.text = text
        self.text.setReadOnly(True)
        self.appended.connect(self._appended)
        self.loggers = []
        self.currentThreadId = core.QThread.currentThreadId()

    def _appended(self, msg):
        self.text.append(msg)
        self.text.repaint()

    def emit(self, record):
        #self.appended.emit('%s %r' % (self.format(record),
        #self.currentThreadId))
        print repr(self.format(record))
        # self.appended.emit(self.format(record))
        self.appended.emit()

    def addLogger(self, logger):
        if logger not in self.loggers:
            self.loggers.append(logger)
            logger.addHandler(self)

    def removeLogger(self, logger):
        if logger in self.loggers:
            self.loggers.remove(logger)
            logger.removeHandler(self)

    def setLevel(self, level, setLoggerLevels=True):
        super(QTextLogHandler, self).setLevel(level)
        if setLoggerLevels:
            for logger in self.loggers:
                logger.setLevel(level)


logger1 = logging.getLogger('logger1')
logger1.setLevel(logging.DEBUG)


def process1():
    logger1.info('process1 starting')
    time.sleep(0.5)
    logger1.debug('process1 middle')
    time.sleep(1)
    logger1.warning('process1 finishing')


logger2 = logging.getLogger('logger2')
logger2.setLevel(logging.DEBUG)
logger2.addHandler(logging.StreamHandler(sys.stdout))


def process2():
    logger2.info('process2 starting')
    time.sleep(1)
    logger2.debug('process2 middle')
    time.sleep(1)
    logger2.warning('process2 finishing')


def process3():
    logger2.info('process3 starting')
    time.sleep(3)
    logger2.info('process3 finished')


class TestDialog(widgets.QWidget):
    def __init__(self):
        super(TestDialog, self).__init__()
        self.layout = widgets.QVBoxLayout(self)
        self.text = widgets.QTextEdit(self)
        self.logHandler = QTextLogHandler(self.text)
        # #self.logHandler = QLoggerText(self)
        self.logHandler.addLogger(logger1)
        self.logHandler.addLogger(logger2)
        self.logHandler.setLevel(logging.DEBUG)
        self.btn = widgets.QPushButton(self)
        self.btn.clicked.connect(self.do)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
        self.pool = ThreadPool(processes=10)

    def do(self):
        #self.pool.map_async(lambda x: process1(), range(3))
        process3()
        #self.pool.map_async(lambda x: process2(), range(3))


if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)
    dlg = TestDialog()
    dlg.show()
    app.exec_()
