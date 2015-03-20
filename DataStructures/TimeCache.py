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
import sys
from collections import deque

import AppCore

class TimeIndicator(object):
    def __init__(self):
        super(TimeIndicator, self).__init__()
        
        self.Position = 0
        self.Top = 0
    def getCurrentFrameNumber(self):
        return self.Position
    def getTopPosition(self):
        return self.Top
    def setCurrentFrameNumber(self, value):
        self.Position = value
    def setTopPosition(self, value):
        self.Top = value
        
    def moveCurrentFrameNumber(self, value):
        self.Position += value
    
    
class TimeCache(deque):
    def __init__(self):
        super(TimeCache, self).__init__()
        
        self.append(None)
        self.zeroFrame = 0
        self.rotateCounter = 0
        
        self.TimeIndicator = TimeIndicator()
        
        #FLAW: need to keep track of frameCache size in AppCore somehow
        #AppCore.data['frameCache'] = 
        #AppCore.data['frameCache'].append(AppCore.generateBlack())

    #Overridden Functions###
    def __contains__(self, frame):
        if frame >= self.zeroFrame and frame < self.zeroFrame+len(self):
            return True
        else:
            return False
    def pop(self, *args):
        returnList = []
        if len(args) is 1:
            frames = args[0]
        else:
            frames = 1
        for i in range(frames):
            returnList.append(super(TimeCache, self).pop())
            if self.rotateCounter < 0:
                self.rotateCounter += 1
        return returnList
    def rotate(self, value):
        super(TimeCache, self).rotate(value)
        self.rotateCounter += value
    def reset(self):
        self.rotate(-self.rotateCounter)
    #######################
    
    def gotoFrameNumber(self, frameNumber, end = False):
        rotationAmount = frameNumber - self.zeroFrame + self.rotateCounter
        self.rotate(-rotationAmount-end)  
    def moveCurrentFrameNumber(self, value, playback = False):
        self.TimeIndicator.moveCurrentFrameNumber(value)
        if playback is False:
            self.rotate(-value)
    def getCurrentImage(self):
        if self.getCurrentFrameNumber() in self:
            return self[0]
        else:
            return None
    def getCacheList(self):
        return list(range(self.zeroFrame, len(self)))
    
    def getImageAt(self, frame):
        if frame in self:
            currentFrame = self.getCurrentFrameNumber()
            self.gotoFrameNumber(frame)
            returnVal = self[0]
            self.gotoFrameNumber(currentFrame)
            return returnVal
        else:
            return None
            
    def cacheFrames(self, imageIterator, firstFrame = 0):
        self.clear()
        self.zeroFrame = firstFrame
        self.rotateCounter = 0
        print('zeroFrame', self.zeroFrame)
        
        FrameCounter = 0
        for image in imageIterator:
            FrameCounter += 1
            self.append(image)
            sys.stdout.write("\rReading Frame "+str(FrameCounter))
        self.gotoFrameNumber(self.getCurrentFrameNumber())
        print('...done!')
    
    ###Pointer Functions###
    def getCurrentFrameNumber(self):
        return self.TimeIndicator.getCurrentFrameNumber()
    def getTopPosition(self):
        return self.TimeIndicator.getTopPosition()
    def setTopPosition(self, value):
        self.TimeIndicator.setTopPosition(value)
    def setCurrentFrameNumber(self, value):
        self.TimeIndicator.setCurrentFrameNumber(value)
        self.gotoFrameNumber(value)
    #####################
    
   