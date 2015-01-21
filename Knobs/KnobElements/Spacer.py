from PySide import QtGui, QtCore

class Spacer(QtGui.QWidget):
    def __init__(self):
        super(Spacer, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
