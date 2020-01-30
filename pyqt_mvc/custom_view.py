import sys
from Qt import QtGui, QtCore, QtWidgets


class DataModel(QtCore.QAbstractItemModel):
    headers = ("i", "i^2", "name", "comments")
    TupleRole = QtCore.Qt.UserRole
    DictRole = QtCore.Qt.UserRole + 1

    def __init__(self, data=None, parent=None):
        ''':type data: list'''
        QtCore.QAbstractItemModel.__init__(self, parent)
        if data:
            self._data = data[:]
        else:
            self._data = []

        self._start = 0

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.headers[section]
            else:
                return "data %d" % section

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index, role):

        row = index.row()
        column = index.column()
        c_key = self.headers[column]

        val = None

        if role == QtCore.Qt.EditRole:
            val = self._data[row][c_key]

        if role == QtCore.Qt.ToolTipRole:
            val = self.headers[column] + ' for ' + str(row)

        if role == QtCore.Qt.DisplayRole:
            val = self._data[row][c_key]

        if role == DataModel.TupleRole:
            val = tuple([self._data[row][self.headers[c]]
                         for c in range(len(self.headers))])

        if role == DataModel.DictRole:
            val = self._data[row].copy()

        return val

    def flags(self, index):
        val = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        if index.column() in [0, 2, 3]:
            val |= QtCore.Qt.ItemIsEditable
        return val

    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():

            row = index.row()
            column = index.column()

            if role == QtCore.Qt.EditRole:

                c_key = self.headers[column]
                if column == 0:
                    self._data[row][c_key] = int(value)
                    self._data[row][self.headers[1]] = int(value)**2
                    return True

                elif column in [2, 3]:
                    self._data[row][c_key] = value
                    return True

            if role == DataModel.TupleRole:

                data = self._data[row]
                try:
                    for idx, header in enumerate(self.headers):
                        if idx == 1:
                            self._data[row][header] = int(value[0])**2
                        elif idx == 0:
                            self._data[row][header] = int(value[idx])
                        else:
                            self._data[row][header] = value[idx]
                    return True
                except (ValueError, IndexError):
                    self._data[row] = data

            if role == DataModel.DictRole:
                try:
                    value = value.copy()
                    value[self.headers[1]] = value[self.headers[0]]**2
                    self._data[row] = value
                except (KeyError, ValueError):
                    pass

        return False

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position+rows-1)
        for i in range(rows):
            s = self._start + i
            self._data.append({'i': s,
                                         'i^2': s**2,
                                         'name': 'data%04d' % s,
                                         'comments': ''})
        self._start = self._start + i + 1
        self.endInsertRows()

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position+rows-1)
        for i in range(rows):
            self._data.remove(self._data[position])
        self.endRemoveRows()

    def columnCount(self, index):
        return len(self.headers)

    def index(self, row, column, parent):
        return self.createIndex(row, column, parent)

    def parent(self, index):
        return QtCore.QModelIndex()


