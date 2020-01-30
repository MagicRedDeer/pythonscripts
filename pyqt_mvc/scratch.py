from PySide import QtGui, QtCore
import sys


app = QtGui.QApplication(sys.argv)
app.setStyle("plastique")


model = QtGui.QStandardItemModel()
widget = QtGui.QListView()
names = ["name" + str(i) for i in range(4)]

for name in names:
    item = QtGui.QStandardItem(name)
    item.setCheckState(QtCore.Qt.Checked)
    item.setCheckable(True)
    model.appendRow(item)

widget.setModel(model)

widget.show()

app.exec_()
