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
import math

from KnobTypes import *


class PropertiesWidget(QtGui.QWidget):
    def __init__(self):
        #global Core
        #Core = CorePointer
        super(PropertiesWidget, self).__init__()
        #self.setAccessibleName('PropertiesWidget')   #override visible name here or elsewhere
        ##################################
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        #QtGui.QSizePolicy.MinimumExpanding
        #self.setMaximumSize(200,200)
        
        self.panelLayout = QtGui.QVBoxLayout()
        self.setLayout(self.panelLayout)
        
        
        
        #cb1 = QtGui.QPushButton("One",self)
        #cb2 = QtGui.QPushButton("Two",self)
        #self.panelLayout.addWidget(cb1)
        #self.panelLayout.addWidget(cb2)
        
        
    def addKnob(widget):
        self.panelLayout.addWidget(widget)
    def sizeHint(self):
        return QtCore.QSize(100,400)
    

class PropertiesDockWidget(QtGui.QDockWidget):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(PropertiesDockWidget, self).__init__()
        ##################################
        self.setWidget(PropertiesWidget())
        
        #self.visibilityChanged.triggered.connect(self.unDock)
        self.toggleViewAction().triggered.connect(self.unDock)
    def unDock(self):
        #TODO get this signal working
        print 'yay'
        Core.PropertiesBin.removeDockWidget(self)
        
