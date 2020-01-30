import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui
# from PySide import QtGui


def func(*args):
    print args

app = QtGui.QApplication([])
win = QtGui.QCheckBox()
win.clicked[bool].connect(func)
win.show()

app.exec_()


