from PyQt4.QtGui import ( QLayout, QSizePolicy, QDialog, QApplication,
        QPushButton, QHBoxLayout )
from PyQt4.QtCore import QSize, Qt, QRect, QPoint
import sys


class FlowLayout(QLayout):
    '''reimplements QLayout to adjust the elements in the avaible width in the window'''
    def __init__(self, parent=None, margin=0, spacing=-1):
        self.mysuper = super(FlowLayout, self)
        super(FlowLayout, self).__init__(parent)
        self.itemList = []
        self.setContentsMargins(0,0,0,0)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]
        return 0

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        self.mysuper.setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.margin(), 2 * self.margin())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0
        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton,
                    Qt.Horizontal )
            spaceY = self.spacing() + wid.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical
                    )
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0
            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
        return y + lineHeight - rect.y()


class Diag(QDialog):

    def __init__(self, num=10):
        super(Diag, self).__init__()
        self.layout = FlowLayout()
        self.setGeometry(self.geometry().x(), self.geometry().y(), 300, 200)
        # self.layout = QHBoxLayout()
        for x in range(num):
            self.layout.addWidget(QPushButton('button %d'%x))
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = Diag()
    d.show()
    app.exec_()
    sys.exit()



