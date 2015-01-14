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
import copy

from PySide import QtGui, QtCore

import AppCore
import MediaAppIcons
import MediaAppKnobs
import DataStructures
from NodeLinkedWidget import *
from AbstractGraphArea import AbstractGraphArea
from DataStructures import KeyboardDict

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
        
        
class Viewer(AbstractGraphArea):
    ###Initialize Class###
    def __init__(self):
        super(Viewer, self).__init__()

        self.modes.append('marqMode')
        self.modes.append('extraMode')
        
        #Initialize Values
        self.frameCache = AppCore.generateBlack()
    ######################
    
    ###Input Events###
    def subclassPressEvents(self, event):
        if self.pressedButtons == AppCore.AppPrefs['Viewer-Shortcuts-frameBackward']:
            self.parent().getInput().moveCurrentFrame(-1)
            self.parent().updateFrame()
            self.parent().getInput().repaint()
        if self.pressedButtons == AppCore.AppPrefs['Viewer-Shortcuts-frameForward']:
            self.parent().getInput().moveCurrentFrame(1)
            self.parent().updateFrame()
            self.parent().getInput().repaint()
        if self.pressedButtons == AppCore.AppPrefs['Viewer-Shortcuts-cacheFrames']:
            self.parent().cacheFrames()
            self.parent().updateFrame()
        if self.pressedButtons == AppCore.AppPrefs['Viewer-Shortcuts-playForward']:
            self.playForward()
    ##################
    
    ###Button Handling###
    def subclassModes(self):
        if hasattr(AppCore.getActiveNode(), 'ViewerEventExtra'):
            self.modes.setCurrentMode('extraMode')
        elif self.pressedButtons == AppCore.AppPrefs['Viewer-Shortcuts-marq']:
            self.modes.setCurrentMode('marqMode')
    #####################
    
    ###InitalValues###        
    def subclassInitialValues(self):
        if hasattr(AppCore.getActiveNode(), 'viewerInitialValues'):
            AppCore.getActiveNode().viewerInitialValues(self)
    ##################
    
    ###ModeEvents###
    def subclassModeEvents(self, event):
        if self.getCurrentMode() == 'extraMode':
            self.extraEvent()
        elif self.getCurrentMode() == 'marqMode':
            self.marqEvent()
   
    def marqEvent(self):
        self.endModeX = self.curModeX
        self.endModeY = self.curModeY
        self.marqContains()
    def extraEvent(self):
        self.endModeX = self.curModeX
        self.endModeY = self.curModeY
        AppCore.getActiveNode().ViewerEventExtra(self)
    def marqContains(self):
        #Sample Pixels here
        pass
    #################   

    ###PaintEvents###
    def subclassPaintEvent(self, pEvent, painter):
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
        
        #Finished
        painter.end()
    #################

    ###Other Functions###
    def playForward(self):
        frameperiod=1.0/AppCore.AppAttributes['FPS']
        now = time()
        nextframe = now
        cache = self.parent().getCache()
        for image in cache:
            while now < nextframe:
                sleep(nextframe-now)
                now = time()
                
            self.frameCache = image
            #Maybe some overhead here
            cache.moveCurrentFrame(1, playback = True)
            self.repaint()
            
            nextframe += frameperiod
    def cacheFrame(self, image):
        self.frameCache = image
    #def setNode(self, node):
    #    self.node = node
    #####################
    
    
    
