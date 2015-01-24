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

import AppCore
from KnobConstructor import Knob
import KnobElements


class FileKnob(Knob):
    urlDropped = QtCore.Signal()
    def __init__(self, value, parent = None, name = 'FileKnob'):
        super(FileKnob, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        
        self.name.setText(name)
        self.parent = parent
        #self.setAcceptDrops(True)
        
        self.PathWidget = KnobElements.PathWidget()
        self.knobLayout.addWidget(self.PathWidget)

        self.browseButton = KnobElements.SquareButton('B')
        self.browseButton.setAutoFillBackground(True)
        self.browseButton.clicked.connect(self.fileBrowse)
        self.knobLayout.addWidget(self.browseButton)
        
        self.setValue(value)
        
    def setValue(self, value):
        self.PathWidget.setValue(value)
    def getValue(self):
        return self.PathWidget.getValue()

    def fileBrowse(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, "Open File", self.PathWidget.getValue())
        if path:
            self.PathWidget.setValue(path)
        
    #FLAW: Maybe this does not belong here
    def getEvaluatedPath(self, *args):
        if len(args) is 1:
            currentFrame = args[0]
        else:
            currentFrame = self.parent.getCurrentFrame()
        startAt = self.parent['startAt'].getValue()
        offset = currentFrame-startAt
        
        firstFrame = self.parent['firstFrame'].getValue()
        lastFrame = self.parent['lastFrame'].getValue()
        length = lastFrame-firstFrame
        
        ####Get Frame Value####
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
                return self.PathWidget.unTranslatePath('*BLACK')
        else:
            frame = firstFrame+offset
        ####################
        
        #TODO fix this
        text = self.getValue().replace('######', str(frame).zfill(6))
        
        return text
        
        
        
        
       