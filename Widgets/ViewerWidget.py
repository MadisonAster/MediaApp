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
class modeList(list):
    def __init__(self, *args):
        super(modeList, self).__init__(*args)
        self.currentMode = 0
    def getCurrentMode(self):
        return self[self.currentMode]
    def getCurrentModeIndex(self):
        return self.currentMode
    def setCurrentMode(self, arg):
        if type(arg) == int:
            self.currentMode = i
        elif type(arg) == str:
            for i, mode in enumerate(self):
                if mode == arg:
                    self.currentMode = i
        
class ViewerWidget(QtGui.QWidget):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(ViewerWidget, self).__init__()
        self.className = self.__class__.__name__
        ################################
        
        #Initialize Values
        self.modes = modeList(['None','zoomMode','panMode','marqMode'])
        self.middleClick = False
        self.leftClick = False
        self.rightClick = False

        #Initialize User Values#
        self.ZoomXYJoined = Core.AppSettings[self.className+'-ZoomXYJoined']
        self.XPixelsPerUnit = Core.AppSettings[self.className+'-XPixelsPerUnit']
        self.YPixelsPerUnit = Core.AppSettings[self.className+'-YPixelsPerUnit']
        self.upperXZoomLimit = Core.AppSettings[self.className+'-upperXZoomLimit']
        self.upperYZoomLimit = Core.AppSettings[self.className+'-upperYZoomLimit']
        self.lowerXZoomLimit = Core.AppSettings[self.className+'-lowerXZoomLimit']
        self.lowerYZoomLimit = Core.AppSettings[self.className+'-lowerYZoomLimit']
        self.zoomSensitivity = 100.0/Core.AppSettings[self.className+'-zoomSensitivity']

        self.curGraphX = Core.AppAttributes[self.className+'-startGraphX']
        self.curGraphY = Core.AppAttributes[self.className+'-startGraphY']
        self.curGraphXS = Core.AppAttributes[self.className+'-startGraphXS']
        self.curGraphYS = Core.AppAttributes[self.className+'-startGraphYS']
        
        #Go
        self.initUI()
        
    def initUI(self):
        self.setMinimumSize(0, 0)
        self.setGeometry(0, 0, 0, 0)
        self.setMouseTracking(True)
        
        #ToolBar#
        #toolbar = self.addToolBar('Exit')
        #toolbar.addAction(exitAction)
        #/ToolBar#
        
        #Status Bar#
        #self.statusBar()
        #/Status Bar#
        
    def mousePressEvent(self, event):
        self.startMouseX = event.pos().x()
        self.startMouseY = event.pos().y()
        self.startModeX, self.startModeY = self.graphTrans.inverted()[0].map(self.startMouseX, self.startMouseY)
            
        button = str(event.button())
        
        self.changeButton(button, True)
        self.setMode()
        self.grabValues()
        self.update()
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
            self.modes.setCurrentMode('marqMode')
        else:
            self.modes.setCurrentMode('None')
    def grabValues(self):
        Core.AppAttributes[self.className+'-startGraphX'] = self.curGraphX
        Core.AppAttributes[self.className+'-startGraphY'] = self.curGraphY
        Core.AppAttributes[self.className+'-startGraphXS'] = self.curGraphXS
        Core.AppAttributes[self.className+'-startGraphYS'] = self.curGraphYS
        self.endModeX = self.startModeX
        self.endModeY = self.startModeY
        
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
        self.update() #Redraw      
    def panEvent(self):
        self.curGraphX = Core.AppAttributes[self.className+'-startGraphX']+(self.curMouseX-self.startMouseX)
        self.curGraphY = Core.AppAttributes[self.className+'-startGraphY']+(self.curMouseY-self.startMouseY)
    def zoomEvent(self):
        posDeltaX = (self.curMouseX-self.startMouseX)
        posDeltaY = (self.curMouseY-self.startMouseY)
        scaleDeltaX = posDeltaX/self.zoomSensitivity
        scaleDeltaY = posDeltaY/self.zoomSensitivity*-1
        
        if self.ZoomXYJoined == True:
            self.curGraphXS = Core.AppAttributes[self.className+'-startGraphXS']+(scaleDeltaX+scaleDeltaY)/2
            self.curGraphYS = Core.AppAttributes[self.className+'-startGraphYS']+(scaleDeltaX+scaleDeltaY)/2
        else:
            self.curGraphXS = Core.AppAttributes[self.className+'-startGraphXS']+scaleDeltaX
            self.curGraphYS = Core.AppAttributes[self.className+'-startGraphYS']+scaleDeltaY
        
        difScaleX = self.curGraphXS-Core.AppAttributes[self.className+'-startGraphXS']
        difScaleY = self.curGraphYS-Core.AppAttributes[self.className+'-startGraphYS']
        
        if self.curGraphXS > self.upperXZoomLimit:
            self.curGraphXS = self.upperXZoomLimit
        elif self.curGraphXS < self.lowerXZoomLimit:
            self.curGraphXS = self.lowerXZoomLimit
        else:
            self.curGraphX = Core.AppAttributes[self.className+'-startGraphX']-(self.startModeX*difScaleX)
            
        if self.curGraphYS > self.upperYZoomLimit:
            self.curGraphYS = self.upperYZoomLimit  
        elif self.curGraphYS < self.lowerYZoomLimit:
            self.curGraphYS = self.lowerYZoomLimit
        else:
            self.curGraphY = Core.AppAttributes[self.className+'-startGraphY']-(self.startModeY*difScaleY)   
    def marqEvent(self):
        self.endModeX = self.curModeX
        self.endModeY = self.curModeY
        self.marqContains()
    def marqContains(self):
        pass
        #Sample Pixels here
                    
    def paintEvent(self, a):
        painter = QtGui.QPainter(self)
        
        #DrawBG
        self.widgetSize = self.size()
        painter.setBrush(Core.AppPrefs[self.className+'-bgColor'])
        painter.drawRect(0, 0, self.widgetSize.width(), self.widgetSize.height())
        
        #SetTransform
        self.graphTrans = QtGui.QTransform()
        self.graphTrans.translate(self.curGraphX, self.curGraphY)
        self.graphTrans.scale(self.curGraphXS+1, self.curGraphYS+1)
        painter.setTransform(self.graphTrans)

        #DrawResolutionBox
        painter.setBrush(Core.AppPrefs[self.className+'-ResBoxColor'])
        pen = Core.AppPrefs[self.className+'-ResBoxPen']
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawRect(0, 0, 800, 600)
        
        #DrawBoundingBox
        
        #DrawImage
        
        #DrawMarq
        if self.modes.getCurrentMode() == 'marqMode':
            marqX = [self.startModeX, self.endModeX]
            marqY = [self.startModeY, self.endModeY]
            marqX.sort()
            marqY.sort()
            painter.setBrush(Core.AppPrefs[self.className+'-marqBoxColor'])
            pen = Core.AppPrefs[self.className+'-marqOutlinePen']
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawRect(marqX[0], marqY[0], marqX[1]-marqX[0], marqY[1]-marqY[0]) 
        
        #Finished
        painter.end()