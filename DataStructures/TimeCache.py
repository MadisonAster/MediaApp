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

import AppCore
from .RingCache import RingCache

class TimeIndicator(object):
    def __init__(self):
        super(TimeIndicator, self).__init__()
        
        self.Position = 0
        self.Top = 0
    def getCurrentFrame(self):
        return self.Position
    def getTopPosition(self):
        return self.Top
    def setCurrentFrame(self, value):
        self.Position = value
    def setTopPosition(self, value):
        self.Top = value
        
    def moveCurrentFrame(self, value):
        self.Position += value
    
    
class TimeCache(object):
    def __init__(self):
        super(TimeCache, self).__init__()
        
        self.RingCache = RingCache()
        self.RingCache.append(None)
        
        self.TimeIndicator = TimeIndicator()
        
        #FLAW: need to keep track of frameCache size in AppCore somehow
        #AppCore.data['frameCache'] = 
        #AppCore.data['frameCache'].append(AppCore.generateBlack())
    def __iter__(self):
        for frame in self.RingCache:
            yield frame
    def getCurrentFrame(self):
        return self.TimeIndicator.getCurrentFrame()
    def setCurrentFrame(self, value):
        self.TimeIndicator.setCurrentFrame(value)
        self.RingCache.goto(value)
    def setTopPosition(self, value):
        self.TimeIndicator.setTopPosition(value)
    def moveCurrentFrame(self, value, playback = False):
        self.TimeIndicator.moveCurrentFrame(value)
        if playback is False:
            self.RingCache.rotate(-value)

    def cacheFrames(self, frameIterator, firstFrame = 0):
        self.RingCache = RingCache(zero = firstFrame)
        for frame in frameIterator:
            self.RingCache.append(frame)
            #print('.',)
        self.RingCache.goto(self.getCurrentFrame())
        print('done')
        
    def getTopPosition(self):
        return self.TimeIndicator.getTopPosition()

    def getFrame(self):
        if self.getCurrentFrame() in self.RingCache:
            return self.RingCache[0]
        else:
            return None
    def getFrameAt(self, frame):
        if frame in self.RingCache:
            currentFrame = self.getCurrentFrame()
            self.RingCache.goto(frame)
            returnVal = self.RingCache[0]
            self.RingCache.goto(currentFrame)
            return returnVal
        else:
            return None