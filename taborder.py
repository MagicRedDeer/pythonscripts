import PyQt4.QtGui as gui
import PyQt4.QtCore as core
#import qtify_maya_window as qtfy
import sys

from functools import partial

#parent = qtfy.getMayaWindow()

def printme(k):
    print k


class MyDialog(gui.QDialog):
    def __init__(self, numBtns=5):
        super(MyDialog, self).__init__(parent=None)
        self.layout = gui.QVBoxLayout(self)
        self.btns = []
        self.edits = []
        for i in range(numBtns):
            edit = gui.QLineEdit()
            btn = gui.QPushButton()
            btn.clicked.connect(partial(printme, i))
            self.btns.append(btn)
            self.edits.append(edit)
            self.layout.addWidget(edit)
            self.layout.addWidget(btn)

        self.setLayout(self.layout)
        self.setFocusPolicy( core.Qt.StrongFocus)
        for i in reversed(range(numBtns)):
            if i >= 1:
                self.setTabOrder(self.btns[i-1], self.edits[i])
            self.setTabOrder(self.edits[i], self.btns[i])

app  = gui.QApplication(sys.argv)
win = MyDialog()
win.exec_()
