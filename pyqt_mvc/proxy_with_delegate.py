import sys
from PySide2 import QtCore, QtGui, QtWidgets

_data = {
        {'Name': 'Rania', 'age': 7, 'class': '3'},
        {'Name': 'Rahma', 'age': 3, 'class': 'Montessori'},
        {'Name': 'Nabiha', 'age': 1, 'class': None},
        {'Name': 'Fatima', 'age': 3, 'class': 'Playgroup'},
}



class Editor(QtWidgets.QListWidget):

    def __init__(self, parent=None, data=None):
        self.setParent(parent)
        self.nameLabel = QtWidgets.QLabel(self)
        self.ageLabel = QtWidgets.QLabel(self)
        self.classLabel = QtWidgets.QLabel(self)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.ageLabel)
        self.layout.addWidget(self.classLabel)
        if data is not None:
            self.setData(data)

    def setData(self, data):
        self.nameLabel.setText(data['Name'])
        self.ageLabel.setText(data['age'])
        self.classLabel.setText(data['class'])


class MyModel(QtCore.QAbstractListModel):
    def __init__(self, data):
        super().__init__()
        self.data = data


class MyDelegate(QtWidgets.QAbstractItemDelegate):
    pass


if __name__ == "__main__":
    _app = QtGui.QGuiApplication(sys.argv)
    view = QtWidgets.QListView(sys.argv)
