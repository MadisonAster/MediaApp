from PySide import QtGui, QtCore

from KnobTypes import *

class NodeConstructor(dict):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(NodeConstructor, self).__init__()
        ################################

        self['xpos'] = IntKnob(Core.AppAttributes['GraphXPos'])
        self['ypos'] = IntKnob(Core.AppAttributes['GraphYPos'])
        
        self.nodeShape()
        
    def name(self):
        return self['nodeName']
    def toKnob(self, a):
        return self[a]
    def drawNode(self, widget, painter):
        X = self['xpos'].value()
        Y = self['ypos'].value()
        widgetSize = widget.size()

        self.nodeGradient.setStart(self.nodeGradientStart.x()+X, self.nodeGradientStart.y()+Y)
        self.nodeGradient.setFinalStop(self.nodeGradientStop.x()+X, self.nodeGradientStop.y()+Y)
        
        painter.setBrush(QtGui.QBrush(self.nodeGradient))
        painter.drawConvexPolygon(self.polyShapeQT.translated(X,Y))
        
        #self.textTransform.translate(widgetSize.width()/2,widgetSize.height()/2)
        painter.setTransform(self.textTransform,True)
        painter.drawText(self.textRectangle.translated(X,Y),QtCore.Qt.AlignCenter,self.displayText)
    def nodeShape(self):
        self.polyShape = [[0,0],[70,0],[74,8],[70,16],[0,16]]
        #colorTable = 0xCC6666
        self.polyLowX, self.polyLowY = 0, 0
        self.polyHighX, self.polyHighY = 0, 0
        for a in self.polyShape:
            if a[0] > self.polyHighX:
                self.polyHighX = a[0]
            if a[1] > self.polyHighY:
                self.polyHighY = a[1]
            if a[0] < self.polyLowX:
                self.polyLowX = a[0]
            if a[1] < self.polyLowY:
                self.polyLowY = a[1]
        self.polyMidX = (self.polyHighX-self.polyLowX)/2
        self.polyMidY = (self.polyHighY-self.polyLowY)/2
        
        for a in self.polyShape:
            a[0] -= self.polyMidX
            a[1] -= self.polyMidY
        
        self.polyShapeQT = []
        for a in self.polyShape:
            self.polyShapeQT.append(QtCore.QPointF(a[0],a[1]))
        self.polyShapeQT = QtGui.QPolygonF(self.polyShapeQT)

        self.nodeRectangle = QtCore.QRectF(self.polyLowX-self.polyMidX, self.polyLowY-self.polyMidY, self.polyHighX, self.polyHighY)
        self.nodeRectangleI = QtCore.QRect(self.polyLowX-self.polyMidX, self.polyLowY-self.polyMidY, self.polyHighX, self.polyHighY)
        self.nodeGradientStart = QtCore.QPointF(self.polyMidX, self.polyLowY-self.polyMidY)
        self.nodeGradientStop = QtCore.QPointF(self.polyMidX, self.polyHighY-self.polyMidY)
        self.nodeGradient = QtGui.QLinearGradient(self.nodeGradientStart, self.nodeGradientStop)
        self.nodeGradient.setSpread(QtGui.QGradient.RepeatSpread)
        self.nodeGradient.setColorAt(0, QtGui.QColor(238,238,238))
        self.nodeGradient.setColorAt(1, QtGui.QColor(122,122,122))


        self.displayText = self.name().value()
        
        
        self.textRectangle = Core.AppPrefs['AppFontMetrics'].boundingRect(self.nodeRectangleI, QtCore.Qt.AlignCenter, self.displayText)
        #self.textRectangle = QtGui.QPainter.boundingRect(self.nodeRectangle, QtCore.Qt.AlignCenter, self.displayText)
        testTextW = self.nodeRectangle.width()/self.textRectangle.width()
        testTextH = self.nodeRectangle.height()/self.textRectangle.height()
        self.textScale = 1
        if testTextW < 1 or testTextH < 1:
            self.textScale = testTextW
            if testTextH < testTextW:
                self.textScale = testTextH
        
        self.textTransform = QtGui.QTransform()
        #self.textTransform.translate(self.curGraphX, self.curGraphY)
        self.textTransform.scale(self.textScale, self.textScale)
        #painter.setTransform(self.textTransform)
        
        #self.textSize = 0
        #for a in self.displayText:
        #    self.textSize += robo.letterSize(a)
        #self.displayText = str(int(self.textSize))+self.displayText
        #self.textSize = 8*(1/(self.textSize/1430))
        #if self.textSize > 8:
        #    self.textSize = 8
        #print(str(self.textSize)+self.displayText)
        #self.textSize = 8
        
    def updateShape(self):
        pass