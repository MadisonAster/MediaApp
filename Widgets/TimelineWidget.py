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

from PySide import QtGui, QtCore
from NodeLinkedWidget import *

from GraphWidget import *
class TimelineWidget(GraphWidget, NodeLinkedWidget):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(TimelineWidget, self).__init__(CorePointer)
        ################################
        self.node = Core.NodeGraph.createNode('TimelineNode')
        self.node.setTimelineWidget(self)
        
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
        Core.ViewerWidget.repaint()
            
    def paintExtra(self, painter):
        #Draw cti and zti here!

        pen = Core.AppPrefs[self.className+'-ztiPen']
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(Core.AppAttributes['ztiPos'],0, Core.AppAttributes['ztiPos'],24*10)
        
        
        pen = Core.AppPrefs[self.className+'-ctiPen']
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(Core.AppAttributes['ctiTop'][0],Core.AppAttributes['ctiTop'][1], Core.AppAttributes['ctiBot'][0],Core.AppAttributes['ctiBot'][1])
        
    def keyPressEvent(self, event):
        print event.key()
        if event.key() == 16777220:                                 #Enter
            for node in Core.selectedNodes():
                Core.PropertiesBin.dockThisWidget(node)    
        if event.key() == 16777234: #Left 
            Core.AppAttributes['ctiTop'][0] = Core.AppAttributes['ctiTop'][0]-1
            Core.AppAttributes['ctiBot'][0] = Core.AppAttributes['ctiTop'][0]
            Core.ViewerWidget.repaint()
        if event.key() == 16777236: #Right
            Core.AppAttributes['ctiTop'][0] = Core.AppAttributes['ctiTop'][0]+1
            Core.AppAttributes['ctiBot'][0] = Core.AppAttributes['ctiTop'][0]
            Core.ViewerWidget.repaint()

        self.repaint()
    
    def getTopNodeForCurrentFrame(self):
        nodeStack = self.getNodesAtPos(Core.getCurrentFrame())
        
        returnNode = None
        for node in nodeStack:
            if returnNode is None:
                returnNode = node
            elif node['ypos'].getValue() > returnNode['ypos'].getValue() and Core.AppSettings[self.className+'-YInverted'] is True:
                returnNode = node
            elif node['ypos'].getValue() < returnNode['ypos'].getValue() and Core.AppSettings[self.className+'-YInverted'] is False:
                returnNode = node
        return returnNode
        
    def getNodesAtPos(self, XPos):
        nodeStack = []
        #for node in Core.getChildrenOf(self):
        for node in self.allNodes():
            if node.fallsAround(XPos, None):
                nodeStack.append(node)
        return nodeStack
        
        
        
        
        
        