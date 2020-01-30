from PySide import QtGui, QtCore
import sys


class SingleItemView(QtGui.QAbstractItemView):

    def __init__(self, parent=None):
        super(SingleItemView, self).__init__(parent)

        layout = QtGui.QGridLayout(self.viewport())

        self.label = QtGui.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setSizePolicy(QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.label.setText("<i>No data.</i>")

        layout.addWidget(self.label)

    def visualRect(self, index):

        if len(self.selectionModel().selection().indexes()) != 1:
            return QtCore.QRect()

        if self.currentIndex() != index:
            return QtCore.QRect()

        return self.rect()

    def visualRegionForSelection(self, selection):
        '''
        :type selection: PyQt4.QtGui.QItemSelection
        '''
        if self.currentIndex() != selection.indexes()[0]:
            return QtCore.QRect()
        return self.rect()

    def isIndexHidden(self, index):
        if len(self.selectionModel().selection().indexes()) != 1:
            return True
        if self.currentIndex() != index:
            return True
        return False

    def indexAt(self, point):
        if len(self.selectionModel().selection().indexes()) != 1:
            return QtCore.QModelIndex()
        return self.currentIndex()

    def horizontalOffset(self):
        return self.horizontalScrollBar().value()

    def verticalOffset(self):
        return self.verticalScrollBar().value()

    def moveCursor(self, cursorAction, modifiers):
        return self.currentIndex()

    def setSelection(self, rect, flags):
        pass

    def scrollTo(self, index, hint):
        pass

    def dataChanged(self, topLeft, bottomRight):
        pass

    def selectionChanged(self, selected, deselected):
        self.updateText()

    def updateText(self):
        count = len(self.selectionModel().selection().indexes())

        if count == 0:
            self.label.setText("<i>No data.</i>")
        elif count == 1:
            self.label.setText(self.model().data(self.currentIndex()))
        else:
            self.label.setText(
                    "<i>Too Many Items Selected <br> Can only see 1</i>")


def main():
    app = QtGui.QApplication(sys.argv)

    table = QtGui.QTableView()
    selectionView = SingleItemView()

    splitter = QtGui.QSplitter()
    splitter.addWidget(table)
    splitter.addWidget(selectionView)

    model = QtGui.QStandardItemModel(5, 2)
    for r in range(5):
        for c in range(2):
            item = QtGui.QStandardItem("Row:%d, Column:%d" % (r, c))
            model.setItem(r, c, item)

    table.setModel(model)
    selectionView.setModel(model)

    selectionView.setSelectionModel(table.selectionModel())

    splitter.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
