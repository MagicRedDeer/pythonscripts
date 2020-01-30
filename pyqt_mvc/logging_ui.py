

import sip
sip.setapi('QVariant', 2)
sip.setapi('QString', 2)
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

import time
import sys
import logging
import testprocess


from multiprocessing.pool import ThreadPool


class DialogHandler(logging.Handler):
    def __init__(self, log):
        super(DialogHandler, self).__init__()
        self.log = log
        self.setFormatter(logging.Formatter())

    def emit(self, record):
        '''
        :type record: logging
        '''
        self.log(self.format(record))


class Dialog(gui.QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        self.layout = gui.QVBoxLayout(self)
        self.btn = gui.QPushButton(self)
        self.btn.clicked.connect(self.work)
        self.text = gui.QTextEdit(self)
        self.text.setEnabled(True)
        self.text.setReadOnly(True)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
        self.handler = DialogHandler(self.log)
        self.logger = logging.getLogger(__name__ + '.Dialog')
        self.handler.setLevel(logging.DEBUG)
        logging.getLogger(testprocess.__name__).addHandler(self.handler)
        self.logger.addHandler(self.handler)
        self.logger.error('error')
        self.logger.debug('debug')
        self.pool = ThreadPool(processes=5)

    def work(self):
        self.pool.map_async(lambda x: testprocess.work(), range(10))

    def log(self, message):
        self.text.append(message)
        self.text.repaint()


if __name__ == '__main__':
    app = gui.QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    app.exec_()

