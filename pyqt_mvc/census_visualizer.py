import sys
import random
from Qt import QtCore, QtGui, QtWidgets


class CensusVisualizerView(QtWidgets.QWidget):

    clicked = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, parent):
        super(CensusVisualizerView, self).__init__(parent)

        self.visualizer = self.parent()
        assert(self.visualizer)

        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setMinimumSize(self.minimumSizeHint())

    def minimumSizeHint(self):
        return QtCore.QSize(self.visualizer.widthOfYearColumn() +
                            self.visualizer.maleFemaleHeaderTextWidth() +
                            self.visualizer.widthOfTotalColumn(),
                            QtGui.QFontMetrics(self.font()).height() +
                            self.visualizer.ExtraHeight)

    def sizeHint(self):
        rows = (self.visualizer.model().rowCount()
                if self.visualizer.model() else 1)
        return QtCore.QSize(
                (self.visualizer.widthOfYearColumn() +
                    max(100, self.visualizer.maleFemaleHeaderTextWidth()) +
                    self.visualizer.widthOfTotalColumn()),
                self.visualizer.yOffsetForRow(rows))

    def eventFilter(self, target, event):
        scrollArea = self.visualizer.scrollArea()
        if scrollArea is not None:
            if target == scrollArea and event.type() == QtCore.QEvent.Resize:
                size = event.size()
                size.setHeight(self.sizeHint().height())
                width = size.width() - (
                        self.visualizer.ExtraWidth +
                        scrollArea.verticalScrollBar().sizeHint().width())
                size.setWidth(width)
                self.resize(size)
        return super(CensusVisualizerView, self).eventFilter(target, event)

    def mousePressEvent(self, event):
        row = int(event.y()/(QtGui.QFontMetrics(self.font()).height() +
                             self.visualizer.ExtraHeight))
        column = 0
        if event.x() < self.visualizer.widthOfYearColumn():
            column = self.visualizer.Year
        elif event.x() < (self.visualizer.widthOfYearColumn() +
                          self.visualizer.widthOfMaleFemaleColumn()/2):
            column = self.visualizer.Males
        elif event.x() < (self.visualizer.widthOfYearColumn() +
                          self.visualizer.widthOfMaleFemaleColumn()):
            column = self.visualizer.Females
        else:
            column = self.visualizer.Total

        self.visualizer.setSelectedRow(row)
        self.visualizer.setSelectedColumn(column)
        self.clicked.emit(self.visualizer.model().index(row, column))

    def keyPressEvent(self, event):
        if self.visualizer.model():
            row = -1
            column = -1
            if event.key() == QtCore.Qt.Key_Up:
                column = self.visualizer.selectedColumn()
                if (column == self.visualizer.Males or
                        column == self.visualizer.Females):
                    column -= 1
                elif column == self.visualizer.Females:
                    column = self.visualizer.Females
            elif event.key() == QtCore.Qt.Key_Up:
                row = max(0, self.visualizer.selectedRow() - 1)
            elif event.key() == QtCore.Qt.Key_Down:
                row = min(self.visualizer.selectedRow() + 1,
                          self.visualizer.model().rowCount() - 1)
            row = self.visualizer.selectedRow() if row == -1 else row
            column = (self.visualizer.selectedColumn() if column == -1 else
                      column)

            if (row != self.visualizer.selectedRow() and column !=
                    self.visualizer.selectedColumn()):
                index = self.visualizer.model().index(row, column)
                self.visualizer.setCurrentIndex(index)
                self.clicked.emit(index)
                return

        super(CensusVisualizerView, self).keyPressEvent(event)

    def paintEvent(self, event):
        if self.visualizer.model() is None:
            return
        fm = QtGui.QFontMetrics(self.font())
        rowHeight = fm.height() + self.visualizer.ExtraHeight
        minY = max(0, event.rect().y() - rowHeight)
        maxY = minY + event.rect().height() + rowHeight

        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing |
                               QtGui.QPainter.TextAntialiasing)

        row = minY / rowHeight
        y = row * rowHeight

        for row in range(self.visualizer.model().rowCount()):
            self.paintRow(painter, row, y, rowHeight)
            y += rowHeight
            if y > maxY:
                break

    def paintRow(self, painter, row, y, rowHeight):
        self.paintYear(
                painter, row, QtCore.QRect(
                    0,
                    y,
                    self.visualizer.widthOfYearColumn(),
                    rowHeight))
        self.paintMaleFemale(
                painter, row, QtCore.QRect(
                    self.visualizer.widthOfYearColumn(),
                    y,
                    self.visualizer.widthOfMaleFemaleColumn(),
                    rowHeight))
        self.paintTotal(
                painter, row, QtCore.QRect(
                    (self.visualizer.widthOfYearColumn() +
                        self.visualizer.widthOfMaleFemaleColumn()),
                    y,
                    self.visualizer.widthOfTotalColumn(),
                    rowHeight))

    def paintYear(self, painter, row, rect):
        self.paintItemBackground(
                painter, rect,
                (row == self.visualizer.selectedRow() and
                    self.visualizer.selectedColumn() == self.visualizer.Year))
        painter.drawText(
                QtCore.QRectF(rect),
                self.visualizer.model().data(
                    self.visualizer.model().index(row, self.visualizer.Year)),
                QtGui.QTextOption(QtCore.Qt.AlignCenter))

    def paintItemBackground(self, painter, rect, selected):
        painter.fillRect(rect, self.palette().highlight().color() if selected
                         else self.palette().button().color())
        self.visualizer.paintItemBorder(painter, self.palette(), rect)
        painter.setPen(self.palette().highlightedText().color() if selected
                       else self.palette().windowText().color())

    def paintTotal(self, painter, row, rect):
        self.paintItemBackground(
                painter, rect,
                (row == self.visualizer.selectedRow() and
                    self.visualizer.selectedColumn() == self.visualizer.Total))
        painter.drawText(
                QtCore.QRectF(rect),
                self.visualizer.model().data(
                    self.visualizer.model().index(row, self.visualizer.Total)),
                QtGui.QTextOption(QtCore.Qt.AlignCenter))

    def paintMaleFemale(self, painter, row, rect):
        rectangle = QtCore.QRect(rect)
        locale = QtCore.QLocale()
        males, _ = locale.toInt(self.visualizer.model().data(
            self.visualizer.model().index(row, self.visualizer.Males)))
        females, _ = locale.toInt(self.visualizer.model().data(
            self.visualizer.model().index(row, self.visualizer.Females)))
        total, _ = locale.toInt(self.visualizer.model().data(
            self.visualizer.model().index(row, self.visualizer.Total)))
        offset = round((
            1 -
            (float(total) / self.visualizer.maximumPopulation()))/2 *
                       rectangle.width())
        painter.fillRect(rectangle,
                         (self.palette().highlight().color() if (
                             row == self.visualizer.selectedColumn() and
                             (self.visualizer.selectedColumn() or
                                 self.visualizer.selectedRow()))
                             else self.palette().base().color()))
        self.visualizer.paintItemBorder(painter, self.palette(), rectangle)
        rectangle.setLeft(rectangle.left() + offset)
        rectangle.setRight(rectangle.right() - offset)
        rectY = rectangle.center().y()
        painter.fillRect(
                rectangle.adjusted(0, 1, 0, -1),
                self.maleFemaleGradient(
                    rectangle.left(), rectY, rectangle.right(), rectY,
                    float(males)/total))

    def maleFemaleGradient(self, x1, y1, x2, y2, crossOver):
        gradient = QtGui.QLinearGradient(x1, y1, x2, y2)
        maleColor = QtGui.QColor(QtCore.Qt.green)
        femaleColor = QtGui.QColor(QtCore.Qt.red)
        gradient.setColorAt(0, maleColor.darker())
        gradient.setColorAt(crossOver - 0.001, maleColor.lighter())
        gradient.setColorAt(crossOver + 0.001, femaleColor.lighter())
        gradient.setColorAt(1, femaleColor.darker())
        return gradient


