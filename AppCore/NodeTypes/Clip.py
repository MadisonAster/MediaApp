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
import os

from PySide import QtGui, QtCore
import imageio

import AppCore
from NodeConstructor import *
from KnobTypes import *

class Clip(ImageNode, AudioNode):
    def __init__(self):
        super(Clip, self).__init__()
        self['ClassName'] = 'Clip'
        self.setName(AppCore.getIncrementedName('Clip'))
        ################################
        
        #FLAW: move parent kw setting to KnobConstructor
        defaultPath = '*NWSTORAGE/Environment/AppVariables/PyPlayback/PyPlayback/ImageIO/testImages/chelsea.png'
        defaultPath = '*NWSTORAGE/Environment/AppVariables/PyPlayback/PyPlayback/ImageIO/testImages/MV_BTS_VFX_01001510/MV_BTS_VFX_01001510.######.tif'
        #defaultPath = '*NWSTORAGE/'
        self['file'] = FileKnob(defaultPath, parent = self)
        self['firstFrame'] = IntKnob(86770)
        self['lastFrame'] = IntKnob(86785)
        self['startAt'] = IntKnob(0)
        
        self['before'] = ComboKnob(['hold', 'loop', 'bounce', 'black'])
        self['after'] = ComboKnob(['hold', 'loop', 'bounce', 'black'])
        
        self.attachKnobs()
        
    
    def nodeShape(self):
        self.polyShape = [[0,0],[100,0],[100,24],[0,24]]
        self.color1 = QtGui.QColor(238,238,238)
        self.color2 = QtGui.QColor(122,122,122)
        
    def generateImage(self):
        imagePath = self['file'].getEvaluatedPath()
        if os.path.isfile(imagePath):
            image = imageio.imread(imagePath)
            image = imageio.core.util.image_as_uint8(image)
            #self.imageString = image.tobytes()
            self.imageString = image.tostring()
            
            #TEST: I don't think this will add any overhead, take it out if it does
            image = image.swapaxes(0, 1)
            width, height, channels = image.shape
            #height, width, channels = image.shape
            
            bytesPerLine = channels * width
            if channels == 4:
                QImage = QtGui.QImage(self.imageString, width, height, bytesPerLine, QtGui.QImage.Format_ARGB32).rgbSwapped()
            elif channels == 3:
                QImage = QtGui.QImage(self.imageString, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            
            return QImage
        else:
            #Generate Black QImage
            width = AppCore.AppAttributes['ResolutionWidth']
            height = AppCore.AppAttributes['ResolutionHeight']
            image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)
            return image
        