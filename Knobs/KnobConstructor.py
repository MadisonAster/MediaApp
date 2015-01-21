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

import KnobElements

class Knob(QtGui.QWidget):
    def __init__(self):
        self.name = KnobElements.KnobLabel()
        super(Knob, self).__init__()
        
        #self.setToolTip('Here lies a tooltip, barren and empty')
        #self.setHidden(False)
        #self.setEnabled(True)
        self.newline = True
        self.shown = True
        
        self.knobLayout = QtGui.QHBoxLayout()
        self.knobLayout.setContentsMargins(0,0,0,0)
        self.knobLayout.addWidget(self.name)
        
        self.setLayout(self.knobLayout)
        
        def none(): pass
        self.changed = none
        
    def update(self):
        if hasattr(self, 'parent'):
            if not callable(self.parent):
                self.parent.update()
    def setChanged(self, callable):
        self.changed = callable
        
        #BUG: add some isinstance calls here
        self.textChanged.connect(self.changed)
    def showName(self, value):
        if value is True:
            self.name.show()
        else:
            self.name.hide()
        
    