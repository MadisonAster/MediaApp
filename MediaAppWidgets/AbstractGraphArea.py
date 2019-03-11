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
import threading
import math
from time import time
import datetime

from copy import copy

from Qt import QtGui, QtCore, QtWidgets

import AppCore
from DataStructures import KeyboardDict

#Provides unordered comparisons for a list, In this case keyboard keys,
#so that it does not matter what order you pressed the keys in
class keyList(list):
    def __init__(self, *args):
        super(keyList, self).__init__(*args)
    def __eq__(self, other):
        if not isinstance(other, list):
            return NotImplemented
                
        for item in other:
            if item not in self:
                return False
        for item in self:
            if item not in other:
                return False
        return True
        
#Provides a list with a currently selected item, .currentMode
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

#Provides comparisons for touchPoints 
class touchList(list):
    def __init__(self, *args):
        if len(args) == 1:
            if type(args[0]) is list:
                args = args[0]
        super(touchList, self).__init__(args)
    def __eq__(self, other):
        if not isinstance(other, list):
            return NotImplemented
        for TouchPoint1 in self:
            found = False
            for TouchPoint2 in other:
                if TouchPoint1.startPos() == TouchPoint2.startPos():
                    found = True
            if found is False:
                return False
        for TouchPoint1 in other:
            found = False
            for TouchPoint2 in self:
                if TouchPoint1.startPos() == TouchPoint2.startPos():
                    found = True
            if found is False:
                return False
        return True
    def __ne__(self, other):
        if not isinstance(other, list):
            return NotImplemented
        for TouchPoint1 in self:
            found = False
            for TouchPoint2 in other:
                if TouchPoint1.startPos() == TouchPoint2.startPos():
                    found = True
            if found is False:
                return True
        for TouchPoint1 in other:
            found = False
            for TouchPoint2 in self:
                if TouchPoint1.startPos() == TouchPoint2.startPos():
                    found = True
            if found is False:
                return True
        return False