class ViewerWidget(NodeLinkedWidget, QtGui.QMainWindow):
    def __init__(self):
        super(ViewerWidget, self).__init__()
        self.setDockOptions(False)
        self.setFocusPolicy(AppCore.AppSettings['FocusPolicy'])

        self.setLinkedNode(AppCore.NodeGraph.createNode('ViewerNode'))
        self.TimeIndicator = DataStructures.TimeCache()
        
        self.widget = Viewer()
        self.setCentralWidget(self.widget)
        
        self.AccessoryToolBars = []
        self.createViewerToolbars()
        
        
    def createViewerToolbars(self):
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
        
        
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.topToolBar.addWidget(spacer)
        
        self.inputSelectorA = MediaAppKnobs.ComboKnob([])
        self.topToolBar.addWidget(self.inputSelectorA)
        
        self.inputCombiner = MediaAppKnobs.ComboKnob(['A Only','B Only','Wipe','Blend'])
        self.topToolBar.addWidget(self.inputCombiner)
        
        self.inputSelectorB = MediaAppKnobs.ComboKnob([])
        self.topToolBar.addWidget(self.inputSelectorB)
        
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.topToolBar.addWidget(spacer)
        
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.bottomToolBar.addWidget(spacer)

        RNext = QtGui.QAction(MediaAppIcons.RNext(), 'RNext', self)
        RNext.triggered.connect(self.widget.playForward)
        self.bottomToolBar.addAction(RNext)
        
        RPlay = QtGui.QAction(MediaAppIcons.RPlay(), 'RPlay', self)
        RPlay.triggered.connect(self.widget.playForward)
        self.bottomToolBar.addAction(RPlay)
        
        RAdvance = QtGui.QAction(MediaAppIcons.RAdvance(), 'RAdvance', self)
        RAdvance.triggered.connect(self.widget.playForward)
        self.bottomToolBar.addAction(RAdvance)
        
        Stop = QtGui.QAction(MediaAppIcons.Stop(), 'Stop', self)
        Stop.triggered.connect(self.updateFrame)
        self.bottomToolBar.addAction(Stop)
        
        Advance = QtGui.QAction(MediaAppIcons.Advance(), 'Advance', self)
        Advance.triggered.connect(self.widget.playForward)
        self.bottomToolBar.addAction(Advance)
        
        Play = QtGui.QAction(MediaAppIcons.Play(), 'Play', self)
        Play.triggered.connect(self.widget.playForward)
        self.bottomToolBar.addAction(Play)
        
        Next = QtGui.QAction(MediaAppIcons.Next(), 'Next', self)
        Next.triggered.connect(self.widget.playForward)
        self.bottomToolBar.addAction(Next)
        
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.bottomToolBar.addWidget(spacer)
    
    def getInput(self):
        #FLAW: need to figure out how to play back from 2 caches at once in opengl later
        if self.inputCombiner.getValue() is 'B Only':
            return self.getLinkedNode().getInput(self.inputSelectorB.currentIndex())
        else:
            #For now just return input A, because there's no current method for connecting to two caches at once.
            return self.getLinkedNode().getInput(self.inputSelectorA.currentIndex())
        
    def updateFrame(self):
        inputA = self.getLinkedNode().getInput(self.inputSelectorA.currentIndex())
        inputB = self.getLinkedNode().getInput(self.inputSelectorB.currentIndex())
        
        #TODO 'implement a provided timeline in the viewer'
        if str(self.inputCombiner.getValue()) == 'A Only':
            self.widget.cacheFrame(inputA.getImage())
        elif str(self.inputCombiner.getValue()) == 'B Only':
            self.widget.cacheFrame(inputB.getImage())
        else:
            imageA = inputA.getImage()
            imageB = inputB.getImage()
        if str(self.inputCombiner.getValue()) is 'Blend':    
            self.widget.cacheFrame(self.blendImage(imageA, imageB))
        elif str(self.inputCombiner.getValue()) is 'Wipe':
            self.widget.cacheFrame(self.wipeImage(imageA, imageB))
        
        
        #if AppCore.getCurrentFrame() in AppCore.data['frameCache']:
        #    self.frameCache = AppCore.data['frameCache'][0]
        #else:
        #    self.frameCache = AppCore.generateBlack()
        
    def dumpAccessoryToolbars(self):
        for toolbar in self.AccessoryToolBars:
            self.removeToolBar(toolbar)
        self.AccessoryToolBars = []
    def addAccessoryToolbars(self, toolbars):
        for toolbar in toolbars:
            self.AccessoryToolBars.append(toolbar[1])
            self.addToolBar(toolbar[0], self.AccessoryToolBars[-1])
            self.AccessoryToolBars[-1].show()
            
    ###Pointer Functions###
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
        print 'Viewer generating '+str(lastFrame-firstFrame)+' frames as QImages',
        input = self.getInput()
        for frame in range(firstFrame, lastFrame):
            yield input.getImage(frame)