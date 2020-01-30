import Qt.QtWidgets as gui

import time
import sys


class Dialog(gui.QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        self.layout = gui.QVBoxLayout(self)
        self.btn = gui.QPushButton(self)
        self.defaultAction = self.doNothing
        self.btn.clicked.connect(self.defaultActionWrapper)
        self.defaultAction = self.work
        self.text = gui.QTextEdit(self)
        self.text.setEnabled(False)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

    def doNothing(self):
        self.log('do Nothing')

    def defaultActionWrapper(self):
        self.defaultAction()

    def work(self):
        self.log('<b>starting</b>')
        time.sleep(1)
        self.log('<i>step 1 done</i>')
        time.sleep(1)
        self.log('<em>step 2 done</em>')

    def log(self, message):
        self.text.append(message)
        self.text.repaint()


if __name__ == '__main__':
    app = gui.QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    app.exec_()
