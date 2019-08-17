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

from collections import deque
from time import time

from Qt import QtGui, QtCore

import AppCore
import DataStructures
import MediaAppIcons
import MediaAppKnobs
from .NodeLinkedWidget import *
from .GraphWidget import *

class TimelineWidget(GraphWidget, NodeLinkedWidget):
    def __init__(self):
        super(TimelineWidget, self).__init__(objectName='TimelineWidget', accessibleName='TimelineWidget')
        self.setLinkedNode(AppCore.NodeGraph.createNode('TimelineNode'))
        self.setFocusPolicy(AppCore.AppSettings['FocusPolicy'])
        
        self.modes.append('dragCtiMode')
        self.TimeIndicators = [DataStructures.TimeCache()]
        self.ctiIndex = 0
        self.ZTI = 0
        
        self.preferredNodeClass = 'TimelineNode'

        self.addToolBars() 
    def addToolBars(self):
        self.topToolBar = QtGui.QToolBar('Top Tool Bar')
        self.leftToolBar = QtGui.QToolBar('Left Tool Bar')

        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.topToolBar.addWidget(spacer)
        
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.topToolBar)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.leftToolBar)
        
    ###Input Events###
    #def subclassPressEvents(self, event):
    ##################
    
    ###Button Handling###
    def subclassModes(self, event):
        for TimeIndicator in self.TimeIndicators:
            if QtCore.QRectF(TimeIndicator.getCurrentFrameNumber()-10,TimeIndicator.getTopPosition(),20,1).contains(self.startModeX,self.startModeY):
                self.modes.setCurrentMode('dragCtiMode')
                
                self.CTIList = [TimeIndicator]
                self.CTIxpos = [TimeIndicator.getCurrentFrameNumber()]
                self.CTIypos = [TimeIndicator.getTopPosition()]
                for indicator in self.TimeIndicators:
                    if indicator.getCurrentFrameNumber() == self.CTIxpos[0]:
                        if indicator != TimeIndicator:
                            self.CTIList.append(indicator)
                            self.CTIxpos.append(indicator.getCurrentFrameNumber())
                            self.CTIypos.append(indicator.getTopPosition())
                break
        else:
            for node in self.allNodes():  #TODO-005: change AppCore.Nodes to an ordered dict so that nodes will be looped top to bottom here
                if node.fallsAround(self.startModeX*self.XPixelsPerUnit, self.startModeY*self.YPixelsPerUnit):
                    self.modes.setCurrentMode('dragMode')
                    if node['selected'].getValue() != True:
                        for node2 in self.selectedNodes():
                            node2['selected'].setValue(False)
                        node['selected'].setValue(True)
                    break
            else:
                self.modes.setCurrentMode('marqMode')
        self.initialValues(event)
    #####################
    
    ###ModeEvents###
    def subclassModeEvents(self, event):
        if self.modes.getCurrentMode() == 'marqMode':
            self.marqEvent()
        elif self.modes.getCurrentMode() == 'dragMode':
            self.dragEvent()
        elif self.modes.getCurrentMode() == 'dragCtiMode':
            self.dragCtiEvent()
    
    def dragCtiEvent(self):
        for i in range(len(self.CTIList)):
            self.CTIList[i]
            xpos = int(round(self.CTIxpos[i]+self.curModeX-self.startModeX))
            ypos = int(round(self.CTIypos[i]+self.curModeY-self.startModeY))
            self.CTIList[i].setCurrentFrameNumber(xpos)
            self.CTIList[i].setTopPosition(ypos)
        AppCore.ViewerWidget.updateFrame()
        AppCore.ViewerWidget.repaint()
    def dragEventExtra(self):
        for node in self.dragStartPositions:
            xpos = round(node[1]+self.curModeX-self.startModeX)
            ypos = round(node[2]+self.curModeY-self.startModeY)
            node[0]['startAt'].setValue(xpos)
            
            length = node[0]['width'].getValue()
            
            #xpos*length
        #FLAW: need to implement AppCore.registeredWidgets
        AppCore.ViewerWidget.repaint()
    #################
    
    ###PaintEvents###
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
            painter.drawLine(TimeIndicator.getCurrentFrameNumber(),TimeIndicator.getTopPosition()*self.YPixelsPerUnit, TimeIndicator.getCurrentFrameNumber(),self.visibleBottom)
            painter.drawLine(TimeIndicator.getCurrentFrameNumber()+1,TimeIndicator.getTopPosition()*self.YPixelsPerUnit, TimeIndicator.getCurrentFrameNumber()+1,self.visibleBottom)
            painter.drawRect(TimeIndicator.getCurrentFrameNumber()-10,TimeIndicator.getTopPosition()*self.YPixelsPerUnit,20,1*self.YPixelsPerUnit)
            
            penColor.setHsv(penColor.hue()+66, 255, 255)
            penColor.setAlpha(255)
            pen.setColor(penColor)
            painter.setPen(pen)
            penColor.setAlpha(128)
            painter.setBrush(QtGui.QBrush(penColor))
    #################
    
    ###Other Functions###
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
        print('generating '+str(lastFrame-firstFrame)+' frames as QImages',)
        for frame in range(firstFrame, lastFrame):
            node = self.getTopNodeAtFrame(frame, top = self.getCurrentIndicator().getTopPosition())
            if node is None:
                yield AppCore.generateBlack()
            else:
                yield node.getImage(frame)
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
    def getTopNodeForCurrentFrame(self, notNode = None):
        return self.getTopNodeAtFrame(self.getCurrentFrameNumber(), notNode = notNode)
    def getTopNodeAtFrame(self, Frame, notNode = None, top = None):
        nodeStack = self.getNodesAtPos(Frame)
        
        returnNode = None
        for node in nodeStack:
            if top is None:
                topVal = node['ypos'].getValue()
            else:
                topVal = top
            if node != notNode:
                if node['ypos'].getValue() >= topVal:
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
    
    def frameForward(self):
        self.moveCurrentFrameNumber(1)
        AppCore.ViewerWidget.updateFrame()
        AppCore.ViewerWidget.repaint()
    def frameBackward(self):
        self.moveCurrentFrameNumber(-1)
        AppCore.ViewerWidget.updateFrame()
        AppCore.ViewerWidget.repaint()
    def openNodes(self):
        for node in AppCore.selectedNodes():
            AppCore.PropertiesBin.dockThisWidget(node)
    #####################
        
    ###Pointer Functions###
    def getCurrentFrameNumber(self):
        return self.getCurrentIndicator().getCurrentFrameNumber()
    def setCurrentFrameNumber(self, value):
        self.getCurrentIndicator().setCurrentFrameNumber(value)
        self.update()
    def moveCurrentFrameNumber(self, value, playback = False):
        self.getCurrentIndicator().moveCurrentFrameNumber(value, playback = playback)
    def getImage(self):
        image = self.getCurrentIndicator().getCurrentImage()
        if image is None:
            image = AppCore.generateBlack()
        return image
    def getImageAt(self, frame):
        return self.getCurrentIndicator().getImageAt(frame)
    def getCache(self):
        return self.getCurrentIndicator()
    #####################
    
    pass
    
    

        
        
