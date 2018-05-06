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

from PyQt import QtGui, QtCore, QtWidgets

from .KnobConstructor import Knob
from . import KnobElements

class TitleKnob(Knob):
    def __init__(self, value, name = 'TitleKnob'):
        super(TitleKnob, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.topDivider = KnobElements.Divider(horizontal = True)
        self.barDivider = KnobElements.Divider(horizontal = True)
        self.bottomDivider = KnobElements.Divider(horizontal = True)
        self.leftDivider = KnobElements.Divider(vertical = True)
        self.rightDivider = KnobElements.Divider(vertical = True)
        
        self.spacerLayout = QtWidgets.QHBoxLayout()
        self.spacerLayout.addWidget(self.leftDivider)
        self.spacerLayout.addWidget(KnobElements.Spacer())
        self.spacerLayout.addWidget(self.rightDivider)
        
        self.vertLayout.insertWidget(0, self.topDivider)
        #self.vertLayout.addLayout(self.knobLayout)
        self.vertLayout.addWidget(self.barDivider)
        #self.vertLayout.addLayout(self.spacerLayout)
        #self.vertLayout.addWidget(self.bottomDivider)
        
        
        self.knobLayout.setContentsMargins(40,0,3,0)
        self.knobLayout.setSpacing(50)
        
        self.StrWidget = KnobElements.StrWidget()
        #self.StrWidget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.knobLayout.addWidget(self.StrWidget)
        
        #self.knobLayout.addWidget(KnobElements.Spacer())
        
        self.closeButton = KnobElements.SquareButton('x')
        self.knobLayout.addWidget(self.closeButton)
        self.closeButton.clicked.connect(self.closeWidget)
        
        self.name.setText(name)
        self.name.hide()
        self.setValue(value)

    def setValue(self, value):
        self.StrWidget.setValue(value)
    def getValue(self):
        return self.StrWidget.getValue()
    def setChanged(self, callable):
        self.changed = callable
        self.StrWidget.textChanged.connect(self.changed)
    def closeWidget(self):
        self.parent.close()
       