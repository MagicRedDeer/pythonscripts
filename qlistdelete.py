import sip
import sys

sip.setapi('QString', 2)

if True:
    from PyQt4 import QtGui


class Diag(QtGui.QDialog):
    def __init__(self):
        super(Diag, self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.list = QtGui.QListWidget()
        self.list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.addBtn = QtGui.QPushButton('add')
        self.removeBtn = QtGui.QPushButton('remove')
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.addBtn)
        self.layout.addWidget(self.removeBtn)
        self.setLayout(self.layout)

        self.idx = 0

        self.addBtn.clicked.connect(self.add)
        self.removeBtn.clicked.connect(self.remove)

    def add(self):
        self.idx += 1
        self.list.addItem('item%d' % self.idx)

    def remove(self):
        for item in self.list.selectedItems():
            idx = self.list.row(item)
            self.list.takeItem(idx)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    diag = Diag()
    diag.show()
    app.exec_()