class CensusVisualizerHeader(QtWidgets.QWidget):

    def minimumSizeHint(self):
        visualizer = self.parent()
        assert(visualizer)
        return QtCore.QSize(visualizer.widthOfYearColumn() +
                            visualizer.maleFemaleHeaderTextWidth() +
                            visualizer.widthOfTotalColumn(),
                            QtGui.QFontMetrics(self.font()).height() +
                            visualizer.ExtraHeight)

    def sizeHint(self):
        return self.minimumSizeHint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.rect().center()
        painter.setRenderHints(QtGui.QPainter.Antialiasing |
                               QtGui.QPainter.TextAntialiasing)
        self.paintHeader(painter, self.height())
        painter.setPen(
                QtGui.QPen(self.palette().button().color().darker(), 0.5))
        painter.drawRect(0, 0, self.width(), self.height())

    def paintHeader(self, painter, rowHeight):
        visualizer = self.parent()
        assert(visualizer)

        padding = visualizer.Padding

        self.paintHeaderItem(
            painter,
            QtCore.QRect(0, 0, visualizer.widthOfYearColumn() + padding,
                         rowHeight),
            visualizer.model().headerData(visualizer.Year,
                                          QtCore.Qt.Horizontal),
            visualizer.selectedColumn() == visualizer.Year)

        self.paintHeaderItem(
            painter,
            QtCore.QRect(
                visualizer.widthOfYearColumn() + padding, 0,
                visualizer.widthOfMaleFemaleColumn(), rowHeight),
            visualizer.maleFemaleHeaderText(),
            (visualizer.selectedColumn() == visualizer.Males or
                visualizer.selectedColumn() == visualizer.Females)),

        self.paintHeaderItem(
            painter,
            QtCore.QRect(
                (visualizer.widthOfYearColumn() + padding * 2 +
                    visualizer.widthOfMaleFemaleColumn()),
                0,
                visualizer.widthOfTotalColumn(),
                rowHeight),
            visualizer.model().headerData(
                visualizer.Total, QtCore.Qt.Horizontal),
            visualizer.selectedColumn() == visualizer.Total)

    def paintHeaderItem(self, painter, rect, text, selected):
        visualizer = self.parent()
        assert(visualizer)

        x = rect.center().x()
        gradient = QtGui.QLinearGradient(x, rect.top(), x, rect.bottom())
        color = (self.palette().highlight().color() if selected else
                 self.palette().button().color())
        gradient.setColorAt(0, color.darker(125))
        gradient.setColorAt(0.5, color.lighter(125))
        gradient.setColorAt(1, color.darker(125))
        painter.fillRect(rect, gradient)
        visualizer.paintItemBorder(painter, self.palette(), rect)

        painter.setPen(self.palette().highlightedText().color() if selected
                       else self.palette().buttonText().color())
        painter.drawText(QtCore.QRectF(rect), text,
                         QtGui.QTextOption(QtCore.Qt.AlignCenter))


