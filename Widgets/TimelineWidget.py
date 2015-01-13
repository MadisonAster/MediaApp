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

class TimelineWidget(NodeLinkedWidget, GraphWidget):
    def __init__(self):
        super(TimelineWidget, self).__init__()
        ################################
        self.setLinkedNode(AppCore.NodeGraph.createNode('TimelineNode'))
        
        self.modes = modeList(['None','zoomMode','panMode','marqMode', 'dragMode', 'dragCtiMode'])
        self.TimeIndicators = [DataStructures.TimeCache()]
        self.ctiIndex = 0
        self.ZTI = 0
        
        self.preferredNodeClass = 'TimelineNode'
    def getZeroFrame(self):
        return self.ZTI
    def setZeroFrame(self, value):
        self.ZTI = value
    def getCurrentIndicator(self):
        return self.TimeIndicators[self.ctiIndex]
    
    def cacheFrames(self):
        firstFrame, lastFrame = self.getFirstLastCacheFrame()
        self.getCurrentIndicator().cacheFrames(self.generateFrames(firstFrame, lastFrame), firstFrame = firstFrame)
    
    def generateFrames(self, firstFrame, lastFrame):
        print 'generating '+str(lastFrame-firstFrame)+' frames as QImages',
        for frame in range(firstFrame, lastFrame):
            node = self.getTopNodeAtFrame(frame)
            if node is None:
                yield AppCore.generateBlack()
            else:
                yield node.getImage(frame)
    def setMode(self):
        if self.middleClick == True and self.leftClick == True:
            self.modes.setCurrentMode('zoomMode')
        elif self.middleClick == True and self.leftClick == False:
            self.modes.setCurrentMode('panMode')
        elif self.middleClick == False and self.leftClick == True:
            for TimeIndicator in self.TimeIndicators:
                if QtCore.QRect(TimeIndicator.getCurrentFrame()-10,TimeIndicator.getTopPosition()*24,20,24).contains(self.startModeX,self.startModeY):
                    self.modes.setCurrentMode('dragCtiMode')
                    
                    self.CTIList = [TimeIndicator]
                    self.CTIxpos = [TimeIndicator.getCurrentFrame()]
                    self.CTIypos = [TimeIndicator.getTopPosition()]

                    for indicator in self.TimeIndicators:
                        if indicator.getCurrentFrame() == self.CTIxpos[0]:
                            if indicator != TimeIndicator:
                                self.CTIList.append(indicator)
                                self.CTIxpos.append(indicator.getCurrentFrame())
                                self.CTIypos.append(indicator.getTopPosition())
                    
                    break
            else:
                for node in self.allNodes():  #TODO-005: change AppCore.Nodes to an ordered dict so that nodes will be looped top to bottom here
                    if node.fallsAround(self.startModeX, self.startModeY):
                        self.modes.setCurrentMode('dragMode')
                        if node['selected'].getValue() != True:
                            for node2 in self.selectedNodes():
                                node2['selected'].setValue(False)
                            node['selected'].setValue(True)
                        break
                else:
                    self.modes.setCurrentMode('marqMode')
        else:
            self.modes.setCurrentMode('None')   
    def dragCtiEvent(self):
        for i in range(len(self.CTIList)):
            self.CTIList[i]
            xpos = int(round((self.CTIxpos[i]+self.curModeX-self.startModeX)/self.XPixelsPerUnit))
            ypos = int(round((self.CTIypos[i]+self.curModeY-self.startModeY)/self.YPixelsPerUnit))
            self.CTIList[i].setCurrentFrame(xpos)
            self.CTIList[i].setTopPosition(ypos)

    def dragEventExtra(self):
        for node in self.dragStartPositions:
            xpos = round((node[1]+self.curModeX-self.startModeX)/self.XPixelsPerUnit)*self.XPixelsPerUnit
            ypos = round((node[2]+self.curModeY-self.startModeY)/self.YPixelsPerUnit)*self.YPixelsPerUnit
            node[0]['startAt'].setValue(xpos)
            
            length = node[0]['width'].getValue()
            
            #xpos*length
        #FLAW: need to implement AppCore.registeredWidgets
        AppCore.ViewerWidget.repaint()
            
    def paintExtra(self, painter):
        #Draw cti and zti here!

        pen = AppCore.AppPrefs[self.className+'-ztiPen']
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(self.getZeroFrame(),self.visibleTop, self.getZeroFrame(),self.visibleBottom)
        
        
        pen = QtGui.QPen(AppCore.AppPrefs[self.className+'-ctiPen'].color())
        pen.setCosmetic(True)
        painter.setPen(pen)
        
        penColor = pen.color()
        penColor.setAlpha(128)
        painter.setBrush(QtGui.QBrush(penColor))
        for TimeIndicator in self.TimeIndicators:
            painter.drawLine(TimeIndicator.getCurrentFrame(),TimeIndicator.getTopPosition()*24, TimeIndicator.getCurrentFrame(),self.visibleBottom)
            painter.drawLine(TimeIndicator.getCurrentFrame()+1,TimeIndicator.getTopPosition()*24, TimeIndicator.getCurrentFrame()+1,self.visibleBottom)
            painter.drawRect(TimeIndicator.getCurrentFrame()-10,TimeIndicator.getTopPosition()*24,20,24)
            
            penColor.setHsv(penColor.hue()+66, 255, 255)
            penColor.setAlpha(255)
            pen.setColor(penColor)
            painter.setPen(pen)
            penColor.setAlpha(128)
            painter.setBrush(QtGui.QBrush(penColor))
            
    def keyPressEvent(self, event):
        print 'timeline', event.key()
        if event.key() == 16777220: #Enter
            for node in AppCore.selectedNodes():
                AppCore.PropertiesBin.dockThisWidget(node)    
        elif event.key() == 16777234: #Left 
            self.moveCurrentFrame(-1)
            AppCore.ViewerWidget.updateFrame()
            AppCore.ViewerWidget.repaint()
        elif event.key() == 16777236: #Right
            self.moveCurrentFrame(1)
            AppCore.ViewerWidget.updateFrame()
            AppCore.ViewerWidget.repaint()
        elif event.key() == 67: #C
            self.cacheFrames()
        self.repaint()
    
    def mouseMoveEvent(self, event):
        self.curMouseX = event.pos().x()
        self.curMouseY = event.pos().y()
        self.curModeX, self.curModeY = self.graphTrans.inverted()[0].map(self.curMouseX, self.curMouseY)
        
        if self.modes.getCurrentMode() == 'zoomMode':
            self.zoomEvent()
        elif self.modes.getCurrentMode() == 'panMode':
            self.panEvent()
        elif self.modes.getCurrentMode() == 'marqMode':
            self.marqEvent()
        elif self.modes.getCurrentMode() == 'dragMode':
            self.dragEvent()
        elif self.modes.getCurrentMode() == 'dragCtiMode':
            self.dragCtiEvent()
        self.update() #Redraw 
    def getTopNodeForCurrentFrame(self, notNode = None):
        return self.getTopNodeAtFrame(self.getCurrentFrame(), notNode = notNode)
        
    def getTopNodeAtFrame(self, Frame, notNode = None):
        nodeStack = self.getNodesAtPos(Frame)
        
        returnNode = None
        for node in nodeStack:
            if node != notNode:
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
        
    
        
    ###Pointer Functions###
    def getCurrentFrame(self):
        return self.getCurrentIndicator().getCurrentFrame()
    def setCurrentFrame(self, value):
        self.getCurrentIndicator().setCurrentFrame(value)
    def moveCurrentFrame(self, value, playback = False):
        self.getCurrentIndicator().moveCurrentFrame(value, playback = playback)
    def getImage(self):
        image = self.getCurrentIndicator().getFrame()
        if image is None:
            image = AppCore.generateBlack()
        return image
    def getCache(self):
        return self.getCurrentIndicator()