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

from NodeConstructor import *

from KnobTypes import *

class Clip(Node):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(Clip, self).__init__(CorePointer)
        
        self['ClassName'] = 'Clip'
        self.setName(Core.getIncrementedName('Clip'))
        
        #FLAW: move parent kw setting to KnobConstructor
        self['file'] = FileKnob('*NWSTORAGE/', CorePointer, parent = self)
        self['firstFrame'] = IntKnob(0)
        self['lastFrame'] = IntKnob(0)
        self['startAt'] = IntKnob(0)
        
        #TODO: add PulldownKnob
        #self['before'] = PulldownKnob()
        #self['after'] = PulldownKnob()
        
        self.attachKnobs()
        ################################
    
    def nodeShape(self):
        self.polyShape = [[0,0],[100,0],[100,24],[0,24]]
        self.color1 = QtGui.QColor(238,238,238)
        self.color2 = QtGui.QColor(122,122,122)
        
    def generateImage(self):
        
        #image = imageio.imread('C:/Environment/AppVariables/PyPlayback/PyPlayback/ImageIO/testImages/chelsea.png') 
        #image = imageio.imread('C:/Environment/AppVariables/PyPlayback/PyPlayback/ImageIO/testImages/MV_BTS_VFX_01001510/MV_BTS_VFX_01001510.086770.tif')

        image = imageio.imread(self['file'].getEvaluatedPath())
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
        
    #def node(self):
    #    return self.NodeType
    #def setNodeType(self, shape):
    #    self.nodeType = shape
    #def setRandomNodeType(self):
    #    self.setNodeType(random.randint(1, 7))
        
        