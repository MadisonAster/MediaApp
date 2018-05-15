#===============================================================================
# @Author: Thomas McVay
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with Qt Library
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
import math
import copy

from Qt import QtGui, QtCore, QtWidgets, QtOpenGL
from OpenGL import GL
#from OpenGL import GL

import AppCore
import MediaAppIcons
import MediaAppKnobs
import DataStructures
from .NodeLinkedWidget import *
from .AbstractGraphArea import AbstractGraphArea

class ViewerWidget(QtWidgets.QWidget, NodeLinkedWidget):
    def __init__(self):
        super(ViewerWidget, self).__init__()
        AppCore.LoadUI(self)
        #print('Spacer', self.CentralLayout)
        
        self.ViewerWidget3D = ViewerWidget3D()
        self.ViewerWidget2D = ViewerWidget2D()
        self.addToolBars()
        
        self.SetCentralWidget(self.ViewerWidget2D)
        
        self.setLinkedNode(AppCore.NodeGraph.createNode('ViewerNode'))
        
    def SetCentralWidget(self, Widget):
        for i in range(self.CentralLayout.count()):
            self.CentralLayout.itemAt(i).widget().hide()
            self.CentralLayout.removeItem(self.CentralLayout.itemAt(i))
        self.CentralLayout.addWidget(Widget)
        Widget.show()
        
    def ChangeDimensions(self):
        if self.DimensionSwitcher.getValue() == '2D View':
            self.SetCentralWidget(self.ViewerWidget2D)
        elif self.DimensionSwitcher.getValue() == '3D View':
            self.SetCentralWidget(self.ViewerWidget3D)
        
    def addToolBars(self):
        self.topToolBar = QtWidgets.QToolBar('Top Tool Bar')
        self.leftToolBar = QtWidgets.QToolBar('Left Tool Bar')
        self.rightToolBar = QtWidgets.QToolBar('Right Tool Bar')
        self.bottomToolBar = QtWidgets.QToolBar('Bottom Tool Bar')
        
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.topToolBar)
        #self.addToolBar(QtCore.Qt.LeftToolBarArea, self.leftToolBar)
        #self.addToolBar(QtCore.Qt.RightToolBarArea, self.rightToolBar)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.bottomToolBar)
        
        
        ###Top Toolbar###
        self.DimensionSwitcher = MediaAppKnobs.ComboKnob(['2D View','3D View'])
        
        self.DimensionSwitcher.showName(False)
        self.DimensionSwitcher.setChanged(self.ChangeDimensions)
        self.topToolBar.addWidget(self.DimensionSwitcher)
        
        self.topToolBar.addWidget(MediaAppKnobs.Spacer())
        
        self.inputSelectorA = MediaAppKnobs.ComboKnob([])
        self.inputSelectorA.showName(False)
        self.topToolBar.addWidget(self.inputSelectorA)
        
        self.inputCombiner = MediaAppKnobs.ComboKnob(['A Only','B Only','Wipe','Blend'])
        self.inputCombiner.showName(False)
        self.topToolBar.addWidget(self.inputCombiner)
        
        self.inputSelectorB = MediaAppKnobs.ComboKnob([])
        self.inputSelectorB.showName(False)
        self.topToolBar.addWidget(self.inputSelectorB)

        self.topToolBar.addWidget(MediaAppKnobs.Spacer())
        
        self.UpdateButton = MediaAppKnobs.ComboKnob(['PUSHBUTTON?'])
        self.UpdateButton.showName(False)
        self.topToolBar.addWidget(self.UpdateButton)
        
        ##################
        
        self.bottomToolBar.addWidget(MediaAppKnobs.Spacer())
        

        RNext = QtWidgets.QAction(MediaAppIcons.RNext(), 'RNext', self)
        RNext.triggered.connect(self.ViewerWidget2D.playForward)
        self.bottomToolBar.addAction(RNext)
        
        RPlay = QtWidgets.QAction(MediaAppIcons.RPlay(), 'RPlay', self)
        RPlay.triggered.connect(self.ViewerWidget2D.playForward)
        self.bottomToolBar.addAction(RPlay)
        
        RAdvance = QtWidgets.QAction(MediaAppIcons.RAdvance(), 'RAdvance', self)
        RAdvance.triggered.connect(self.ViewerWidget2D.playForward)
        self.bottomToolBar.addAction(RAdvance)
        
        Stop = QtWidgets.QAction(MediaAppIcons.Stop(), 'Stop', self)
        Stop.triggered.connect(self.ViewerWidget2D.updateFrame)
        self.bottomToolBar.addAction(Stop)
        
        Advance = QtWidgets.QAction(MediaAppIcons.Advance(), 'Advance', self)
        Advance.triggered.connect(self.ViewerWidget2D.playForward)
        self.bottomToolBar.addAction(Advance)
        
        Play = QtWidgets.QAction(MediaAppIcons.Play(), 'Play', self)
        Play.triggered.connect(self.ViewerWidget2D.playForward)
        self.bottomToolBar.addAction(Play)
        
        Next = QtWidgets.QAction(MediaAppIcons.Next(), 'Next', self)
        Next.triggered.connect(self.ViewerWidget2D.playForward)
        self.bottomToolBar.addAction(Next)
        
        self.bottomToolBar.addWidget(MediaAppKnobs.Spacer())
    
    ###Other Functions###
    def addToolBar(self, ToolBarArea, ToolBar):
        if ToolBarArea == QtCore.Qt.TopToolBarArea:
            self.topToolBars.addWidget(ToolBar)
        if ToolBarArea == QtCore.Qt.BottomToolBarArea:
            self.bottomToolBars.addWidget(ToolBar)
        if ToolBarArea == QtCore.Qt.LeftToolBarArea:
            ToolBar.setOrientation(QtCore.Qt.Vertical)
            self.leftToolBars.addWidget(ToolBar)
        if ToolBarArea == QtCore.Qt.RightToolBarArea:
            ToolBar.setOrientation(QtCore.Qt.Vertical)
            self.rightToolBars.addWidget(ToolBar)
    def removeToolBar(self, ToolBar):
        self.topToolBars.removeWidget(ToolBar)
        self.bottomToolBars.removeWidget(ToolBar)
        self.leftToolBars.removeWidget(ToolBar)
        self.rightToolBars.removeWidget(ToolBar)
        ToolBar.hide()
    #####################
        