class AbstractGraphArea(QtWidgets.QWidget):
    ###Initialize Class###
    def __init__(self):
        self.dropThreshhold = datetime.timedelta(1.0/24/60/60*0.02)
        self.dropRange = 30
        self.touchEventList = []
        
        super(AbstractGraphArea, self).__init__()
        self.className = self.__class__.__name__
        
        #QWidget Settings
        self.setFocusPolicy(AppCore.AppSettings['FocusPolicy'])
        self.setMinimumSize(0, 0)
        self.setGeometry(0, 0, 0, 0)
        self.setAttribute(QtCore.Qt.WA_AcceptTouchEvents)
        
        #Initialize Values
        self.modes = modeList(['None','zoom','pan'])
        self.pressedButtons = keyList()
        self.inputInterval = 0
        self.curGraphAngle = 0.0
        
        #self.addToolBarLayouts()
        self.getDictSettings()
        
        self.TabletPressure = 1.0
        
        self.TouchList = touchList()
        self.TouchMode = False
        
    def getDictSettings(self):
        self.ZoomXYJoined = AppCore.AppSettings[self.className+'-ZoomXYJoined']
        self.XPixelsPerUnit = AppCore.AppSettings[self.className+'-XPixelsPerUnit']
        self.YPixelsPerUnit = AppCore.AppSettings[self.className+'-YPixelsPerUnit']
        self.upperXZoomLimit = AppCore.AppSettings[self.className+'-upperXZoomLimit']
        self.upperYZoomLimit = AppCore.AppSettings[self.className+'-upperYZoomLimit']
        self.lowerXZoomLimit = AppCore.AppSettings[self.className+'-lowerXZoomLimit']
        self.lowerYZoomLimit = AppCore.AppSettings[self.className+'-lowerYZoomLimit']
        self.zoomSensitivity = 100.0/AppCore.AppSettings[self.className+'-zoomSensitivity']

        self.curGraphX = AppCore.AppAttributes[self.className+'-GraphX']
        self.curGraphY = AppCore.AppAttributes[self.className+'-GraphY']
        self.curGraphXS = AppCore.AppAttributes[self.className+'-GraphXS']
        self.curGraphYS = AppCore.AppAttributes[self.className+'-GraphYS']
    ######################
    
    ###Input Events###
    def keyPressEvent(self, event):
        if event.key() in KeyboardDict.keys():
            key = KeyboardDict[event.key()]
        else:
            print('key '+str(event.key())+' pressed.')
            return
        self.setButton(key)
        self.callShortcuts()
        self.subclassPressEvents(event)
    def keyReleaseEvent(self, event):    
        if event.key() in KeyboardDict.keys():
            key = KeyboardDict[event.key()]
        else:
            print('key '+str(event.key())+' released.')
            return
        self.clearButton(key)
    
    def event(self, event):
        eventType = AppCore.getEventName(event)
        if type(event) is QtGui.QTouchEvent:
            for touchEvent in self.touchEventList:
                if datetime.datetime.now()-touchEvent[0] > self.dropThreshhold:
                    del self.touchEventList[0]
                else:
                    break
            for point in event.touchPoints():
                touchEvent = [datetime.datetime.now()]
                if eventType == 'TouchBegin':
                    touchEvent.append(point.startPos().x())
                    touchEvent.append(point.startPos().y())
                else:
                    touchEvent.append(point.pos().x())
                    touchEvent.append(point.pos().y())
                self.touchEventList.append(touchEvent)
            return self.touchEvent(event)
        elif eventType in ['MouseButtonPress', 'MouseMove', 'MouseButtonRelease', 'MouseButtonDblClick']:
            for touchEvent in reversed(self.touchEventList):
                if datetime.datetime.now()-touchEvent[0] < self.dropThreshhold:
                    if math.fabs(touchEvent[1]-event.pos().x()) < self.dropRange  and math.fabs(touchEvent[2]-event.pos().y()) < self.dropRange:
                        event.accept()
                        return False
                else:
                    del self.touchEventList[0]
        return super(AbstractGraphArea, self).event(event)
    def touchEvent(self, event):
        eventType = AppCore.getEventName(event)
        event.accept()
        if eventType == 'TouchBegin':
            self.TouchMode = True
            self.initialTouchValues(event)
            self.initialValues(event, fromTouch = True)
            return True
        elif eventType == 'TouchUpdate':
            if self.TouchList != event.touchPoints():
                self.initialTouchValues(event)
                self.initialValues(event, fromTouch = True)
            self.touchMoveEvent(event)
        elif eventType == 'TouchEnd':
            self.TouchMode = False
            self.TouchList = []
        return False
        
    def tabletEvent(self, event):
        self.TabletPressure = event.pressure()
        event.ignore()
    def mousePressEvent(self, event):
        eventType = AppCore.getEventName(event)
        
        button = AppCore.getMouseButtonName(str(event.button()))
        print(eventType, event.pos().x(), event.pos().y(), button, event)
        self.setButton(button)
        self.initialValues(event)
        self.setMode(event)
        self.callShortcuts()
        self.subclassPressEvents(event)
    def mouseReleaseEvent(self, event):
        eventType = AppCore.getEventName(event)
        self.endMouseX = event.pos().x()
        self.endMouseY = event.pos().y()
        self.endModeX, self.endModeY = self.graphTrans.inverted()[0].map(self.endMouseX, self.endMouseY)
        
        button = AppCore.getMouseButtonName(str(event.button()))
        print(eventType, event.pos().x(), event.pos().y(), button, event)
        self.clearButton(button)
        self.initialValues(event)
        self.setMode(event)
    
    def callShortcuts(self):
        for pref in AppCore.getClassPrefs(self):
            if 'Shortcuts' in pref and 'Mode' not in pref:
                if self.pressedButtons == AppCore.AppPrefs[pref]:
                    getattr(self, pref.rsplit('-',1)[-1])()
        self.update()
    def subclassPressEvents(self, event): #Override me!
        pass
    ##################
    
    ###Button Handling###
    def setButton(self, button):
        self.pressedButtons.append(button)
    def clearButton(self, button):
        while button in self.pressedButtons:
            self.pressedButtons.remove(button)
            
        #self.modes.setCurrentMode('None')
        self.releaseTime = time()
        self.inputInterval = AppCore.AppPrefs['AbstractGraphArea-inputInterval']
    def clearAllButtons(self):  
        for button in self.pressedButtons:
            self.clearButton(button)
    def setMode(self, event):
        if self.inputInterval > 0:
            if time() > self.releaseTime+self.inputInterval or len(self.pressedButtons) == 0:
                self.inputInterval = 0
            else:
                return
        for pref in AppCore.getClassPrefs(self):
            if 'Shortcuts' in pref and type(AppCore.AppPrefs[pref]) == list:
                if self.pressedButtons == AppCore.AppPrefs[pref]:
                    self.modes.setCurrentMode(pref.rsplit('-',1)[-1])
                    if pref.split('-',1)[0] != 'AbstractGraphArea':
                        self.subclassModes(event)
                    break
        else:
            self.modes.setCurrentMode('None')
            self.subclassModes(event)
        self.update()
        
    def subclassModes(self, event): #Override me!
        pass
    def getCurrentMode(self):
        return self.modes.getCurrentMode()
    #####################
    
    ###InitalValues###
    def initialTouchValues(self, event):
        self.TouchList = touchList(event.touchPoints())
        
        self.startTouchX = []
        self.startTouchY = []
        eventType = AppCore.getEventName(event)
        for point in event.touchPoints():
            if eventType == 'TouchBegin':
                x = point.startPos().x()
                y = point.startPos().y()
            else:
                x = point.pos().x()
                y = point.pos().y()
            self.startTouchX.append(x)
            self.startTouchY.append(y)
            
        avgStartModeX, avgStartModeY = 0, 0
        for x, y in zip(self.startTouchX, self.startTouchY):
            mx, my = self.graphTrans.inverted()[0].map(x, y)
            avgStartModeX += mx
            avgStartModeY += my
        self.startTouchModeX = avgStartModeX/len(self.startTouchX)
        self.startTouchModeY = avgStartModeY/len(self.startTouchY)
        
        #Calculate Center
        sumX = 0
        sumY = 0
        for x, y in zip(self.startTouchX, self.startTouchY):
            sumX += x
            sumY += y
        self.startTouchCenterX = float(sumX)/len(self.startTouchX)
        self.startTouchCenterY = float(sumY)/len(self.startTouchY)
        
        #Calculate distance and angle of each point relative to center
        self.startTouchDistanceX = []
        self.startTouchDistanceY = []
        self.startTouchDistance = []
        self.startTouchAngle = []
        for x, y in zip(self.startTouchX, self.startTouchY):
            dx = float(x)-float(self.startTouchCenterX)
            dy = float(y)-float(self.startTouchCenterY)
            self.startTouchDistanceX.append(math.fabs(dx))
            self.startTouchDistanceY.append(math.fabs(dy))
            self.startTouchDistance.append(math.sqrt(dx**2+dy**2)/math.sqrt(2))
            self.startTouchAngle.append(self.angleFromPoint(dx,dy))
        self.startGraphAngle = self.curGraphAngle
    def initialValues(self, event, fromTouch = False):
        if self.TouchMode is not True or fromTouch is True:
            AppCore.AppAttributes[self.className+'-GraphX'] = self.curGraphX
            AppCore.AppAttributes[self.className+'-GraphY'] = self.curGraphY
            AppCore.AppAttributes[self.className+'-GraphXS'] = self.curGraphXS
            AppCore.AppAttributes[self.className+'-GraphYS'] = self.curGraphYS
            AppCore.AppAttributes[self.className+'-GraphAngle'] = self.curGraphAngle
            
            self.startMouseX = event.pos().x()
            self.startMouseY = event.pos().y()
            self.startModeX, self.startModeY = self.graphTrans.inverted()[0].map(self.startMouseX, self.startMouseY)
            self.startModeX /= self.XPixelsPerUnit
            self.startModeY /= self.YPixelsPerUnit
        if self.TouchMode is not True:
            self.endModeX = self.startModeX
            self.endModeY = self.startModeY
        self.subclassInitialValues()
    def subclassInitialValues(self): #Override me!
        pass
    ##################

    ###MoveEvents###
    def mouseMoveEvent(self, event):
        #print len(self.touchEventList)
        #print event.type().name, event.pos().x(), event.pos().y(), event
        self.progressValues(event)
        if self.inputInterval > 0:
            if time() > self.releaseTime+self.inputInterval:
                self.inputInterval = 0
                self.initialValues(event)
                print('move setmode')
                self.setMode(event)
            else:
                return
                
        self.ModeEvents(event)
        self.update() #Redraw  
        self.repaint()
    def touchMoveEvent(self, event):
        #print 'touch'
        self.progressTouchValues(event)
        self.TouchModeEvents(event)
        self.update() #Redraw  
        self.repaint()
    ################
    
    ###ProgressValues###
    def progressValues(self, event):
        self.curMouseX = event.pos().x()
        self.curMouseY = event.pos().y()
        self.curModeX, self.curModeY = self.graphTrans.inverted()[0].map(self.curMouseX, self.curMouseY)
        self.curModeX /= self.XPixelsPerUnit
        self.curModeY /= self.YPixelsPerUnit
        self.subclassProgressValues(event)
    def subclassProgressValues(self, event): #Override me!
        pass
    def progressTouchValues(self, event):
        self.curTouchX = []
        self.curTouchY = []
        for point in event.touchPoints():
            self.curTouchX.append(point.pos().x())
            self.curTouchY.append(point.pos().y())
            
        #Calculate Center
        sumX = 0
        sumY = 0
        for x, y in zip(self.curTouchX, self.curTouchY):
            sumX += x
            sumY += y
        self.curTouchCenterX = float(sumX)/len(self.curTouchX)
        self.curTouchCenterY = float(sumY)/len(self.curTouchY)
        
        #Calculate distance and angle of each point relative to center
        self.curTouchDistanceX = []
        self.curTouchDistanceY = []
        self.curTouchAngle = []
        for x, y in zip(self.curTouchX, self.curTouchY):
            dx = float(x)-float(self.curTouchCenterX)
            dy = float(y)-float(self.curTouchCenterY)
            self.curTouchDistanceX.append(math.fabs(dx))
            self.curTouchDistanceY.append(math.fabs(dy))
            self.curTouchAngle.append(self.angleFromPoint(dx,dy))
            
        #Calculate change in angle    
        angleDelta = 0.0
        for ca, sa in zip(self.curTouchAngle, self.startTouchAngle):
            angleDelta += sa - ca
        angleDelta = angleDelta/len(self.startTouchAngle)
        self.curGraphAngle = self.startGraphAngle-angleDelta
        
        self.subclassProgressTouchValues(event)
    def subclassProgressTouchValues(self, event): #Override me!
        pass
    ####################
    
    ###ModeEvents###
    def ModeEvents(self, event):
        if self.getCurrentMode() == 'zoom':
            self.zoom()
        elif self.getCurrentMode() == 'pan':
            self.pan()
        else:
            self.subclassModeEvents(event)
    def TouchModeEvents(self, event):
        if self.TouchMode is True:
            self.touchModeEvent()
        self.subclassTouchModeEvents(event)
    def subclassModeEvents(self, event): #Override me!
        pass
    def subclassTouchModeEvents(self, event): #Override me!
        pass
        
    def pan(self):
        self.curGraphX = AppCore.AppAttributes[self.className+'-GraphX']+(self.curMouseX-self.startMouseX)
        self.curGraphY = AppCore.AppAttributes[self.className+'-GraphY']+(self.curMouseY-self.startMouseY)
    def zoom(self):
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
        ##### Repeated below
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
    def touchModeEvent(self):
        posDeltaX = (self.curTouchCenterX-self.startTouchCenterX)
        posDeltaY = (self.curTouchCenterY-self.startTouchCenterY)
        
        #Scaling math
        if len(self.TouchList) > 1:
            scaleDeltaX = 0
            scaleDeltaY = 0
            for cx, sx in zip(self.curTouchDistanceX, self.startTouchDistance):
                if sx != 0:
                    scaleDeltaX += cx/sx
            for cy, sy in zip(self.curTouchDistanceY, self.startTouchDistance):
                if sy != 0:
                    scaleDeltaY += cy/sy
            scaleDeltaX = scaleDeltaX/len(self.startTouchDistanceX)
            scaleDeltaY = scaleDeltaY/len(self.startTouchDistanceY)
            
            if self.ZoomXYJoined == True:
                self.curGraphXS = (AppCore.AppAttributes[self.className+'-GraphXS']+1)*(math.sqrt(scaleDeltaX**2+scaleDeltaY**2)/math.sqrt(2))-1
                self.curGraphYS = (AppCore.AppAttributes[self.className+'-GraphYS']+1)*(math.sqrt(scaleDeltaX**2+scaleDeltaY**2)/math.sqrt(2))-1
            else:
                self.curGraphXS = AppCore.AppAttributes[self.className+'-GraphXS']*scaleDeltaX
                self.curGraphYS = AppCore.AppAttributes[self.className+'-GraphYS']*scaleDeltaY
        
        #Panning math
        self.curGraphX = AppCore.AppAttributes[self.className+'-GraphX']+posDeltaX
        self.curGraphY = AppCore.AppAttributes[self.className+'-GraphY']+posDeltaY
        
        #Scaling offset math
        if len(self.TouchList) > 1:
            difScaleX = self.curGraphXS-AppCore.AppAttributes[self.className+'-GraphXS']
            difScaleY = self.curGraphYS-AppCore.AppAttributes[self.className+'-GraphYS']
        
            if self.curGraphXS > self.upperXZoomLimit:
                self.curGraphXS = self.upperXZoomLimit
            elif self.curGraphXS < self.lowerXZoomLimit:
                self.curGraphXS = self.lowerXZoomLimit
            else:
                self.curGraphX = self.curGraphX-(self.startTouchModeX*difScaleX)
                
            if self.curGraphYS > self.upperYZoomLimit:
                self.curGraphYS = self.upperYZoomLimit  
            elif self.curGraphYS < self.lowerYZoomLimit:
                self.curGraphYS = self.lowerYZoomLimit
            else:
                self.curGraphY = self.curGraphY-(self.startTouchModeY*difScaleY)
    #################
    
    ###PaintEvents###
    def paintEvent(self, pEvent):
        painter = QtGui.QPainter(self)
        
        #DrawBG
        self.widgetSize = self.size()
        painter.setBrush(AppCore.AppPrefs[self.className+'-bgColor'])
        painter.drawRect(0, 0, self.widgetSize.width(), self.widgetSize.height())
        
        #SetTransform
        self.graphTrans = QtGui.QTransform()
        self.graphTrans.translate(self.curGraphX, self.curGraphY)
        #print self.curGraphXS+1, self.curGraphYS+1
        self.graphTrans.scale(self.curGraphXS+1, self.curGraphYS+1)
        painter.setTransform(self.graphTrans)
        
        self.visibleLeft, self.visibleTop = self.graphTrans.inverted()[0].map(0, 0)
        self.visibleRight, self.visibleBottom = self.graphTrans.inverted()[0].map(self.widgetSize.width(), self.widgetSize.height())
        
        self.subclassPaintEvent(pEvent, painter)
        
        #Finished
        painter.end()
    def subclassPaintEvent(self, pEvent, painter): #Override me!
        pass
    #################

    ###Math Functions###
    def angleFromPoint(self,x,y):
        if x != 0.0:
            slope = y/x
        else:
            slope = 0
        angle = math.degrees(math.atan(slope))
        if x > 0 and y >= 0:
            angle += 270.0
        elif x >= 0 and y < 0:
            angle = 270.0-angle
        elif x < 0 and y <= 0:
            angle += 90.0
        elif x <= 0 and y > 0:
            angle = 90.0-angle
        return angle
    ####################
    

    pass