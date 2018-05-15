#===============================================================================
# @Author: Thomas McVay
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with Qt Library
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
from collections import OrderedDict

from Qt import QtGui, QtCore, QtWidgets

import AppCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        AppCore.RegisterObject(self)
        
        #Get LayoutSettings
        self.defaultLayoutsPath = AppCore.GetOverriddenPath('MainWindow_defaultLayouts.ini')
        self.userLayoutsPath = AppCore['AppDataDirectory']+'/'+'MainWindow_userLayouts.ini'
        self.layoutSettings = QtCore.QSettings(self.defaultLayoutsPath, QtCore.QSettings.IniFormat)
        #if os.path.exists(self.userLayoutsPath):
        #    self.layoutSettings = QtCore.QSettings(self.userLayoutsPath, QtCore.QSettings.IniFormat)
        
    def initUI(self):
        ###CosmeticSettings###
        self.setPalette(AppCore.App.palette())
        self.WindowFont = AppCore.AppPrefs['AppFont']
        self.setWindowTitle(AppCore.AppSettings['AppTitle'])
        self.setWindowIcon(QtGui.QIcon(AppCore.AppSettings['AppIcon']))   
        self.AllowNestedDocks
        self.ForceTabbedDocks
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)
        self.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.setDockNestingEnabled(True)
        ######################
        
        ###Menu Bar###
        self.MenuBar = self.menuBar()
        self.DefineMenus()
        self.SetMenuShortcuts()
        self.SetMenuStatusTips()
        self.SetMenuConnections()
        ##############

        self.show()
        self.RestoreLayoutFunction(0)
    
    
    def CreateMenu(self, MenuName, ActionList):
        MenuObject = self.MenuBar.addMenu('&'+MenuName)
        for action in ActionList:
            if action == 'SEPARATOR':   
                MenuObject.addSeparator()
            else:
                self.NewAction = QtWidgets.QAction('New Project', self)
                MenuObject.addAction(self.NewAction)
        
        return MenuObject
    def DefineMenus(self):
        ####FileMenu####
        self.FileMenuActions = [
        'NewAction',
        'OpenAction',
        'ReloadAction',
        'SEPARATOR',
        'SaveAction',
        'SaveAsAction',
        'SEPARATOR',
        'CloseAction',
        'QuitAction',
        ]
        self.EditMenuActions = [
        'UndoAction',
        'RedoAction',
        'SEPARATOR',
        'CutAction',
        'CopyAction',
        'PasteAction',
        'SEPARATOR',
        'DeleteAction',
        'SelectAllAction',
        'SEPARATOR',
        'RestoreLayoutAction',
        'SaveLayoutAction',
        'SEPARATOR',
        'PrefsWindowAction',
        'PluginsWindowAction',
        ]
        
        self.NewAction = QtWidgets.QAction('New Project', self)
        self.OpenAction = QtWidgets.QAction('Open Project', self)
        self.ReloadAction = QtWidgets.QAction('Reload Project', self)
        self.SaveAction = QtWidgets.QAction('Save Project', self)
        self.SaveAsAction = QtWidgets.QAction('Save As', self)
        self.CloseAction = QtWidgets.QAction('Close Project', self)
        self.QuitAction = QtWidgets.QAction('Quit', self)

        self.FileMenu = self.MenuBar.addMenu('&File')
        self.FileMenu.addAction(self.NewAction)
        self.FileMenu.addAction(self.OpenAction)
        self.FileMenu.addAction(self.ReloadAction)
        self.FileMenu.addSeparator() 
        self.FileMenu.addAction(self.SaveAction)
        self.FileMenu.addAction(self.SaveAsAction)
        self.FileMenu.addSeparator() 
        self.FileMenu.addAction(self.CloseAction)
        self.FileMenu.addAction(self.QuitAction)
        #####################################
        
        ####EditMenu####
        self.UndoAction = QtWidgets.QAction('Undo', self)
        self.RedoAction = QtWidgets.QAction('Redo', self)
        self.CutAction = QtWidgets.QAction('Cut', self)
        self.CopyAction = QtWidgets.QAction('Copy', self)
        self.PasteAction = QtWidgets.QAction('Paste', self)
        self.DeleteAction = QtWidgets.QAction('Delete', self)
        self.SelectAllAction = QtWidgets.QAction('Select All', self)
        self.RestoreLayoutAction = QtWidgets.QAction('Restore Layout 0', self)
        self.SaveLayoutAction = QtWidgets.QAction('Save Layout 0', self)
        self.PrefsWindowAction = QtWidgets.QAction('Preferences', self)
        self.PluginsWindowAction = QtWidgets.QAction('Plugins', self)
        
        self.EditMenu = self.MenuBar.addMenu('&Edit')
        self.EditMenu.addAction(self.UndoAction)
        self.EditMenu.addAction(self.RedoAction)
        self.EditMenu.addSeparator()
        self.EditMenu.addAction(self.CutAction)
        self.EditMenu.addAction(self.CopyAction)
        self.EditMenu.addAction(self.PasteAction)
        self.EditMenu.addSeparator()
        self.EditMenu.addAction(self.DeleteAction)
        self.EditMenu.addAction(self.SelectAllAction)
        self.EditMenu.addSeparator()
        self.EditMenu.addAction(self.RestoreLayoutAction)
        self.EditMenu.addAction(self.SaveLayoutAction)
        self.EditMenu.addSeparator()
        self.EditMenu.addAction(self.PrefsWindowAction)
        self.EditMenu.addAction(self.PluginsWindowAction)
    def SetMenuShortcuts(self):
        #Takes:
        #Performs: Sets shortcuts on menu actions by reading them from the AppPrefs file
        #Returns:
        
        ####FileMenu####
        self.NewAction.setShortcut('Ctrl+N')
        self.OpenAction.setShortcut('Ctrl+O')
        self.ReloadAction.setShortcut('Ctrl+R')
        self.SaveAction.setShortcut('Ctrl+S')
        self.SaveAsAction.setShortcut('Ctrl+Alt+S')
        self.CloseAction.setShortcut('Ctrl+W')
        self.QuitAction.setShortcut('Ctrl+Q')
        ################
        
        ####EditMenu####
        self.UndoAction.setShortcut('Ctrl+Z')
        self.RedoAction.setShortcut('Ctrl+Y')
        self.CutAction.setShortcut('Ctrl+X')
        self.CopyAction.setShortcut('Ctrl+C')
        self.PasteAction.setShortcut('Ctrl+V')
        self.DeleteAction.setShortcut('Delete')
        self.SelectAllAction.setShortcut('Ctrl+Shift+A')
        self.RestoreLayoutAction.setShortcut('Shift+F1')
        self.SaveLayoutAction.setShortcut('Ctrl+F1')
        self.PrefsWindowAction.setShortcut('Ctrl+P')
        self.PluginsWindowAction.setShortcut('Ctrl+Shift+P')
    def SetMenuStatusTips(self):
        #Takes:
        #Performs: Sets status tips on menu actions by reading them from the AppPrefs file
        #Returns:
        
        ####FileMenu####
        self.NewAction.setStatusTip('New Project')
        self.OpenAction.setStatusTip('Open Project')
        self.ReloadAction.setStatusTip('Reload Project')
        self.SaveAction.setStatusTip('Save Project')
        self.SaveAsAction.setStatusTip('Save Project As')
        self.CloseAction.setStatusTip('Close Project')
        self.QuitAction.setStatusTip('Quit Application')
        ################
        
        ####EditMenu####
        self.UndoAction.setStatusTip('Undo Action')
        self.RedoAction.setStatusTip('Redo Action')
        self.CutAction.setStatusTip('Cut Action')
        self.CopyAction.setStatusTip('Copy Action')
        self.PasteAction.setStatusTip('Paste Action')
        self.DeleteAction.setStatusTip('Delete Action')
        self.SelectAllAction.setStatusTip('Select All Action')
        self.RestoreLayoutAction.setStatusTip('Restore Saved Layout')
        self.SaveLayoutAction.setStatusTip('Save Layout')
        self.PrefsWindowAction.setStatusTip('Edit Preferences')
        self.PluginsWindowAction.setStatusTip('Edit Plugins')
    def SetMenuConnections(self):
        #Takes:
        #Performs: Sets connections on menu actions by reading them from the AppPrefs file
        #Returns:
        
        ####FileMenu####
        self.NewAction.triggered.connect(self.NewFunction)
        self.OpenAction.triggered.connect(self.OpenFunction)
        self.ReloadAction.triggered.connect(self.ReloadFunction)
        self.SaveAction.triggered.connect(self.SaveFunction)
        self.SaveAsAction.triggered.connect(self.SaveAsFunction)
        self.CloseAction.triggered.connect(self.CloseFunction)
        self.QuitAction.triggered.connect(self.QuitFunction)
        ################
        
        ####EditMenu####
        self.UndoAction.triggered.connect(self.UndoFunction)
        self.RedoAction.triggered.connect(self.RedoFunction)
        self.CutAction.triggered.connect(self.CutFunction)
        self.CopyAction.triggered.connect(self.CopyFunction)
        self.PasteAction.triggered.connect(self.PasteFunction)
        self.DeleteAction.triggered.connect(self.DeleteFunction)
        self.SelectAllAction.triggered.connect(self.SelectAllFunction)
        self.RestoreLayoutAction.triggered.connect(self.RestoreLayoutFunction)
        self.SaveLayoutAction.triggered.connect(self.SaveLayoutFunction)
        self.PrefsWindowAction.triggered.connect(self.PrefsWindowFunction)
        self.PluginsWindowAction.triggered.connect(self.PluginsWindowFunction)
    
    ###EditMenu Functions###
    def UndoFunction(self):    
        pass
    def RedoFunction(self):    
        pass
    def CutFunction(self):    
        pass
    def CopyFunction(self):    
        pass
    def PasteFunction(self):    
        pass
    def DeleteFunction(self):    
        pass
    def SelectAllFunction(self):    
        pass
    def RestoreLayoutFunction(self, *args):
        if len(args) == 1:
            versionNum = int(args[0])
        else:
            versionNum = int(self.sender().text()[-1])
        print('Restoring Layout', versionNum)
        self.restoreGeometry(self.layoutSettings.value("geometry"+str(versionNum)))
        self.restoreState(self.layoutSettings.value("windowState"+str(versionNum)))
    def SaveLayoutFunction(self, *args):
        if len(args) == 1:
            versionNum = int(args[0])
        else:
            versionNum = int(self.sender().text()[-1])
        print('Saving Layout', versionNum)
        self.layoutSettings.setValue("geometry"+str(versionNum), self.saveGeometry())
        self.layoutSettings.setValue("windowState"+str(versionNum), self.saveState())
    def PrefsWindowFunction(self):
        AppCore.PrefsWindow.show()
    def PluginsWindowFunction(self):
        AppCore.PluginsWindow.show()    
    ########################
     
    ###FileMenu Functions###
    def NewFunction(self):
        pass
    def OpenFunction(self):
        pass
    def ReloadFunction(self):
        pass
    def SaveFunction(self):
        pass
    def SaveAsFunction(self):
        pass
    def CloseFunction(self):
        pass
    def QuitFunction(self):
        self.close()
    ########################
        
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
