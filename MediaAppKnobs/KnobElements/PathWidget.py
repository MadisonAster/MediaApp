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

import AppCore
from .StrWidget import StrWidget

class PathWidget(StrWidget):
    urlDropped = QtCore.Signal()
    def __init__(self):
        super(PathWidget, self).__init__()
        self.setAcceptDrops(True)
                
    def setValue(self, value):
        self.setText(self.TranslatePath(value))
    def getValue(self):
        return self.unTranslatePath(self.text())
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore() 
    def dropEvent(self, event):
        eventText = event.mimeData().urls()[0].path().lstrip('/')
        self.setText(self.TranslatePath(eventText))
        self.urlDropped.emit()  
        self.update()

    def unTranslatePath(self, path):
        path = path.replace('\\','/')
        for key in AppCore.AppPrefs['GLOBALS']:
            if(AppCore.AppPrefs[key]):
                repVal = AppCore.AppPrefs[key].replace('\\','/').rstrip('/')
                path = path.replace(key, repVal)
        return path
        
    def TranslatePath(self, path):
        path = path.replace('\\','/')
        for key in AppCore.AppPrefs['GLOBALS']:
            if(AppCore.AppPrefs[key]):
                repVal = AppCore.AppPrefs[key].replace('\\','/').rstrip('/')
                path = path.replace(repVal, key)
        return path

    
    ###These wont work, refer to your stack overflow question!###
    #@QtCore.Slot()
    #def copy(self):
    #    print 'hello carl'
    #    unTranslatedText = self.unTranslatePath(self.getValue())
    #    AppCore.App.clipboard().setText('hello carl')
    #    
    #def paste(self):
    #    self.setValue(self.TranslatePath(AppCore.App.clipboard().text()))
    #    self.update()
