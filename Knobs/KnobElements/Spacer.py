from PySide import QtGui, QtCore

class Spacer(QtGui.QWidget):
    def __init__(self):
        super(Spacer, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(0,0)
