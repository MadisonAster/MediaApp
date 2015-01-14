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

from PySide import QtGui, QtCore
import AppCore
from DataStructures import NodeOwningObject

class modeList(list):
    def __init__(self, *args):
        super(modeList, self).__init__(*args)
        self.currentMode = 0
    def getCurrentMode(self):
        return self[self.currentMode]
    def getCurrentModeIndex(self):
        return self.currentMode
    def setCurrentMode(self, arg):
        if type(arg) is int:
            self.currentMode = i
        elif type(arg) is str:
            for i, mode in enumerate(self):
                if mode == arg:
                    self.currentMode = i
        
class GraphWidget( NodeOwningObject, QtGui.QWidget):
    def __init__(self):
        super(GraphWidget, self).__init__()
        self.className = self.__class__.__name__
        
        #Initialize Values
        self.modes = modeList(['None','zoomMode','panMode','marqMode', 'dragMode'])
        self.middleClick = False
        self.leftClick = False
        self.rightClick = False

        #Initialize User Values#
        self.ZoomXYJoined = AppCore.AppSettings[self.className+'-ZoomXYJoined']
        self.XPixelsPerUnit = AppCore.AppSettings[self.className+'-XPixelsPerUnit']
        self.YPixelsPerUnit = AppCore.AppSettings[self.className+'-YPixelsPerUnit']
        self.PaintXGridLines = AppCore.AppSettings[self.className+'-PaintXGridLines']
        self.PaintYGridLines = AppCore.AppSettings[self.className+'-PaintYGridLines']
        self.upperXZoomLimit = AppCore.AppSettings[self.className+'-upperXZoomLimit']
        self.upperYZoomLimit = AppCore.AppSettings[self.className+'-upperYZoomLimit']
        self.lowerXZoomLimit = AppCore.AppSettings[self.className+'-lowerXZoomLimit']
        self.lowerYZoomLimit = AppCore.AppSettings[self.className+'-lowerYZoomLimit']
        self.zoomSensitivity = 100.0/AppCore.AppSettings[self.className+'-zoomSensitivity']

        self.curGraphX = AppCore.AppAttributes[self.className+'-GraphX']
        self.curGraphY = AppCore.AppAttributes[self.className+'-GraphY']
        self.curGraphXS = AppCore.AppAttributes[self.className+'-GraphXS']
        self.curGraphYS = AppCore.AppAttributes[self.className+'-GraphYS']
        
        #Go
        self.setFocusPolicy(AppCore.AppSettings['FocusPolicy'])
        self.initUI()
    def initUI(self):
        self.setMinimumSize(0, 0)
        self.setGeometry(0, 0, 0, 0)
        self.setMouseTracking(True)
    
    def mousePressEvent(self, event):
        self.startMouseX = event.pos().x()
        self.startMouseY = event.pos().y()
        self.startModeX, self.startModeY = self.graphTrans.inverted()[0].map(self.startMouseX, self.startMouseY)
            
        button = str(event.button())
        
        self.changeButton(button, True)
        self.setMode()
        self.grabValues()
        self.update()
        
    def mouseDoubleClickEvent(self, event):
        dx = event.x()
        dy = event.y()
        
        for node in self.allNodes():
            if node.fallsAround(dx, dy):
                AppCore.PropertiesBin.dockThisWidget(node)
                
    def keyPressEvent(self, event):
        if event.key() == 16777220:                                 #Enter
            for node in self.selectedNodes():
                AppCore.PropertiesBin.dockThisWidget(node)
    
    def mouseReleaseEvent(self, event):
        self.endMouseX = event.pos().x()
        self.endMouseY = event.pos().y()
        self.endModeX, self.endModeY = self.graphTrans.inverted()[0].map(self.endMouseX, self.endMouseY)
        
        button = str(event.button())
        
        self.changeButton(button, False)
        self.setMode()
        self.grabValues()
        self.update()
    def changeButton(self, button, Value):
        if button.rsplit('.', 1)[1] == 'MiddleButton' or button.rsplit('.', 1)[1] == 'MidButton':
            self.middleClick = Value
        elif button.rsplit('.', 1)[1] == 'LeftButton':
            self.leftClick = Value
        elif button.rsplit('.', 1)[1] == 'RightButton':
            self.rightClick = Value
    def setMode(self):
        if self.middleClick == True and self.leftClick == True:
            self.modes.setCurrentMode('zoomMode')
        elif self.middleClick == True and self.leftClick == False:
            self.modes.setCurrentMode('panMode')
        elif self.middleClick == False and self.leftClick == True:
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
    def grabValues(self):
        AppCore.AppAttributes[self.className+'-GraphX'] = self.curGraphX
        AppCore.AppAttributes[self.className+'-GraphY'] = self.curGraphY
        AppCore.AppAttributes[self.className+'-GraphXS'] = self.curGraphXS
        AppCore.AppAttributes[self.className+'-GraphYS'] = self.curGraphYS
        self.endModeX = self.startModeX
        self.endModeY = self.startModeY
        
        
        self.dragStartPositions = []
        for node in self.selectedNodes():
            self.dragStartPositions.append([node,node['xpos'].getValue(),node['ypos'].getValue()])
        
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
        self.update() #Redraw      
    def panEvent(self):
        self.curGraphX = AppCore.AppAttributes[self.className+'-GraphX']+(self.curMouseX-self.startMouseX)
        self.curGraphY = AppCore.AppAttributes[self.className+'-GraphY']+(self.curMouseY-self.startMouseY)
    def zoomEvent(self):
        posDeltaX = (self.curMouseX-self.startMouseX)
        posDeltaY = (self.curMouseY-self.startMouseY)
        scaleDeltaX = posDeltaX/self.zoomSensitivity
        scaleDeltaY = posDeltaY/self.zoomSensitivity*-1
        
        if self.ZoomXYJoined == True:
            self.curGraphXS = AppCore.AppAttributes[self.className+'-GraphXS']+(scaleDeltaX+scaleDeltaY)/2
            self.curGraphYS = AppCore.AppAttributes[self.className+'-GraphYS']+(scaleDeltaX+scaleDeltaY)/2
        else:
            self.curGraphXS = AppCore.AppAttributes[self.className+'-GraphXS']+scaleDeltaX
            self.curGraphYS = AppCore.AppAttributes[self.className+'-GraphYS']+scaleDeltaY
        
        difScaleX = self.curGraphXS-AppCore.AppAttributes[self.className+'-GraphXS']
        difScaleY = self.curGraphYS-AppCore.AppAttributes[self.className+'-GraphYS']
        
        if self.curGraphXS > self.upperXZoomLimit:
            self.curGraphXS = self.upperXZoomLimit
        elif self.curGraphXS < self.lowerXZoomLimit:
            self.curGraphXS = self.lowerXZoomLimit
        else:
            self.curGraphX = AppCore.AppAttributes[self.className+'-GraphX']-(self.startModeX*difScaleX)
            
        if self.curGraphYS > self.upperYZoomLimit:
            self.curGraphYS = self.upperYZoomLimit  
        elif self.curGraphYS < self.lowerYZoomLimit:
            self.curGraphYS = self.lowerYZoomLimit
        else:
            self.curGraphY = AppCore.AppAttributes[self.className+'-GraphY']-(self.startModeY*difScaleY)   
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
                    
    def paintEvent(self, a):
        painter = QtGui.QPainter(self)
        
        #DrawBG
        self.widgetSize = self.size()
        painter.setBrush(AppCore.AppPrefs[self.className+'-bgColor'])
        painter.drawRect(0, 0, self.widgetSize.width(), self.widgetSize.height())
        
        #SetTransform
        self.graphTrans = QtGui.QTransform()
        self.graphTrans.translate(self.curGraphX, self.curGraphY)
        self.graphTrans.scale(self.curGraphXS+1, self.curGraphYS+1)
        painter.setTransform(self.graphTrans)
        
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