#class ViewerWidget3D(QtWidgets.QWidget):
class ViewerWidget3D(QtOpenGL.QGLWidget):
    def __init__(self):
        super(ViewerWidget3D, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        #QtOpenGL.QGLWidget.__init__(self, parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QtCore.QPoint()

        self.trolltechGreen = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

    def xRotation(self):
        return self.xRot

    def yRotation(self):
        return self.yRot

    def zRotation(self):
        return self.zRot

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            #self.emit("xRotationChanged(int)", angle)
            #self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            #self.emit("yRotationChanged(int)", angle)
            #self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            #self.emit("zRotationChanged(int)", angle)
            #self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()

    def initializeGL(self):
        self.qglClearColor(self.trolltechPurple.darker())
        self.object = self.makeObject()
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -10.0)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport(int((width - side) / 2),int((height - side) / 2), side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-0.5, +0.5, -0.5, +0.5, 4.0, 15.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = QtCore.QPoint(event.pos())

    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)

        GL.glBegin(GL.GL_QUADS)

        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        Pi = 3.14159265358979323846
        NumSectors = 200

        for i in range(NumSectors):
            angle1 = (i * 2 * Pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * Pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)

        GL.glEnd()
        GL.glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.qglColor(self.trolltechGreen)

        GL.glVertex3d(x1, y1, +0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x3, y3, +0.05)
        GL.glVertex3d(x4, y4, +0.05)

        GL.glVertex3d(x4, y4, -0.05)
        GL.glVertex3d(x3, y3, -0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x1, y1, -0.05)

    def extrude(self, x1, y1, x2, y2):
        self.qglColor(self.trolltechGreen.darker(250 + int(100 * x1)))

        GL.glVertex3d(x1, y1, -0.05)
        GL.glVertex3d(x2, y2, -0.05)
        GL.glVertex3d(x2, y2, +0.05)
        GL.glVertex3d(x1, y1, +0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle
 
class ViewerWidget2D(AbstractGraphArea):
    ###Initialize Class###
    def __init__(self):
        super(ViewerWidget2D, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        
        self.setMouseTracking(True)
        self.modes.append('marqMode')
        self.modes.append('extraMode')
        
        #Initialize Values
        self.frameCache = AppCore.generateBlack()
        self.AccessoryToolBars = []
        
        self.TimeIndicator = DataStructures.TimeCache()
        

    ######################
    
    ###Input Events###
    #def subclassPressEvents(self, event):
    ##################
    
    ###Button Handling###
    def subclassModes(self, event):
        if hasattr(AppCore.getActiveNode(), 'ViewerEventExtra'):
            self.modes.setCurrentMode('extraMode')
    #####################
    
    ###InitalValues###        
    def subclassInitialValues(self):
        if hasattr(AppCore.getActiveNode(), 'viewerInitialValues'):
            AppCore.getActiveNode().viewerInitialValues(self)
    ##################
    
    ###ModeEvents###
    def subclassModeEvents(self, event):
        if self.getCurrentMode() == 'marqMode':
            self.marqEvent()
        else: #self.getCurrentMode() == 'extraMode':
            self.extraEvent()
   
    def marqEvent(self):
        self.endModeX = self.curModeX
        self.endModeY = self.curModeY
        self.marqContains()
    def extraEvent(self):
        self.endModeX = self.curModeX
        self.endModeY = self.curModeY
        if hasattr(AppCore.getActiveNode(), 'ViewerEventExtra'):
            AppCore.getActiveNode().ViewerEventExtra(self)
    def marqContains(self):
        #Sample Pixels here
        pass
    #################   

    ###PaintEvents###
    def subclassPaintEvent(self, pEvent, painter):
        #DrawImage
        
        #if self.frameCache is None or self.frameCacheFrame != AppCore.getCurrentFrameNumber():
        #    self.frameCache =  self.node.getImage()
        #    self.frameCacheFrame = AppCore.getCurrentFrameNumber()
        
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
        
        #Draw ActiveNode Overlays
        if hasattr(AppCore.getActiveNode(), 'ViewerOverlays'):
            AppCore.getActiveNode().ViewerOverlays(self, painter)
            
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
    #################

    ###Other Functions###
    def playForward(self):
        frameperiod=1.0/AppCore.AppAttributes['FPS']
        now = time()
        nextframe = now
        cache = self.getCache()
        for image in cache:
            while now < nextframe:
                sleep(nextframe-now)
                now = time()
                
            self.frameCache = image
            #Maybe some overhead here
            cache.moveCurrentFrameNumber(1, playback = True)
            self.repaint()
            
            nextframe += frameperiod
    def cacheFrame(self, image):
        self.frameCache = image
    
    def getInput(self):
        #FLAW: need to figure out how to play back from 2 caches at once in opengl later
        if self.inputCombiner.getValue() is 'B Only':
            return self.getLinkedNode().getInput(self.inputSelectorB.currentIndex())
        else:
            #For now just return input A, because there's no current method for connecting to two caches at once.
            return self.getLinkedNode().getInput(self.inputSelectorA.currentIndex())
    def updateFrame(self):
        inputA = self.parent().getLinkedNode().getInput(self.parent().inputSelectorA.currentIndex())
        inputB = self.parent().getLinkedNode().getInput(self.parent().inputSelectorB.currentIndex())
        
        #TODO 'implement a provided timeline in the viewer'
        if str(self.parent().inputCombiner.getValue()) == 'A Only':
            if inputA != None:
                self.cacheFrame(inputA.getImage())
        elif str(self.parent().inputCombiner.getValue()) == 'B Only':
            if imageB != None:
                self.cacheFrame(inputB.getImage())
        else:
            if inputA != None:
                imageA = inputA.getImage()
            if imageB != None:
                imageB = inputB.getImage()
        if str(self.parent().inputCombiner.getValue()) is 'Blend':    
            self.cacheFrame(self.blendImage(imageA, imageB))
        elif str(self.parent().inputCombiner.getValue()) is 'Wipe':
            self.cacheFrame(self.wipeImage(imageA, imageB))
    
    def update(self):
        self.updateFrame()
        super(ViewerWidget2D, self).update()
    def dumpAccessoryToolbars(self):
        for toolbar in self.AccessoryToolBars:
            self.removeToolBar(toolbar)
        self.AccessoryToolBars = []
    def addAccessoryToolbars(self, toolbars):
        for toolbar in toolbars:
            self.AccessoryToolBars.append(toolbar[1])
            self.addToolBar(toolbar[0], self.AccessoryToolBars[-1])
            self.AccessoryToolBars[-1].show()
    def getCache(self):
        input = self.getInput()
        if hasattr(input, 'getCache'):
            return self.getInput().getCache()
        else:
            return self.TimeIndicator
    def cacheFrames(self):
        input = self.getInput()
        if hasattr(input, 'cacheFrames'):
            self.getInput().cacheFrames()
        else:
            firstFrame, lastFrame = self.getInputRange()
            self.TimeIndicator.cacheFrames(self.generateFrames(firstFrame, lastFrame), firstFrame = firstFrame)
    
    def generateFrames(self, firstFrame, lastFrame):
        print('Viewer generating '+str(lastFrame-firstFrame)+' frames as QImages',)
        input = self.getInput()
        for frame in range(firstFrame, lastFrame):
            yield input.getImage(frame)
    
    def sizeHint(self):
        return QtCore.QSize(1920,1080)
    
    def frameForward(self):
        self.getInput().moveCurrentFrameNumber(1)
        self.update()
        self.getInput().repaint()
    def frameBackward(self):
        self.getInput().moveCurrentFrameNumber(-1)
        self.update()
        self.getInput().repaint()
    #####################
    