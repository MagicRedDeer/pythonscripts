import sip

sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

if True:
    import PyQt4.QtGui as gui

    import sys


class Dialog(gui.QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        self.layout = gui.QVBoxLayout(self)
        self.tree = gui.QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.layout.addWidget(self.tree)

        self.populate()

    def populate(self):
        for i in range(10):
            item = gui.QTreeWidgetItem(self.tree)
            item.setText(0, str(i+1))
            item.setCheckState(0, True)
            box = gui.QComboBox(self)
            box.addItems([str(x) for x in range(i)])
            self.tree.setItemWidget(item, 1, box)
            self.tree.addTopLevelItem(item)


if __name__ == '__main__':
    app = gui.QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    app.exec_()
