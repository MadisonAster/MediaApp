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
from time import time

from PySide import QtGui, QtCore
import AppCore
from DataStructures import NodeOwningObject
from AbstractGraphArea import AbstractGraphArea
   
class GraphWidget(NodeOwningObject, AbstractGraphArea):
    ###Initialize Class###
    def __init__(self):
        super(GraphWidget, self).__init__()
        self.className = self.__class__.__name__

        self.modes.append('marqMode')
        self.modes.append('dragMode')
        
        self.PaintXGridLines = AppCore.AppSettings[self.className+'-PaintXGridLines']
        self.PaintYGridLines = AppCore.AppSettings[self.className+'-PaintYGridLines']
    ######################
    
    ###Input Events###
    def subclassPressEvents(self, event):
        if self.pressedButtons == AppCore.AppPrefs[self.className+'-Shortcuts-OpenNode']:
            for node in self.selectedNodes():
                AppCore.PropertiesBin.dockThisWidget(node)
    ##################
    
    
    ###Button Handling###
    def subclassModes(self):
        if self.pressedButtons == AppCore.AppPrefs[self.className+'-Shortcuts-SelectNodes']:
            for node in reversed(self.allNodes()):  #TODO-005: change AppCore.Nodes to an ordered dict so that nodes will be looped top to bottom here
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
    #####################       
    
    ###InitalValues###
    def subclassInitialValues(self):
        self.dragStartPositions = []
        for node in self.selectedNodes():
            self.dragStartPositions.append([node,node['xpos'].getValue(),node['ypos'].getValue()])
    ##################
     
    ###ModeEvents###
    def subclassModeEvents(self, event):
        if self.modes.getCurrentMode() == 'marqMode':
            self.marqEvent()
        elif self.modes.getCurrentMode() == 'dragMode':
            self.dragEvent()  

    def marqEvent(self):
        self.endModeX = self.curModeX
        self.endModeY = self.curModeY
        self.marqContains()
    def marqContains(self):
        marqX = [self.startModeX, self.endModeX]
        marqY = [self.startModeY, self.endModeY]
        
        marqRect = QtCore.QRectF(self.startModeX, self.startModeY, self.endModeX-self.startModeX, self.endModeY-self.startModeY)
        for node in self.allNodes():
            if marqRect.contains(node.mappedNodeRect):
                node.toKnob('selected').setValue(True)
            else:
                node.toKnob('selected').setValue(False)
    def dragEvent(self):
        for node in self.dragStartPositions:
            #xpos = round((node[1]+self.curModeX-self.startModeX)/self.XPixelsPerUnit)*self.XPixelsPerUnit
            #ypos = round((node[2]+self.curModeY-self.startModeY)/self.YPixelsPerUnit)*self.YPixelsPerUnit
            xpos = round((node[1]+self.curModeX-self.startModeX)/self.XPixelsPerUnit)
            ypos = round((node[2]+self.curModeY-self.startModeY)/self.YPixelsPerUnit)
            node[0]['xpos'].setValue(xpos)
            node[0]['ypos'].setValue(ypos)
            node[0].getPos()
        self.dragEventExtra()
    def dragEventExtra(self):
        #Override this method
        pass
    #################
    
    ###PaintEvents###
    def subclassPaintEvent(self, pEvent, painter):
        self.visibleLeft, self.visibleTop = self.graphTrans.inverted()[0].map(0, 0)
        self.visibleRight, self.visibleBottom = self.graphTrans.inverted()[0].map(self.widgetSize.width(), self.widgetSize.height())

        #DrawGrid
        self.paintGrid(painter)
        
        #DrawNodes
        painter.setFont(AppCore.AppPrefs['AppFont'])
        for node in self.allNodes():
            node.drawNode(painter)
            #painter.setTransform(self.graphTrans)
            
        #DrawExtra
        self.paintExtra(painter)
        
        #DrawMarq
        if self.modes.getCurrentMode() == 'marqMode':
            marqX = [self.startModeX, self.endModeX]
            marqY = [self.startModeY, self.endModeY]
            marqX.sort()
            marqY.sort()
            painter.setBrush(AppCore.AppPrefs[self.className+'-marqBoxColor'])
            pen = AppCore.AppPrefs[self.className+'-marqOutlinePen']
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawRect(QtCore.QRectF(marqX[0], marqY[0], marqX[1]-marqX[0], marqY[1]-marqY[0])) 
        
        #Finished
        painter.end()
    def paintGrid(self, painter):
        pen = AppCore.AppPrefs[self.className+'-gridPen']
        pen.setCosmetic(True)
        painter.setPen(pen)
        
        if self.PaintYGridLines:
            for i in range(int(self.visibleLeft), int(self.visibleRight)):
                if i % self.XPixelsPerUnit == 0:
                    p1 = QtCore.QPoint(i, self.visibleTop)
                    p2 = QtCore.QPoint(i, self.visibleBottom)
                    painter.drawLine(p1, p2)
        if self.PaintXGridLines:     
            #TODO: get visible range
            for i in range(int(self.visibleTop), int(self.visibleBottom)):
                if i % self.YPixelsPerUnit == 0:
                    p1 = QtCore.QPoint(self.visibleLeft, i)
                    p2 = QtCore.QPoint(self.visibleRight, i)
                    painter.drawLine(p1, p2)
    def paintExtra(self, painter):
        #Override Me!
        pass
    #################
    
    ###Other Functions###
    def mouseDoubleClickEvent(self, event):
        dx = event.x()
        dy = event.y()
        
        for node in self.allNodes():
            if node.fallsAround(dx, dy):
                AppCore.PropertiesBin.dockThisWidget(node)
    #####################