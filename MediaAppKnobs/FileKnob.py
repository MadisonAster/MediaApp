#===============================================================================
# @Author: Madison Aster
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with Qt Library
#    Copyright (C) 2013 Madison Aster
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

import re

from Qt import QtGui, QtCore, QtWidgets

import AppCore
from .KnobConstructor import Knob
from . import KnobElements


class FileKnob(Knob):
    urlDropped = QtCore.Signal()
    def __init__(self, value, parent = None, name = 'FileKnob'):
        super(FileKnob, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
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
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open File", self.PathWidget.getValue())
        if path:
            self.PathWidget.setValue(path)
        
    #FLAW: Maybe this does not belong here
    def getEvaluatedPath(self, *args):
        if len(args) is 1:
            currentFrame = args[0]
        else:
            currentFrame = self.parent.getCurrentFrameNumber()
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
        
        text = self.patternFill(self.getValue(), frame)
        return text
        
    def patternFill(self, pattern, frame):
        splitList = re.split("(#*)", pattern[::-1], maxsplit=1)[::-1]
        for a in range(len(splitList)):
            splitList[a] = splitList[a][::-1]
        if len(splitList) != 1:
            forePattern = splitList[0]
            frameDigits = len(splitList[1])
            aftPattern = splitList[2]
        else:
            forePattern = pattern.rsplit('%',1)[0]
            frameDigits = int(pattern.rsplit('%',1)[-1].split('d',1)[0])
            aftPattern = pattern.rsplit('%',1)[-1].split('d',1)[-1]
        
        frame = str(frame).zfill(frameDigits)
        return forePattern+frame+aftPattern
        
        
        
        
       