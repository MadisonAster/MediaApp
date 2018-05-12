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

from Qt import QtGui, QtCore, QtWidgets

from .KnobConstructor import Knob
from . import KnobElements

class ComboKnob(Knob):
    def __init__(self, values, name = 'ComboKnob'):
        super(ComboKnob, self).__init__()
        self.name.setText(name)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        
        self.ComboWidget = KnobElements.ComboWidget()
        self.knobLayout.addWidget(self.ComboWidget)
        
        self.ComboWidget.currentIndexChanged.connect(self.ValueChanged)

        if type(values) is list:
            self.ComboWidget.setItems(values)
            
    def setValue(self, value):
        self.ComboWidget.setValue(value)
    def getValue(self):
        return self.ComboWidget.getValue()
    def setItems(self, Items):
        self.ComboWidget.setItems(Items)
    def currentIndex(self):
        return self.ComboWidget.currentIndex()