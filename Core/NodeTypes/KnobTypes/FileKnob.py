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
import KnobConstructor

class FileKnob(KnobConstructor.Knob, QtGui.QLineEdit):
    urlDropped = QtCore.Signal()
    def __init__(self, value, CorePointer, parent = None, name = 'StrKnob'):
        global Core
        Core = CorePointer
        #super(FileKnob, self).__init__(CorePointer)
        super(FileKnob, self).__init__()
        #######################################
        
        self.parent = parent
        
        self.knobLayout.addWidget(self)
        self.name.setText(name)
        self.setValue(value)
        
        self.setAcceptDrops(True)
         
        self.browseButton = QtGui.QPushButton('Browse', self)
        self.browseButton.clicked[bool].connect(self.fileBrowse)
        self.knobLayout.addWidget(self.browseButton)
        
    def setValue(self, value):
        self.setText(value)
    def getValue(self):
        return self.text()
    
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore() 
    def dropEvent(self, e):
        self.setText(e.mimeData().urls()[0].path().lstrip('/'))
        self.urlDropped.emit()        
    
    def unTranslatePath(self, path):
        path = path.replace('\\','/')
        for key in Core.AppPrefs['GLOBALS']:
            repVal = Core.AppPrefs[key].replace('\\','/').rstrip('/')
            path = path.replace(key, repVal)
        return path
        
    def TranslatePath(self, path):
        path = path.replace('\\','/')
        for key in Core.AppPrefs['GLOBALS']:
            repVal = Core.AppPrefs[key].replace('\\','/').rstrip('/')
            path = path.replace(repVal, key)
        return path
        
    def fileBrowse(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, "Open File", self.unTranslatePath(self.text()))
        if path:
            path = self.TranslatePath(path)
            self.setText(path)
        
    def getEvaluatedPath(self):
        currentFrame = Core.getCurrentFrame()
        startAt = self.parent['startAt'].getValue()
        offset = currentFrame-startAt
        
        firstFrame = self.parent['firstFrame'].getValue()
        lastFrame = self.parent['lastFrame'].getValue()
        length = lastFrame-firstFrame
        
        
        ####Get Frame Value####
        #TEST: loop and bounce
        if offset < 0 or offset > length:
            if offset < 0:
                knob = 'before'
            else:
                knob = 'after'
            knobVal = self.parent[knob].getValue()
            
            if knobVal == 'hold':
                if knob == 'before':
                    frame = self.parent['firstFrame'].getValue()
                elif knob == 'after':
                    frame = self.parent['lastFrame'].getValue()
            elif knobVal == 'loop':
                frame = firstFrame+(offset % (length+1))
            elif knobVal == 'bounce':
                if int(offset/(length+1)) % 2 == 1:
                    frame = firstFrame-((offset+1) % (-length-1))
                elif int(offset/(length+1)) % 2 == 0:
                    frame = firstFrame+(offset % (length+1))        
            elif knobVal == 'black':
                return self.unTranslatePath('*BLACK')
        else:
            frame = firstFrame+offset
        ####################

        
        #TODO fix this
        text = self.text().replace('######', str(frame).zfill(6))
        text = self.unTranslatePath(text)
        
        return text
        
        
        
        
       