class CensusVisualizer(QtWidgets.QWidget):

    Year = 0
    Males = 1
    Females = 2
    Total = 3

    ExtraWidth = 5
    ExtraHeight = 5

    Padding = 2

    clicked = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(CensusVisualizer, self).__init__(parent)

        self._model = None
        self._maximumPopulation = -1
        self._selectedRow = -1
        self._selectedColumn = -1

        fm = QtGui.QFontMetrics(self.font())
        self._widthOfYearColumn = fm.width("W9999W")
        self._widthOfTotalColumn = fm.width("W9,999,999W")

        self._view = CensusVisualizerView(self)
        self._header = CensusVisualizerHeader(self)

        self._scrollArea = QtWidgets.QScrollArea()
        self._scrollArea.setBackgroundRole(QtGui.QPalette.Light)
        self._scrollArea.setWidget(self._view)
        self._scrollArea.installEventFilter(self._view)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._header)
        layout.addWidget(self._scrollArea)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self._view.clicked.connect(self.clicked)

    def model(self):
        return self._model

    def _determineMaximumPopulation(self, model=None):
        if model is None:
            model = self.model()

        self._maximumPopulation = -1
        locale = QtCore.QLocale()
        for row in range(model.rowCount()):
            total, _ = locale.toInt(model.data(model.index(row,
                                    CensusVisualizer.Total)))
            if total > self._maximumPopulation:
                self._maximumPopulation = total

                population = str(total)
                population = '%d%s' % (
                    int(population[0])+1, (len(population) - 1) * '0')

            self._maximumPopulation = int(population)

            fm = QtGui.QFontMetrics(self.font())
            self._widthOfTotalColumn = fm.width("W%s%sW" % (
                population, len(population)/3 * ','))

    def setModel(self, model):
        ''':type model: PyQt4.QtGui.QAbstractItemModel'''
        if model:
            if self._model:
                self._model.rowsInserted.disconnect(self.changeOfData)

            self._determineMaximumPopulation(model)

        self._model = model
        self._model.rowsInserted.connect(self.changeOfData)
        self._header.update()
        self._view.update()

    def changeOfData(self, *args):
        self._determineMaximumPopulation(self._model)
        self._scrollArea.repaint()
        self._view.update()

    def scrollArea(self):
        return self._scrollArea

    def maximumPopulation(self):
        return self._maximumPopulation

    def widthOfYearColumn(self):
        return self._widthOfYearColumn

    def widthOfMaleFemaleColumn(self):
        return self.width() - (
                self._widthOfYearColumn +
                self._widthOfTotalColumn + self.ExtraWidth +
                self._scrollArea.verticalScrollBar().sizeHint().width())

    def widthOfTotalColumn(self):
        return self._widthOfTotalColumn

    def selectedRow(self):
        return self._selectedRow

    def selectedColumn(self):
        return self._selectedColumn

    def setSelectedRow(self, row):
        self._selectedRow = row
        self._view.update()

    def setSelectedColumn(self, column):
        self._selectedColumn = column
        self._view.update()

    def paintItemBorder(self, painter, palette, rect):
        painter.setPen(QtGui.QPen(palette.button().color().darker(), 0.33))
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        painter.drawLine(rect.bottomRight(), rect.topRight())

    def maleFemaleHeaderText(self):
        if not self._model:
            return " - "
        return ('%s - %s' % (self._model.headerData(
            CensusVisualizer.Males, QtCore.Qt.Horizontal),
            self._model.headerData(CensusVisualizer.Females, QtCore.Qt.Horizontal)))

    def maleFemaleHeaderTextWidth(self):
        return QtGui.QFontMetrics(self.font()).width(
                self.maleFemaleHeaderText())

    def xOffsetForMiddleOfColumn(self, column):
        if column == CensusVisualizer.Year:
            return self.widthOfYearColumn()
        if column == CensusVisualizer.Males:
            return self.widthOfYearColumn() + (
                    self.widthOfMaleFemaleColumn() / 4)
        if column == CensusVisualizer.Females:
            return self.widthOfYearColumn() + (
                    (self.widthOfMaleFemaleColumn() * 4) / 3)
        if column == CensusVisualizer.Total:
            return (self.widthOfYearColumn() + self.widthOfMaleFemaleColumn() +
                    self.widthOfTotalColumn() / 2)

    def yOffsetForRow(self, row):
        fm = QtGui.QFontMetrics(self.font())
        return int((fm.height() + self.ExtraHeight) * row)

    def setCurrentIndex(self, index):
        self.setSelectedRow(index.row())
        self.setSelectedColumn(index.column())
        x = self.xOffsetForMiddleOfColumn(index.column())
        y = self.yOffsetForRow(index.row())
        self._scrollArea.ensureVisible(x, y, 10, 20)


