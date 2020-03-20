from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets


class ThreshWidget(QtWidgets.QSpinBox):

    def __init__(self, value=5):
        super(ThreshWidget, self).__init__()
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.setRange(5, 100)
        self.setSuffix(' %')
        self.setValue(value)
        self.setToolTip('Detect Threshold')
        self.setStatusTip(self.toolTip())
        self.setAlignment(QtCore.Qt.AlignCenter)

    def minimumSizeHint(self):
        height = super(ThreshWidget, self).minimumSizeHint().height()
        fm = QtGui.QFontMetrics(self.font())
        width = fm.width(str(self.maximum()))
        return QtCore.QSize(width, height)
