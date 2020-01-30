import pymel.core as pc
import site
site.addsitedir(r'D:\talha.ahmed\workspace\pyenv_maya\maya2015\PyQt')


import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import sys

import time

class Dialog(gui.QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.layout = gui.QVBoxLayout(self)

        self.lineEdit = gui.QLineEdit()
        self.lineEdit.setEnabled(False)
        self.lineEdit.setValidator(gui.QRegExpValidator(core.QRegExp('[a-z0-9_]+')))
        #self.lineEdit.editingFinished.connect(self.finish)

        self.btn = gui.QPushButton()
        self.btn.setText('Edit')
        self.btn.clicked.connect(self.edit)

        self.box = gui.QDialogButtonBox(gui.QDialogButtonBox.Ok|gui.QDialogButtonBox.Cancel)
        self.box.accepted.connect(self.accepted)
        self.box.accepted.connect(self.accept)
        self.box.rejected.connect(self.reject)

        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.box)
        self.setLayout( self.layout )
        self.setTabOrder(self.box, self.btn)
        self.setTabOrder(self.lineEdit, self.btn)
        self.setTabOrder(self.btn, self.box)
        self.setFocusPolicy(core.Qt.StrongFocus)
        self.box.button(gui.QDialogButtonBox.Ok).setDefault(False)



    def finish(self, *args):
        print 'finishing ....'
        print self.lineEdit.text()
        self.lineEdit.setEnabled(False)
        self.btn.setFocus()
        #self.box.button(gui.QDialogButtonBox.Ok).setDefault(True)
        #self.box.accepted.connect(self.accept)

    def edit(self, *args):
        self.lineEdit.setEnabled(True)
        self.lineEdit.setFocus()
        self.box.button(gui.QDialogButtonBox.Ok).setDefault(False)
        #self.box.accepted.disconnect()

    def accepted(self                    ):
        print 'accepting ...'
        time.sleep(2)

    def keyPressEvent(self, event):
        if event.key() == core.Qt.Key_Enter:
            if not self.lineEdit.isEnabled():
                self.box.accepted.emit()
            else:
                self.finish()
        else:
            print event.key()
            super(Dialog, self).keyPressEvent(event)

app = gui.QApplication(sys.argv)
diag = Dialog()
diag.show()
app.exec_()