class CensusModel(QtCore.QAbstractItemModel):
    headers = ('Year', 'Males', 'Females', 'Total')

    def __init__(self, parent=None):
        super(CensusModel, self).__init__(parent)

        self._data = []
        self.start_year = 1940
        self.start_total = 1000
        self.year_inc = 10
        self.min_inc = 50
        self.max_inc = 100
        for row in range(10):
            self._addRow()

    def _addRow(self, position=None):
        year = self.start_year + self.year_inc
        inc = random.randint(self.min_inc, self.max_inc)
        total = self.start_total + inc
        half = int(total/2)
        males = half + random.randint(0, inc)
        females = total - males
        data = (str(year), str(males), str(females), str(total))

        if position is None:
            self._data.append(data)
        else:
            self._data.insert(position, data)

        self.start_year = year
        self.start_total = total

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.DisplayRole and index.isValid():
            row = index.row()
            column = index.column()
            try:
                return self._data[row][column]
            except IndexError:
                return '0'

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def index(self, row, column, parent=QtCore.QModelIndex()):
        return super(CensusModel, self).createIndex(row, column)

    def headerData(self, index, direction, role=QtCore.Qt.DisplayRole):
        if index < len(self.headers):
            return self.headers[index]

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):

        self.beginInsertRows(parent, position, position+rows-1)

        for i in range(position, position+rows):
            self._addRow(i)

        self.endInsertRows()

    def parent(self, index):
        return QtCore.QModelIndex()


def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    btn = QtWidgets.QPushButton(widget)
    btn.setText('Add')
    splitter = QtWidgets.QSplitter(widget)
    layout.addWidget(btn)
    layout.addWidget(splitter)
    widget.setLayout(layout)
    vis = CensusVisualizer()
    model = CensusModel()
    btn.clicked.connect(lambda *args: model.insertRows(10, 5))
    vis.setModel(model)
    table = QtWidgets.QTableView(widget)
    table.setModel(model)
    splitter.addWidget(vis)
    splitter.addWidget(table)
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
