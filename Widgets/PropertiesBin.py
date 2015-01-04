#===============================================================================
# @Author: Thomas McVay
# @ModuleDescription: 
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
#    See LICENSE in the root directory of this library for copy of
#    GNU Lesser General Public License and other license details.
#===============================================================================

from PySide import QtGui, QtCore

class PropertiesBin(QtGui.QScrollArea):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(PropertiesBin, self).__init__()
        #self.setBackgroundRole(QtGui.QPalette.Dark)
        self.setWidgetResizable(True)
        
        self.DockingBin = DockingBin(CorePointer)
        #self.DockingBin = TestWidget()
        self.DockingBin.show()
        self.setWidget(self.DockingBin)
        
        self.show()
        
    def getDockedWidgets(self):
        returnList = []
        for child in self.DockingBin.findChildren(QtGui.QDockWidget):
            if child.docked is True:
                returnList.append(child)
        return returnList
        
    def dockThisWidget(self, widget):
        #WORKAROUND 1: There doesn't appear to be a way to tell QT what location
        #within a DockWidgetArea that you want the DockWidget to be added.
        #So each time we add a widget we are removing them all, and adding again in the right order
    
        #WORKAROUND 2: appears to be no way to remove a child from a qobject.
        #recomended way seems to be widget.setParent(None), but widget still appears in list of children after making that call
        #using custom attribute widget.docked to solve this issue
    
        #move called widget to the top of parent.children() list so it will go to top if already docked
        widget.raise_()
        
        #Get list of current widgets, and reverse them because we need to re-add top to bottom
        dockedWidgets = self.getDockedWidgets()
        dockedWidgets.reverse()
        
        #Remove each currently docked widget
        for dockedWidget in dockedWidgets:
            self.DockingBin.removeDockWidget(dockedWidget)
        
        #Dock called widget if it is not already
        if widget.docked is False:
            self.DockingBin.addDockWidget(QtCore.Qt.TopDockWidgetArea, widget, QtCore.Qt.Vertical)
            widget.docked = True
            widget.show()
        
        #Re-add each docked widget
        for dockedWidget in dockedWidgets:
            self.DockingBin.addDockWidget(QtCore.Qt.TopDockWidgetArea, dockedWidget, QtCore.Qt.Vertical)
            dockedWidget.show()
        
        #Call show docking bin so that sizehint will be recalculated
        self.DockingBin.show()
        
        #Call ScrollArea.show() so that it will grab the size hint and display the widget
        self.show()
        
    def unDockThisWidget(self, widget):
        #WORKAROUND 1: widget.docked is a custom attribute, see dockThisWidget() for more details
        
        #self.DockingBin.removeChild(widget)
        self.DockingBin.removeDockWidget(widget)
        widget.docked = False 
        
class DockingBin(QtGui.QMainWindow):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(DockingBin, self).__init__()
        ################################
        self.setDockOptions(False)
        self.setAnimated(True)
        
        self.setFocusPolicy(Core.AppSettings['FocusPolicy'])
        
        #ToolBar#
        #toolbar = self.addToolBar('Exit')
        #toolbar.addAction(exitAction)
        #/ToolBar#
    def sizeHint(self):
        XHint, YHint = 200, 200
        for child in self.findChildren(QtGui.QDockWidget):
            if child.isVisible() is True:
                YHint += child.sizeHint().height()
                if child.sizeHint().width() > XHint:
                    XHint = child.sizeHint().width()
        return QtCore.QSize(XHint,YHint)  
    
        