class NodeConstructor(object):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(NodeConstructor, self).__init__(CorePointer)
        ################################
        
        self.knobs = []
        
        self['xpos'] = IntKnob(Core.AppAttributes['GraphXPos'])
        self['ypos'] = IntKnob(Core.AppAttributes['GraphYPos'])
        self['selected'] = BoolKnob(False)
        
        self['ClassName'] = StrKnob('Clip')
        self['nodeName'] = StrKnob('Node000')
        
        self.shapeTransform = QtGui.QTransform()
        self.nodeShape()
        self.mapNodeShape()
        
        #self.properties = PropertiesWidget(Core)
    
    def __len__(self):
        return len(self.knobs)
    def __getitem__(self, key):
        for knob in self.knobs:
            if knob.name == key:
                return knob
        else:
            return None
    def __delitem__(self, key):
        for i, knob in enumerate(self.knobs):
            if knob.name == key:
                del self.knobs[i]
    def __setitem__(self, key, value):
        if self[key] != None:
            del self[key]
        value.name = key    
        self.knobs.append(value)
    def __iter__(self):
        for knob in self.knobs:
            yield knob
    def __reversed__(self):
        return reversed(self.knobs)
        
        
    def name(self):
        return self['nodeName'].getValue()
    def toKnob(self, a):
        return self[a]

    def nodeShape(self):
        #Override Me!
        self.polyShape = [[0,0],[70,0],[74,8],[70,16],[0,16]]
        self.color1 = QtGui.QColor(238,238,238)
        self.color2 = QtGui.QColor(122,122,122)
        
    def mapNodeShape(self):
        #Center Shape, create rectangle, midpoint
        self.coordList, self.rectLowHigh, self.rectMidPoint = self.coordListCentered(self.polyShape)
        
        #Convert Shape and Rectangle
        self.polyShape = self.coordListConvert(self.coordList)
        self.nodeRectangle = self.rectConvert(self.rectLowHigh)
        self.nodeRectangleI = self.nodeRectangle.toRect()
        
        #Create selectShape
        selectShapeTrans = QtGui.QTransform.fromScale((self.nodeRectangle.width()-3)/self.nodeRectangle.width(), (self.nodeRectangle.height()-3)/self.nodeRectangle.height())
        self.selectShape = selectShapeTrans.map(self.polyShape).translated(1.5,1.5)
        
        #colorTable = 0xCC6666
        self.nodeGradientStart = QtCore.QPointF(0, self.rectLowHigh[0][1])
        self.nodeGradientStop = QtCore.QPointF(0, self.rectLowHigh[1][1])
        self.nodeGradient = QtGui.QLinearGradient(self.nodeGradientStart, self.nodeGradientStop)
        self.nodeGradient.setSpread(QtGui.QGradient.RepeatSpread)
        self.nodeGradient.setColorAt(0, self.color1)
        self.nodeGradient.setColorAt(1, self.color2)
        self.gradientBrush = QtGui.QBrush(self.nodeGradient)
        
        
        Metrics = Core.AppPrefs['AppFontMetrics']
        textHeight = Metrics.boundingRect(self.nodeRectangle.toRect(), QtCore.Qt.TextWrapAnywhere, self['nodeName'].getValue()).height()
        textLines = math.ceil(textHeight/float(Metrics.lineSpacing()))
        stretchHeight = textLines*(Metrics.lineSpacing()/self.nodeRectangle.height())

        self.shapeTransform.scale(1,stretchHeight)
        self.scaledPolyShape = self.shapeTransform.map(self.polyShape)
        
        self.getPos()   
    def getPos(self):
        X = self['xpos'].getValue()
        Y = self['ypos'].getValue()
        
        self.mappedPolyShape = self.scaledPolyShape.translated(X,Y)
        self.mappedSelectShape = self.shapeTransform.map(self.selectShape).translated(X,Y)
        self.mappedNodeRect = self.shapeTransform.mapRect(self.nodeRectangle).translated(X,Y)

        nodeRectX = self.shapeTransform.mapRect(self.nodeRectangle).x()
        nodeRectY = self.shapeTransform.mapRect(self.nodeRectangle).y()
        nodeRectH = self.shapeTransform.mapRect(self.nodeRectangle).height()
        self.nodeGradient.setStart(nodeRectX+X,nodeRectY+Y)
        
        
        self.nodeGradient.setFinalStop(nodeRectX+X,nodeRectH-nodeRectY+Y)
        self.gradientBrush = QtGui.QBrush(self.nodeGradient)
        
    def coordListRect(self, coordList):
        #Takes: coordList = [[0,0],[70,0],[74,8]]
        #Returns: rectLowHigh = [[0,0],[74,8]]
        dimensions = len(coordList[0])
        lowValues = []
        highValues = []
        for a in range(dimensions):
            lowValues.append(None)
            highValues.append(None)
            for b in coordList:
                if lowValues[a] == None or b[a] < lowValues[a]:
                    lowValues[a] = b[a]
                if highValues[a] == None or b[a] > highValues[a]:
                    highValues[a] = b[a]
        return [lowValues, highValues]    
    def coordListConvert(self, coordList):
        #Takes: coordList = [[0,0],[70,0],[74,8]]
        #Returns: QPolyGonF()
        polyShapeQT = []
        for a in coordList:
            polyShapeQT.append(QtCore.QPointF(a[0],a[1]))
        return QtGui.QPolygonF(polyShapeQT)
    def coordListCentered(self, coordList, rectLowHigh = None):
        #coordList Takes: coordList = [[0,0],[70,0],[74,8]]
        #rectLowHigh Takes: rectLowHigh = [[0,0],[74,8]]
        #    only necessary to manually offset the midpoint
        #Returns: coordList in coordList format, centered around 0 in each dimension
        if rectLowHigh == None:
            rectLowHigh = self.coordListRect(coordList)
        dimensions = len(coordList[0])
        rectMidPoint = []
        for a in range(dimensions):
            for b in range(len(coordList)):
                #move shape so that top, and left boundaries of rect = 0
                coordList[b][a] -= rectLowHigh[0][a]
                rectLowHigh[0][a] -= rectLowHigh[0][a]
                rectLowHigh[1][a] -= rectLowHigh[0][a]
            rectMidPoint.append((rectLowHigh[1][a]-rectLowHigh[0][a])/2)
        return coordList, rectLowHigh, rectMidPoint    
    def rectConvert(self, rectLowHigh):
        #Takes: rectLowHigh = [[0,0],[74,16]]
        #Returns: QRectF(lowX, highY, width, height)
        lowX = rectLowHigh[0][0]
        lowY = rectLowHigh[0][1]
        width = rectLowHigh[1][0]-rectLowHigh[0][0]
        height = rectLowHigh[1][1]-rectLowHigh[0][1]
        return QtCore.QRectF(lowX, lowY, width, height)
    def fallsAround(self, X, Y):
        return self.mappedNodeRect.contains(X,Y)
    
    def drawNode(self, painter):   
        painter.setBrush(self.gradientBrush)
        painter.drawConvexPolygon(self.mappedPolyShape)
        if self.toKnob('selected').getValue() == True:  
            painter.setBrush(Core.AppPrefs['GraphWidget-nodeSelectColor'])
            painter.setPen(Core.AppPrefs['GraphWidget-nodeSelectPen'])
            painter.drawConvexPolygon(self.mappedSelectShape)
        painter.drawText(self.mappedNodeRect,QtCore.Qt.TextWrapAnywhere,self['nodeName'].getValue())
    
    def setName(self, value):
        self['nodeName'] = StrKnob(value)
        self.setObjectName(value)
        self.setWindowTitle(value)
    def attachKnobs(self):
        #for widget in self.widget().panelLayout.findChildren(object):
        #    self.widget().panelLayout.removeWidget(widget)
        for knob in self:
            if knob not in self.widget().panelLayout.findChildren(object):
                #self.widget().panelLayout.addWidget(knob.name)
                #self.widget().panelLayout.addWidget(knob)
                self.widget().panelLayout.addLayout(knobLayout)
       
class Node(NodeConstructor, PropertiesDockWidget):
    def __init__(self, CorePointer):
        super(Node, self).__init__(CorePointer)   
        
        #widgetName = widget.accessibleName()
        #widgetName = widget['nodeName'].getValue()
        #if widgetName == '':
        #    widgetName = type(widget).__name__
        
        