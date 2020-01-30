import Qt.QtGui as gui
import Qt.QtCore as core
import Qt.QtWidgets as widgets

import sys


class Dialog(widgets.QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        self.layout = widgets.QVBoxLayout(self)
        self.expandBtn = widgets.QPushButton(self)
        self.expandBtn.clicked.connect(self.expand)
        self.shrinkBtn = widgets.QPushButton(self)
        self.shrinkBtn.clicked.connect(self.shrink)
        self.text = widgets.QTextEdit(self)
        self.text.setEnabled(False)
        self.layout.addWidget(self.expandBtn)
        self.layout.addWidget(self.shrinkBtn)
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)
        self.log('%r'%self.sizePolicy().verticalPolicy())
        self.log('%r'%self.sizePolicy().horizontalPolicy())

    def log(self, message):
        self.text.append(message)
        self.text.repaint()

    def shrink(self):
        self.resize(self.width(), self.height() - 10)
        self.log('shrinking')

    def expand(self):
        self.resize(self.width(), self.height()+10)
        self.log('expanding ...')


if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    app.exec_()

