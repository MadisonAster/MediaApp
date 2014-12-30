#===============================================================================
# @Author: Thomas McVay
# @Version: 0.1
# @LastModified: 130511
# @Description: 
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
#    See MediaApp_LGPL.txt in the root directory of this library for copy of
#    GNU Lesser General Public License and other license details.
#===============================================================================

from PySide import QtGui, QtCore

class KnobLabel(QtGui.QLabel):
    def __init__(self):
        super(KnobLabel, self).__init__()
        
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Ignored)
        self.setAlignment(QtCore.Qt.AlignRight)
    def sizeHint(self):
        return QtCore.QSize(100,15)
        
        
class Knob(object):
    def __init__(self):
        self.name = KnobLabel()
        
        self.setToolTip('Here lies a tooltip, barren and empty')
        self.setHidden(False)
        self.setEnabled(True)
        self.newline = True
        
        self.knobLayout = QtGui.QHBoxLayout()
        self.knobLayout.addWidget(self.name)
    
    
    