from PyQt5 import QtCore, QtGui

class Graph(QtGui.QWidget):
    def __init__(self, data, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._data = data
        self.resize(400, 700)
        self.setWindowTitle('FSPwners')
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Base)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)

        screen_width = self.width()
        screen_height = self.height()

        # highest y = max_data_value * y_stretch
        y_stretch = 15
        # gap between lower canvas edge and x axis
        y_gap = 350
        # stretch enough to get all data items in
        x_stretch = 10
        x_width = 20
        # gap between left canvas edge and y axis
        x_gap = 20

        for x, y in enumerate(self._data):
            # calculate reactangle coordinates (integers) for each bar
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = screen_height - (y * y_stretch + y_gap)
            x1 = x0 + x_width
            y1 = screen_height - y_gap
            if y < 0:
                painter.setBrush(QtCore.Qt.red)
            else:
                painter.setBrush(QtCore.Qt.green)
            painter.drawRect(QtCore.QRectF(
                QtCore.QPointF(x0, y0), QtCore.QPointF(x1, y1)))
            print (x0, y0, x1, y1)

            # put the y value above each bar
            painter.drawText(x0 + 2, y0 - 2, str(y))

        painter.end()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    # data to be graphed
    data = [-20, 15, 10, 7, 5, -4, 3, 2, 1, 1, 0]
    window = Graph(data)
    window.show()
    sys.exit(app.exec_())
