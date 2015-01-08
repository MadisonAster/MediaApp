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

from collections import deque

from PySide import QtGui, QtCore

import AppCore
import DataStructures
from NodeLinkedWidget import *
from GraphWidget import *

class TimelineWidget(GraphWidget, NodeLinkedWidget):
    def __init__(self):
        super(TimelineWidget, self).__init__()
        ################################
        self.node = AppCore.NodeGraph.createNode('TimelineNode')
        self.node.setTimelineWidget(self)
        
        AppCore.data['frameCache'] = DataStructures.dynamicCache()
        AppCore.data['frameCache'].append(AppCore.generateBlack())
        
        
    #def dragEvent(self):
    #    for node in self.dragStartPositions:
    #        xpos = round((node[1]+self.curModeX-self.startModeX)/self.XPixelsPerUnit)*self.XPixelsPerUnit
    #        ypos = round((node[2]+self.curModeY-self.startModeY)/self.YPixelsPerUnit)*self.YPixelsPerUnit
    #        node[0]['xpos'].setValue(xpos)
    #        node[0]['ypos'].setValue(ypos)
    #        node[0].getPos()
    #    self.dragEventExtra()
    def dragEventExtra(self):
        for node in self.dragStartPositions:
            xpos = round((node[1]+self.curModeX-self.startModeX)/self.XPixelsPerUnit)*self.XPixelsPerUnit
            ypos = round((node[2]+self.curModeY-self.startModeY)/self.YPixelsPerUnit)*self.YPixelsPerUnit
            node[0]['startAt'].setValue(xpos)
            
            length = node[0]['length'].getValue()
            
            #xpos*length
        AppCore.ViewerWidget.repaint()
            
    def paintExtra(self, painter):
        #Draw cti and zti here!

        pen = AppCore.AppPrefs[self.className+'-ztiPen']
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(AppCore.AppAttributes['ztiPos'],0, AppCore.AppAttributes['ztiPos'],24*10)
        
        
        pen = AppCore.AppPrefs[self.className+'-ctiPen']
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(AppCore.AppAttributes['ctiTop'][0],AppCore.AppAttributes['ctiTop'][1], AppCore.AppAttributes['ctiBot'][0],AppCore.AppAttributes['ctiBot'][1])
        painter.drawLine(AppCore.AppAttributes['ctiTop'][0]+1,AppCore.AppAttributes['ctiTop'][1], AppCore.AppAttributes['ctiBot'][0]+1,AppCore.AppAttributes['ctiBot'][1])
        
    def keyPressEvent(self, event):
        print 'timeline', event.key()
        if event.key() == 16777220: #Enter
            for node in AppCore.selectedNodes():
                AppCore.PropertiesBin.dockThisWidget(node)    
        elif event.key() == 16777234: #Left 
            AppCore.moveCurrentFrame(-1)
            AppCore.ViewerWidget.updateFrame()
            AppCore.ViewerWidget.repaint()
        elif event.key() == 16777236: #Right
            AppCore.moveCurrentFrame(1)
            AppCore.ViewerWidget.updateFrame()
            AppCore.ViewerWidget.repaint()
        elif event.key() == 67: #C
            self.cacheFrames()
        self.repaint()
    
    def getTopNodeForCurrentFrame(self):
        nodeStack = self.getNodesAtPos(AppCore.getCurrentFrame())
        
        returnNode = None
        for node in nodeStack:
            if returnNode is None:
                returnNode = node
            elif node['ypos'].getValue() > returnNode['ypos'].getValue() and AppCore.AppSettings[self.className+'-YInverted'] is True:
                returnNode = node
            elif node['ypos'].getValue() < returnNode['ypos'].getValue() and AppCore.AppSettings[self.className+'-YInverted'] is False:
                returnNode = node
        return returnNode
        
    def getTopNodeAtFrame(self, Frame):
        nodeStack = self.getNodesAtPos(Frame)
        
        returnNode = None
        for node in nodeStack:
            if returnNode is None:
                returnNode = node
            elif node['ypos'].getValue() > returnNode['ypos'].getValue() and AppCore.AppSettings[self.className+'-YInverted'] is True:
                returnNode = node
            elif node['ypos'].getValue() < returnNode['ypos'].getValue() and AppCore.AppSettings[self.className+'-YInverted'] is False:
                returnNode = node
        return returnNode
        
    def getNodesAtPos(self, XPos):
        nodeStack = []
        #for node in AppCore.getChildrenOf(self):
        for node in self.allNodes():
            if node.fallsAround(XPos, None):
                nodeStack.append(node)
        return nodeStack
        
    def getFirstLastCacheFrame(self):
        firstFrame = None
        lastFrame = None
        for node in self.allNodes():
            if firstFrame is None:
                firstFrame = node['xpos'].getValue()
                lastFrame = node['xpos'].getValue()+node['width'].getValue()
            if node['xpos'].getValue() < firstFrame:
                firstFrame = node['xpos'].getValue()
            if node['xpos'].getValue()+node['width'].getValue() > lastFrame:
                lastFrame = node['xpos'].getValue()+node['width'].getValue()
        return firstFrame, lastFrame
        
    def nodeCreate(self):
        #maybe unnecessary
        pass
        
    def cacheFrames(self):
        firstFrame, lastFrame = self.getFirstLastCacheFrame()
        print 'caching '+str(lastFrame-firstFrame)+' frames',
        AppCore.data['frameCache'] = DataStructures.dynamicCache(zero = firstFrame)
        for frame in range(firstFrame, lastFrame):
            node = self.getTopNodeAtFrame(frame)
            AppCore.data['frameCache'].append(node.getImage(frame))
            print '.',
        AppCore.data['frameCache'].goto(AppCore.getCurrentFrame())
        print 'done'
        
        
        
        
        