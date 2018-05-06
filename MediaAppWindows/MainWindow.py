#===============================================================================
# @Author: Thomas McVay
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with PyQt Library
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
#    See LICENSE in the root directory of this library for copy of
#    GNU Lesser General Public License and other license details.
#===============================================================================

import sys

from PyQt import QtGui, QtCore, QtWidgets

import AppCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        AppCore.RegisterObject(self)
        
        #Get LayoutSettings
        self.defaultLayoutsPath = AppCore['AppDirectory']+'/'+'MainWindow_defaultLayouts.ini'
        self.userLayoutsPath = AppCore['AppDataDirectory']+'/'+'MainWindow_userLayouts.ini'
        self.layoutSettings = QtCore.QSettings(self.defaultLayoutsPath, QtCore.QSettings.IniFormat)
        #if os.path.exists(self.userLayoutsPath):
        #    self.layoutSettings = QtCore.QSettings(self.userLayoutsPath, QtCore.QSettings.IniFormat)
        
    def initUI(self):
    
        #CosmeticSettings
        self.setPalette(AppCore.App.palette())
        self.WindowFont = AppCore.AppPrefs['AppFont']
        self.setWindowTitle(AppCore.AppSettings['AppTitle'])
        self.setWindowIcon(QtGui.QIcon(AppCore.AppSettings['AppIcon']))   
        self.AllowNestedDocks
        self.ForceTabbedDocks
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)
        self.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.setDockNestingEnabled(True)
        
        #Menu Actions#
        exitAction = QtWidgets.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        restoreLayout = QtWidgets.QAction('Restore Layout 0', self)
        restoreLayout.setShortcut('Shift+F1')
        restoreLayout.setStatusTip('Restore Saved Layout')
        restoreLayout.triggered.connect(self.restoreLayoutN)
        
        saveLayout = QtWidgets.QAction('Save Layout 0', self)
        saveLayout.setShortcut('Ctrl+F1')
        saveLayout.setStatusTip('Save Layout')
        saveLayout.triggered.connect(self.saveLayoutN)
        
        prefsWindow = QtWidgets.QAction('Preferences', self)
        prefsWindow.setStatusTip('Edit Preferences')
        prefsWindow.triggered.connect(AppCore.PrefsWindow.show)
        
        
        #Menu Bar#
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        layoutMenu = menubar.addMenu('&Layout')
        layoutMenu.addAction(restoreLayout)
        layoutMenu.addAction(saveLayout)
        layoutMenu.addAction(prefsWindow)
             
        self.show()
        self.restoreLayoutN(0)
    
    def saveLayoutN(self, *args):
        if len(args) == 1:
            versionNum = int(args[0])
        else:
            versionNum = int(self.sender().text()[-1])
        print('Saving Layout', versionNum)
        self.layoutSettings.setValue("geometry"+str(versionNum), self.saveGeometry())
        self.layoutSettings.setValue("windowState"+str(versionNum), self.saveState())
    def restoreLayoutN(self, *args):
        if len(args) == 1:
            versionNum = int(args[0])
        else:
            versionNum = int(self.sender().text()[-1])
        print('Restoring Layout', versionNum)
        self.restoreGeometry(self.layoutSettings.value("geometry"+str(versionNum)))
        self.restoreState(self.layoutSettings.value("windowState"+str(versionNum)))
    def dockThisWidget(self, widget, dockArea = QtCore.Qt.RightDockWidgetArea):
        widgetName = widget.accessibleName()
        if widgetName == '':
            widgetName = type(widget).__name__
        dockWidget = QtWidgets.QDockWidget()
        dockWidget.setWidget(widget)
        dockWidget.setObjectName(widgetName)
        dockWidget.setWindowTitle(widgetName)
        self.addDockWidget(dockArea, dockWidget)
        
        #FLAW: A little funky to do this here, re-evaluate
        AppCore.RegisterObject(widget)
        
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', 
        'Are you sure you want to quit?', QtWidgets.QMessageBox.Yes |
        QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)        
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            quit()
        else:
            event.ignore()
