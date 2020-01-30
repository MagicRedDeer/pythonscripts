import Qt.QtWidgets as gui
import Qt.QtCore as core

import sys


kb  = core.Qt.KeyboardModifier()


class Dialog(gui.QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        self.layout = gui.QVBoxLayout(self)
        self.text = gui.QTextEdit(self)
        self.text.setEnabled(False)
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)

    def log(self, message):
        self.text.append(message)
        self.text.repaint()

    def keyPressEvent(self, event):
        self.log(event.text())

    def keyReleaseEvent(self, event):
        if event.text() == 'e' and event.modifiers() & core.Qt.AltModifier:
            self.log('edit')
        self.log(event.text())


if __name__ == '__main__':
    app = gui.QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    app.exec_()
