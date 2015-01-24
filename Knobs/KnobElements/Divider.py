from PySide import QtGui, QtCore

class Divider(QtGui.QWidget):
    def __init__(self, vertical = False, horizontal = False):
        super(Divider, self).__init__()
        
        if vertical == True:
            self.width = 1
            verticalPolicy = QtGui.QSizePolicy.Expanding
        else:
            self.width = 0
            verticalPolicy = QtGui.QSizePolicy.Fixed
        if horizontal == True:
            self.height = 1
            horizontalPolicy = QtGui.QSizePolicy.Expanding
        else:
            self.height = 0
            horizontalPolicy = QtGui.QSizePolicy.Fixed
        self.setSizePolicy(horizontalPolicy, verticalPolicy)
            
            
        self.color = QtGui.QColor(0,0,0,1)
        #self.setPalette(QtGui.QPalette(self.color))
        #self.setAutoFillBackground(True)
    def sizeHint(self):
        return QtCore.QSize(self.width,self.height)
    def setWidth(self, value):
        self.width = value
    def setHeight(self, value):    
        self.height = value
    def setColor(self, QColor):
        self.color = QColor
        self.setPalette(QtGui.QPalette(self.color, QtGui.QBrush(self.color)))
    def paintEvent(self, pEvent):
        painter = QtGui.QPainter(self)
        
        #DrawBG
        self.widgetSize = self.size()
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(0, 0, self.widgetSize.width(), self.widgetSize.height())   
    
