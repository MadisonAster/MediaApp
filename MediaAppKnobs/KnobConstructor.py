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

from . import KnobElements

class Knob(QtWidgets.QWidget):
    ValueChanged = QtCore.Signal(str)
    def __init__(self):
        self.name = KnobElements.KnobLabel()
        super(Knob, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        
        #self.setToolTip('Here lies a tooltip, barren and empty')
        #self.setHidden(False)
        #self.setEnabled(True)
        self.newline = True
        self.shown = True
        
        self.vertLayout = QtWidgets.QVBoxLayout()
        self.vertLayout.setContentsMargins(0,0,0,0)
        self.vertLayout.setSpacing(0)
        
        self.knobLayout = QtWidgets.QHBoxLayout()
        self.knobLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.knobLayout.setContentsMargins(0,0,0,0)
        self.knobLayout.setSpacing(0)
        self.knobLayout.addWidget(self.name)
        self.vertLayout.addLayout(self.knobLayout)
        self.setLayout(self.vertLayout)
        
    def update(self):
        if hasattr(self, 'parent'):
            if not callable(self.parent):
                self.parent.update()
    
    def showName(self, value):
        if value is True:
            self.name.show()
        else:
            self.name.hide()
    