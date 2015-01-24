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

class ComboWidget(QtGui.QComboBox):
    def __init__(self):
        super(ComboWidget, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        #self.setAlignment(QtCore.Qt.AlignLeft)
    def sizeHint(self):
        return QtCore.QSize(150,16)
    def setValue(self, value):
        if type(value) is str:
            value = self.findText(value)
        self.setCurrentIndex(value)
    def getValue(self):
        return self.currentText()
    def setItems(self, Items):
        for index in range(self.count()):
            self.removeItem(index)
        self.addItems(Items)
        self.update()
