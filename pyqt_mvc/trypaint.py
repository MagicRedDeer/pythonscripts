import site
import sys

sys.path.append(r'c:\Python27\Lib\site-packages')

from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *

class Widget(QWidget):

    def paintEvent(self, event):
        print 'painting'
        painter = QPainter(self)
        painter.drawLine(0,0,self.width(),self.height())


def main():
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
