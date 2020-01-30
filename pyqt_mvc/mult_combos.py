import sip
sip.setapi('QVariant', 2)
sip.setapi('QString', 2)
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

import sys


class Dialog(gui.QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        self.layout = gui.QVBoxLayout(self)
        self.text = gui.QTextEdit(self)
        self.text.setEnabled(False)
        self.c1 = gui.QComboBox(self)
        self.c2 = gui.QComboBox(self)
        self.c1.activated.connect(self.c1changed)
        self.c2.activated.connect(self.c2changed)
        self.populatec1()
        self.char = self.c1.currentText()
        self.populatec2()
        self.char2 = self.c2.currentText()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.c1)
        self.layout.addWidget(self.c2)
        self.setLayout(self.layout)

    def log(self, message):
        self.text.append(message)
        self.text.repaint()

    def c1changed(self, *args):
        if self.char == self.c1.currentText():
            return
        self.char = self.c1.currentText()
        self.log('c1changed')
        self.populatec2()

    def populatec1(self):
        self.c1.clear()
        map(lambda x: self.c1.addItem(x), 'abcd')
        self.c2.setCurrentIndex(0)

    def populatec2(self):
        self.c2.clear()
        map(lambda x: self.c2.addItem(x[0]*x[1]), [(self.c1.currentText(), i) for
            i in range(2, 5)])

    def c2changed(self, *args):
        if self.char2 == self.c2.currentText():
            return
        self.char2 == self.c2.currentText()
        self.log('c2changed')

if __name__ == '__main__':
    app = gui.QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    app.exec_()



