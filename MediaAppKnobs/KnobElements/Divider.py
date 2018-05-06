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

class Divider(QtWidgets.QWidget):
    def __init__(self, vertical = False, horizontal = False):
        super(Divider, self).__init__()
        
        if vertical == True:
            self.width = 1
            verticalPolicy = QtWidgets.QSizePolicy.Expanding
        else:
            self.width = 0
            verticalPolicy = QtWidgets.QSizePolicy.Fixed
        if horizontal == True:
            self.height = 1
            horizontalPolicy = QtWidgets.QSizePolicy.Expanding
        else:
            self.height = 0
            horizontalPolicy = QtWidgets.QSizePolicy.Fixed
        self.setSizePolicy(horizontalPolicy, verticalPolicy)
            
            
        self.color = QtGui.QColor(0,0,0,1)
        #self.setPalette(QtGui.QPalette(self.color))
        #self.setAutoFillBackground(True)
    def sizeHint(self):
        return QtCore.QSize(self.width,self.height)
    def setWidth(self, value):
        self.width = value
    def setHeight(self, value):    
        self.height = value
    def setColor(self, QColor):
        self.color = QColor
        self.setPalette(QtGui.QPalette(self.color, QtGui.QBrush(self.color)))
    def paintEvent(self, pEvent):
        painter = QtGui.QPainter(self)
        
        #DrawBG
        self.widgetSize = self.size()
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(0, 0, self.widgetSize.width(), self.widgetSize.height())   
    
