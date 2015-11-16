from PyQt4 import QtGui, QtCore

# a progress bar widget that is separated in several sub-processes.
# It can be used to better illustrate a multi-step process
class MinimalBarChart(QtGui.QWidget):
    def __init__(self, blockSize=3, maxYValue=100):
        super(MinimalBarChart, self).__init__()
        self.blockSize=3
        self.maxYValue=maxYValue
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 5)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()

        pen = QtGui.QPen(QtGui.QColor("Orange"), 0, QtCore.Qt.NoPen)

        qp.setPen(pen)

        for until in sorted(self.untils.keys(), reverse=True):
            qp.setBrush(QtGui.QColor(self.untils[until]))
            if (self.maxV - self.minV) <= 0:
                pass
            else:
                qp.drawRect(0, 0, w * min(1. * (self.value - self.minV) / (self.maxV - self.minV), until), h)


        for until in sorted(self.untils.keys(), reverse=True):
            qp.setBrush(QtGui.QColor(self.untils[until]))
            qp.drawRect(0, h-1, w * min(1. * (1. - self.minV) / (1. - self.minV), until), h)
