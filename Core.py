from PySide import QtGui, QtCore
import sys

import FileManager
import Timer
import Widgets
import Windows

from CoreObject import *

def main():
    App = QtGui.QApplication(sys.argv)
    MainWindow = Windows.createWindow()
    Core = CoreObject(App, MainWindow)

    BrowserBin = Widgets.BrowserBin(Core)
    MainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, BrowserBin)
    
    Timeline = Widgets.Timeline(Core)
    MainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, Timeline)
    #MainWindow.setCentralWidget(Timeline)
    
    Core.createNode('Clip')
    
    MainWindow.initUI()
    MainWindow.show()
    sys.exit(App.exec_())
if __name__ == '__main__':
    main()