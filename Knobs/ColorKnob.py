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
import KnobConstructor
from FloatKnob import FloatKnob

class ColorKnob(QtGui.QWidget):
    def __init__(self, red = 0.0, green = 0.0, blue = 0.0, name = 'FloatKnob'):
        super(ColorKnob, self).__init__()
        self.name = KnobConstructor.KnobLabel()
        self.knobLayout = QtGui.QHBoxLayout()
        
        #BUG: Program crashes if knob contains another knobtype.
        #self.knobLayout.addWidget(self)
        redKnob = QtGui.QLineEdit()
        #redKnob = FloatKnob(red)
        #greenKnob = FloatKnob(green)
        #blueKnob = FloatKnob(blue)
        
        self.knobLayout.addWidget(redKnob)
        #self.knobLayout.addWidget(greenKnob)
        #self.knobLayout.addWidget(blueKnob)
        
        self.name.setText(name)
    def setValue(self, value):
        self.setText(str(value))
    def getValue(self):
        return float(self.text())
    def sizeHint(self):
        return QtCore.QSize(100,24)