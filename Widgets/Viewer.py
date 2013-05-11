from PySide import QtGui, QtCore

class Viewer(QtGui.QDockWidget):
    def __init__(self):
        super(Viewer, self).__init__()
        
        cb = QtGui.QCheckBox('Show title', self)
        #cb.toggle()
        #cb.stateChanged.connect(self.changeTitle)