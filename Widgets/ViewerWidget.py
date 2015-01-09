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
from time import time, sleep

from PySide import QtGui, QtCore

import AppCore
from NodeLinkedWidget import *

class modeList(list):
    def __init__(self, *args):
        super(modeList, self).__init__(*args)
        self.currentMode = 0
        
        self.frameCache = None
        self.frameCacheFrame = None
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
        
        
class Viewer(QtGui.QWidget):
    def __init__(self):
        super(Viewer, self).__init__()
        self.className = self.__class__.__name__
        
        self.setFocusPolicy(AppCore.AppSettings['FocusPolicy'])
        self.setMouseTracking(True)
        self.setMinimumSize(0, 0)
        self.setGeometry(0, 0, 0, 0)
        
        #Initialize Values
        self.modes = modeList(['None','zoomMode','panMode','marqMode'])
        self.middleClick = False
        self.leftClick = False
        self.rightClick = False

        #Initialize User Values#
        self.ZoomXYJoined = AppCore.AppSettings[self.className+'-ZoomXYJoined']
        self.XPixelsPerUnit = AppCore.AppSettings[self.className+'-XPixelsPerUnit']
        self.YPixelsPerUnit = AppCore.AppSettings[self.className+'-YPixelsPerUnit']
        self.upperXZoomLimit = AppCore.AppSettings[self.className+'-upperXZoomLimit']
        self.upperYZoomLimit = AppCore.AppSettings[self.className+'-upperYZoomLimit']
        self.lowerXZoomLimit = AppCore.AppSettings[self.className+'-lowerXZoomLimit']
        self.lowerYZoomLimit = AppCore.AppSettings[self.className+'-lowerYZoomLimit']
        self.zoomSensitivity = 100.0/AppCore.AppSettings[self.className+'-zoomSensitivity']

        self.curGraphX = AppCore.AppAttributes[self.className+'-startGraphX']
        self.curGraphY = AppCore.AppAttributes[self.className+'-startGraphY']
        self.curGraphXS = AppCore.AppAttributes[self.className+'-startGraphXS']
        self.curGraphYS = AppCore.AppAttributes[self.className+'-startGraphYS']
        
        self.frameCache = AppCore.generateBlack()
    
    def keyPressEvent(self, event):
        print 'viewer', event.key()
        if event.key() == 16777234: #Left 
            AppCore.moveCurrentFrame(-1)
            self.updateFrame()
            AppCore.TimelineWidget.repaint()
        if event.key() == 16777236: #Right
            AppCore.moveCurrentFrame(1)
            print AppCore.data['frameCache'].rotateCounter
            self.updateFrame()
            print self.frameCache
            AppCore.TimelineWidget.repaint()
        if event.key() == 67: #C
            AppCore.TimelineWidget.cacheFrames()
        if event.key() == 32: #Space
            self.playForward()
        self.repaint()
        
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
        AppCore.AppAttributes[self.className+'-startGraphX'] = self.curGraphX
        AppCore.AppAttributes[self.className+'-startGraphY'] = self.curGraphY
        AppCore.AppAttributes[self.className+'-startGraphXS'] = self.curGraphXS
        AppCore.AppAttributes[self.className+'-startGraphYS'] = self.curGraphYS
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
        self.curGraphX = AppCore.AppAttributes[self.className+'-startGraphX']+(self.curMouseX-self.startMouseX)
        self.curGraphY = AppCore.AppAttributes[self.className+'-startGraphY']+(self.curMouseY-self.startMouseY)
    def zoomEvent(self):
        posDeltaX = (self.curMouseX-self.startMouseX)
        posDeltaY = (self.curMouseY-self.startMouseY)
        scaleDeltaX = posDeltaX/self.zoomSensitivity
        scaleDeltaY = posDeltaY/self.zoomSensitivity*-1
        
        if self.ZoomXYJoined == True:
            self.curGraphXS = AppCore.AppAttributes[self.className+'-startGraphXS']+(scaleDeltaX+scaleDeltaY)/2
            self.curGraphYS = AppCore.AppAttributes[self.className+'-startGraphYS']+(scaleDeltaX+scaleDeltaY)/2
        else:
            self.curGraphXS = AppCore.AppAttributes[self.className+'-startGraphXS']+scaleDeltaX
            self.curGraphYS = AppCore.AppAttributes[self.className+'-startGraphYS']+scaleDeltaY
        
        difScaleX = self.curGraphXS-AppCore.AppAttributes[self.className+'-startGraphXS']
        difScaleY = self.curGraphYS-AppCore.AppAttributes[self.className+'-startGraphYS']
        
        if self.curGraphXS > self.upperXZoomLimit:
            self.curGraphXS = self.upperXZoomLimit
        elif self.curGraphXS < self.lowerXZoomLimit:
            self.curGraphXS = self.lowerXZoomLimit
        else:
            self.curGraphX = AppCore.AppAttributes[self.className+'-startGraphX']-(self.startModeX*difScaleX)
            
        if self.curGraphYS > self.upperYZoomLimit:
            self.curGraphYS = self.upperYZoomLimit  
        elif self.curGraphYS < self.lowerYZoomLimit:
            self.curGraphYS = self.lowerYZoomLimit
        else:
            self.curGraphY = AppCore.AppAttributes[self.className+'-startGraphY']-(self.startModeY*difScaleY)   
    def marqEvent(self):
        self.endModeX = self.curModeX
        self.endModeY = self.curModeY
        self.marqContains()
    def marqContains(self):
        pass
        #Sample Pixels here
    
    def playForward(self):
        frameperiod=1.0/AppCore.AppAttributes['FPS']
        now = time()
        nextframe = now
        
        for image in AppCore.data['frameCache']:
            while now < nextframe:
                sleep(nextframe-now)
                now = time()
                
            self.frameCache = image
            #Maybe some overhead here
            AppCore.moveCurrentFrame(1, playback = True)
            self.repaint()
            
            nextframe += frameperiod
            
    def updateFrame(self):
        if AppCore.getCurrentFrame() in AppCore.data['frameCache']:
            self.frameCache = AppCore.data['frameCache'][0]
        else:
            self.frameCache = AppCore.generateBlack()
    
    def paintEvent(self, a):
        painter = QtGui.QPainter(self)
        #ADD quickpaint here?
        
        
        #DrawBG
        self.widgetSize = self.size()
        painter.setBrush(AppCore.AppPrefs[self.className+'-bgColor'])
        painter.drawRect(0, 0, self.widgetSize.width(), self.widgetSize.height())
        
        #SetTransform
        self.graphTrans = QtGui.QTransform()
        self.graphTrans.translate(self.curGraphX, self.curGraphY)
        self.graphTrans.scale(self.curGraphXS+1, self.curGraphYS+1)
        painter.setTransform(self.graphTrans)
        
        
        #DrawImage
        
        #if self.frameCache is None or self.frameCacheFrame != AppCore.getCurrentFrame():
        #    self.frameCache =  self.node.getImage()
        #    self.frameCacheFrame = AppCore.getCurrentFrame()
        
        #self.frameCache =  self.node.getImage()
        painter.drawImage(QtCore.QRect(0,0,self.frameCache.width(),self.frameCache.height()), self.frameCache)
        
        #DrawResolutionBox
        painter.setBrush(AppCore.AppPrefs[self.className+'-ResBoxColor'])
        pen = AppCore.AppPrefs[self.className+'-ResBoxPen']
        pen.setCosmetic(True)
        painter.setPen(pen)
        #BUG: Diagonal line gets drawn here when zoomed in just the right way
        painter.drawRect(QtCore.QRect(-1,-1,self.frameCache.width()+2,self.frameCache.height()+2))
        
        #DrawBoundingBox
        
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
            painter.drawRect(marqX[0], marqY[0], marqX[1]-marqX[0], marqY[1]-marqY[0])
        
        #Finished
        painter.end()
        