class DataEditor(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super(DataEditor, self).__init__(parent=parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.edits = []

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        for key in DataModel.headers:
            widget = QtWidgets.QWidget()
            hlayout = QtWidgets.QHBoxLayout(widget)
            hlayout.setSpacing(0)
            hlayout.setContentsMargins(0, 0, 0, 0)
            label = QtWidgets.QLabel(key)
            edit = QtWidgets.QLineEdit()
            label.setMinimumSize(QtCore.QSize(50, 0))
            self.edits.append(edit)
            hlayout.addWidget(label)
            hlayout.addWidget(edit)
            self.layout.addWidget(widget)

    def setData(self, data):
        for i in range(len(DataModel.headers)):
            self.edits[i].setText(str(data[i]))

    def data(self):
        return [x.text() for x in self.edits]


class DataLabel(QtWidgets.QLabel):

    def data(self):
        return self.text().split(',')

    def setData(self, data):
        self.setText(','.join([str(x) for x in data]))


class DataView(QtWidgets.QAbstractItemView):

    def __init__(self, parent=None):
        super(DataView, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self.viewport())

    def visualRect(self, index):
        if len(self.selectionModel().selection().indexes()) != 1:
            return QtCore.QRect()
        if self.currentIndex() != index:
            return QtCore.QRect()
        return self.rect()

    def visualRegionForSelection(self, selection):
        '''
        :type selection: PyQt4.QtWidgets.QItemSelection
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
        pass


class DataDelegate(QtWidgets.QItemDelegate):

    def createEditor(self, parent, option, index):

        editor = DataEditor(parent)

        row = index.row()
        model = index.model()

        data = model.data(model.createIndex(row, 0), DataModel.TupleRole)
        editor.setData(data)

        return editor

    def setEditorData(self, editor, index):

        model = index.model()
        row = index.row()

        data = model.data(model.createIndex(row, 0), DataModel.TupleRole)
        editor.setData(data)

    def setModelData(self, editor, model, index):

        value = editor.data()
        model.setData(index, value, DataModel.TupleRole)

    def updateEditorGeometry(self, editor, option, index):
        # editor.setGeometry(option.rect)
        editor.setGeometry(option.rect.x(), option.rect.y(), 400, 100)

    def sizeHint(self, option, index):
        return QtCore.QSize(300, 100)


class DataView2(QtWidgets.QWidget):
    ''' Data View 2 '''

    def __init__(self, parent=None, model=None):
        super(DataView2, self).__init__(parent)
        self._model = None
        self._scrollArea = QtWidgets.QScrollArea(self)
        self._scrollArea.setBackgroundRole(QtGui.QPalette.Light)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self._scrollArea)
        self.widget = QtWidgets.QWidget()
        self.widget.setMinimumSize(QtCore.QSize(300, 300))
        self.widgetLayout = QtWidgets.QVBoxLayout()
        self._scrollArea.setWidget(self.widget)
        self.widget.setLayout(self.widgetLayout)
        self.setModel(model)
        self.populate()
        self.setLayout(layout)

    def setModel(self, model):
        if model is not None:
            if self._model:
                self._model.layoutChanged.disconnect(self.changed)
                self._model.dataChanged.disconnect(self.changed)
                self._model.rowsInserted.disconnect(self.changed)
            self._model = model
            self._model.layoutChanged.connect(self.changed)
            self._model.dataChanged.connect(self.changed)
            self._model.rowsInserted.connect(self.changed)
            self.populate()

    def model(self):
        return self._model

    def changed(self, *args):
        self.clear()
        self.populate()

    def populate(self):
        if self._model:
            self._editors = {}
            for row in range(self._model.rowCount()):
                index = self._model.createIndex(row, 0, None)
                data = self._model.data(index, self._model.TupleRole)
                editor = DataEditor(self)
                editor.setData(data)
                self._editors[index] = editor
                self.widgetLayout.addWidget(editor)
                self.widget.resize(self.sizeHint())
                size = DataEditor().sizeHint()
            self.widget.setMinimumSize(
                    QtCore.QSize(size.width(),
                                 size.height() * self._model.rowCount()))

    def clear(self):
        layout = self.widgetLayout
        for editor in self._editors.values():
            layout.removeWidget(editor)
            editor.deleteLater()


def main():
    # create App
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('plastique')

    # create Model
    model = DataModel()
    model.insertRows(0, 2)


    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    widget.setLayout(layout)

    splitter = QtWidgets.QSplitter()

    # create View
    listView = QtWidgets.QTableView()
    listView.setItemDelegate(DataDelegate())
    listView.setModel(model)

    # create view
    dataView = DataView2()
    dataView.setModel(model)

    splitter.addWidget(listView)
    splitter.addWidget(dataView)

    button = QtWidgets.QPushButton()
    button.setText('Hit ME')
    button.clicked.connect(lambda *args: model.insertRows(0, 2))

    layout.addWidget(button)
    layout.addWidget(splitter)

    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
