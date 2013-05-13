#===============================================================================
# @Author: Thomas McVay
# @Version: 0.1
# @LastModified: 130511
# @Description: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with PySide Library
#    Copyright (C) 2013 Thomas McVay
#    
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License version 2.1 as published by the Free Software Foundation;
#    
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#    See MediaApp_LGPL.txt in the root directory of this library for copy of
#    GNU Lesser General Public License and other license details.
#===============================================================================

from PySide import QtGui, QtCore

class PropertiesBin(QtGui.QWidget):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(PropertiesBin, self).__init__()
        #self.setAccessibleName('PropertiesBin')   #override visible name here
        ##################################
        
        self.binLayout = QtGui.QVBoxLayout()
        cb1 = QtGui.QPushButton("One",self)
        cb2 = QtGui.QPushButton("Two",self)
        self.binLayout.addWidget(cb1)
        self.binLayout.addWidget(cb2)
        self.setLayout(self.binLayout)
        
class MainWindow(QtGui.QMainWindow):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(MainWindow, self).__init__()
        ################################
        
    def initUI(self):
        #self.WindowFont = QtGui.QFont('Courier')
        #self.WindowFont.setPixelSize(16)
        #self.WindowFontMetrics = QtGui.QFontMetrics(self.WindowFont)
        
        #self.AllowNestedDocks
        self.ForceTabbedDocks
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtGui.QTabWidget.North)
        self.setTabShape(QtGui.QTabWidget.Triangular)
        self.setDockNestingEnabled(True)
        
        #ToolBar#
        #toolbar = self.addToolBar('Exit')
        #toolbar.addAction(exitAction)
        #/ToolBar#
    
    def dockThisWidget(self, widget, dockArea = QtCore.Qt.RightDockWidgetArea):
        widgetName = widget.accessibleName()
        if widgetName == '':
            widgetName = type(widget).__name__
        dockWidget = QtGui.QDockWidget()
        dockWidget.setWidget(widget)
        dockWidget.setObjectName(widgetName)
        dockWidget.setWindowTitle(widgetName)
        self.addDockWidget(dockArea, dockWidget)
    
    def changeTitle(self, state):
        if state == QtCore.Qt.Checked:
            self.setWindowTitle('Checkbox')
        else:
            self.setWindowTitle('')