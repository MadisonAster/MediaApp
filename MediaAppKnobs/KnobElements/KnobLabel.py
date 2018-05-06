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
from copy import copy

from PyQt import QtGui, QtCore, QtWidgets

import AppCore

class KnobLabel(QtWidgets.QLabel):
    def __init__(self):
        super(KnobLabel, self).__init__()
        
        font = copy(AppCore.AppPrefs['AppFont'])
        try:
            font.__init__()
        except:
            pass
        #font.setStyle(QtGui.QFont.StyleOblique)
        font.setPointSize(font.pointSize()-3)
        self.setFont(font)
        
        #self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        #self.setAlignment(QtCore.Qt.AlignRight)
        #self.labelSize = 100
    #def sizeHint(self):
    #    return QtCore.QSize(self.labelSize,18)
       
       
       
       
       
       
       
       
       