class ViewerWidget(QtGui.QMainWindow, NodeLinkedWidget):
    def __init__(self):
        super(ViewerWidget, self).__init__()
        self.setDockOptions(False)
        self.setFocusPolicy(AppCore.AppSettings['FocusPolicy'])
        
        
        self.widget = Viewer()
        self.setCentralWidget(self.widget)
        
        self.node = AppCore.NodeGraph.createNode('ViewerNode')
        self.node.setViewerWidget(self.widget)
        
        #ToolBar#
        self.topToolBar = QtGui.QToolBar('Top Tool Bar')
        self.leftToolBar = QtGui.QToolBar('Left Tool Bar')
        self.rightToolBar = QtGui.QToolBar('Right Tool Bar')
        self.bottomToolBar = QtGui.QToolBar('Bottom Tool Bar')
        
        self.topToolBar.setMovable(False)
        self.leftToolBar.setMovable(False)
        self.rightToolBar.setMovable(False)
        self.bottomToolBar.setMovable(False)
        
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.topToolBar)
        #self.addToolBar(QtCore.Qt.LeftToolBarArea, self.leftToolBar)
        #self.addToolBar(QtCore.Qt.RightToolBarArea, self.rightToolBar)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.bottomToolBar)
        
        
        PlayForward = QtGui.QAction('PlayForward', self)
        PlayForward.setStatusTip('Close All the widgets in the bin.')
        PlayForward.triggered.connect(self.widget.playForward)
        
        self.bottomToolBar.addAction(PlayForward)
    def updateFrame(self):
        self.widget.updateFrame()