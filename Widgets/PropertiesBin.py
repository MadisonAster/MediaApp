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
import AppCore


            
class DockingBin(QtGui.QMainWindow):
    def __init__(self):
        super(DockingBin, self).__init__()
        self.setDockOptions(False)
        self.setAnimated(True)
        self.setFocusPolicy(AppCore.AppSettings['FocusPolicy'])
        
    def sizeHint(self):
        #WORKAROUND: adding together the height of all the docked widgets manually here
        #QtGui.QScrollArea does not appear to care what size policy you set, it always treats
        #the sizeHint you return here as QtGui.QSizePolicy.Fixed
        XHint, YHint = 200, 200
        for child in self.findChildren(QtGui.QDockWidget):
            if child.isVisible() is True:
                YHint += child.sizeHint().height()
                if child.sizeHint().width() > XHint:
                    XHint = child.sizeHint().width()
        return QtCore.QSize(XHint,YHint)  
    
    def unDockThisWidget(self, widget):
        #WORKAROUND: widget.docked is a custom attribute, see dockThisWidget() for more details
        
        #self.removeChild(widget)
        self.removeDockWidget(widget)
        widget.docked = False
        
    def emptyBin(self):
        for widget in self.getDockedWidgets():
            self.unDockThisWidget(widget)
            
    def dockThisWidget(self, widget):
        #WORKAROUND: There doesn't appear to be a way to tell QT what location
        #within a DockWidgetArea that you want the DockWidget to be added.
        #So each time we add a widget we are removing them all, and adding again in the right order
    
        #WORKAROUND: appears to be no way to remove a child from a qobject.
        #recomended way seems to be widget.setParent(None), but widget still appears in list of children after making that call
        #using custom attribute widget.docked to solve this issue
    
        #move called widget to the top of parent.children() list so it will go to top if already docked
        widget.raise_()
        
        #Get list of current widgets, and reverse them because we need to re-add top to bottom
        dockedWidgets = self.getDockedWidgets()
        dockedWidgets.reverse()
        
        #Remove each currently docked widget
        for dockedWidget in dockedWidgets:
            self.removeDockWidget(dockedWidget)
        
        #Dock called widget if it is not already
        if widget.docked is False:
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, widget, QtCore.Qt.Vertical)
            widget.docked = True
            widget.show()
        
        #Re-add each docked widget
        for dockedWidget in dockedWidgets:
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dockedWidget, QtCore.Qt.Vertical)
            dockedWidget.show()
            
    def getDockedWidgets(self):
        returnList = []
        for child in self.findChildren(QtGui.QDockWidget):
            if child.docked is True:
                returnList.append(child)
        return returnList
        
class PropertiesBin(QtGui.QMainWindow):
    def __init__(self):
        super(PropertiesBin, self).__init__()
        self.className = self.__class__.__name__
        self.setDockOptions(False)
        
        self.DockingBin = DockingBin()
        self.DockingBin.show()
        
        self.ScrollBin = QtGui.QScrollArea()
        self.ScrollBin.setWidgetResizable(True)
        self.ScrollBin.setWidget(self.DockingBin)    
        self.ScrollBin.show()
        
        self.setCentralWidget(self.ScrollBin)
        
        #ToolBar#
        toolbar = self.addToolBar('test')
        toolbar.setMovable(False)
        
        EmptyBin = QtGui.QAction('EmptyBin', self)
        EmptyBin.setStatusTip('Close All the widgets in the bin.')
        EmptyBin.triggered.connect(self.emptyBin)
        
        toolbar.addAction(EmptyBin)
        
    #WORKAROUND: Pointer functions below, because we can't use multiple inheritance and setWidget(self)
    def getDockedWidgets(self):
        return self.DockingBin.getDockedWidgets()
    def dockThisWidget(self, widget):
        self.DockingBin.dockThisWidget(widget)
    def unDockThisWidget(self, widget):
        self.DockingBin.unDockThisWidget(widget)
    def emptyBin(self):
        self.DockingBin.emptyBin()