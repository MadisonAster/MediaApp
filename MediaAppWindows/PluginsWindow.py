#===============================================================================
# @Author: Madison Aster
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with Qt Library
#    Copyright (C) 2013 Madison Aster
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

from Qt import QtGui, QtCore, QtWidgets

import AppCore
from MediaAppKnobs import *

class PluginsWindow(QtWidgets.QWidget):
    def __init__(self):
        super(PluginsWindow, self).__init__()
        AppCore.RegisterObject(self)
        
        self.panelLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.panelLayout)
        
        self.ScrollWidget = QtWidgets.QScrollArea()
        self.EnumeratedPlugins = EnumeratedPlugins()
        self.ScrollWidget.setWidget(self.EnumeratedPlugins)
        self.panelLayout.addWidget(self.ScrollWidget)
        
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        
        saveButton = QtWidgets.QPushButton('SavePlugins')
        saveButton.clicked.connect(self.SavePlugins)
        defaultsButton = QtWidgets.QPushButton('RestoreDefaults')
        defaultsButton.clicked.connect(self.RestoreDefaults)
        closeButton = QtWidgets.QPushButton('Close')
        closeButton.clicked.connect(self.close)
        
        self.buttonsLayout.addWidget(saveButton)
        self.buttonsLayout.addWidget(defaultsButton)
        self.buttonsLayout.addWidget(closeButton)
        
        self.panelLayout.addLayout(self.buttonsLayout)
    def SavePlugins(self):
        pass
    def RestoreDefaults(self):
        pass
class EnumeratedPlugins(QtWidgets.QWidget):
    def __init__(self):
        super(EnumeratedPlugins, self).__init__()
        self.panelLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.panelLayout)
        
        self.knobs = []

    def __delitem__(self, key):
        for i, knob in enumerate(self.knobs):
            if knob.name.text() == key:
                del self.knobs[i]
    def __setitem__(self, key, value):
        if 'knob' in type(value).__name__.lower():
            if self[key] != None:
                del self[key]       #BUG widgets don't get destroyed when we do a simple delete
            #Node subclass has assigned knob the name key, so we tell the knob that here.   
            value.name.setText(key)
            self.knobs.append(value)
        else:
            self[key].setValue(value)
        #self.show()
    def __getitem__(self, key):
        for knob in self.knobs:
            if knob.name.text() == key:
                return knob
        else:
            return None
            
    def sizeHint(self):
        YHint = 0
        for knob in self.knobs:
            YHint += knob.sizeHint().height()+20
        return QtCore.QSize(800,YHint)
        
    #def sizeHint(self):
    #    return QtCore.QSize(400,1000)    
        
PluginsWindow()
        
        
        
        
        
        
        
        
        
        
        