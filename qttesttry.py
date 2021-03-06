#!"c:\Program Files\Autodesk\Maya2016\bin\mayapy.exe"
import sys
sys.path.insert(0, r'D:\talha.ahmed\workspace\pyenv_common\utilities')

from uiContainer import _setPySide
_setPySide()

from PyQt4.QtTest import QTest
from PyQt4 import QtCore, QtGui, QtTest

print QtCore
print QtGui
print QtTest 
import sys
import unittest
import time

app = None

def reverse(stuff, gui=False):
    ''':type stuff: str'''
    if gui:
        time.sleep(1)
    if stuff == "secret":
        return "NOOO!"
    return ''.join( stuff[::-1] )

class ReverseGui(QtGui.QDialog):
    '''String reversal GUI'''

    def __init__(self, parent=None):
        super(ReverseGui, self).__init__(parent=parent)
        self.layout = QtGui.QVBoxLayout()
        self.lineEdit = QtGui.QLineEdit()
        self.label = QtGui.QLabel()
        self.reverseBtn = QtGui.QPushButton("Reverse")
        self.cancelBtn = QtGui.QPushButton("Cancel")

        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.reverseBtn)
        self.layout.addWidget(self.cancelBtn)
        self.setLayout(self.layout)

        self.reverseBtn.clicked.connect(self.reverse)
        self.cancelBtn.clicked.connect(self.reject)

    def reverse(self):
        text = self.lineEdit.text()
        new_text = reverse(text)
        self.label.setText(new_text)

def main():
    win = ReverseGui()
    win.show()
    app.exec_()

class TestReverse(unittest.TestCase):
    '''Testing Without Gui'''

    def testHello(self):
        self.assertEqual(reverse("Hello"), "olleH")

    def testSecret(self):
        self.assertEqual(reverse("secret"), "NOOO!")

    def testEmpty(self):
        self.assertEqual(reverse(""), "")

class TestReverseGui(unittest.TestCase):
    '''Testing With Gui'''

    def setUp(self):
        self.gui = ReverseGui()

    def tearDown(self):
        self.gui.hide()
        self.gui.deleteLater()

    def testEmpty(self):
        self.gui.show()
        QTest.keyClicks(self.gui.lineEdit, "")
        QTest.mouseClick(self.gui.reverseBtn, QtCore.Qt.LeftButton)
        self.assertEqual(self.gui.label.text(), "")

    def testHello(self):
        self.gui.show()
        QTest.keyClicks(self.gui.lineEdit, "Hello")
        QTest.mouseClick(self.gui.reverseBtn, QtCore.Qt.LeftButton)
        self.assertEqual(self.gui.label.text(), "olleH")

    def testSecret(self):
        self.gui.show()
        QTest.keyClicks(self.gui.lineEdit, "secret")
        QTest.mouseClick(self.gui.reverseBtn, QtCore.Qt.LeftButton)
        self.assertEqual(self.gui.label.text(), "NOOO!")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    unittest.main()
