from PySide import QtGui, QtCore

class BrowserBin(QtGui.QDockWidget):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(BrowserBin, self).__init__()
        
        cb = QtGui.QCheckBox('Show title', self)
        cb.toggle()
        cb.stateChanged.connect(Core.MainWindow.changeTitle)
        
        