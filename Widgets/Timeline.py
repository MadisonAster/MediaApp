from PySide import QtGui, QtCore
class Timeline(QtGui.QDockWidget):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        super(Timeline, self).__init__()
        ################################
        
        self.initUI()
        
        self.middleClick = False
        self.leftClick = False
        self.rightClick = False
        self.clickEventRestart = True
        self.panMode = False
        self.zoomMode = False
        self.marqMode = False
        self.curGraphX = 0
        self.curGraphY = 0
        self.curGraphS = 0
        
        self.startMarqX = 0
        self.startMarqY = 0
        self.endMarqX = 0
        self.endMarqY = 0
        
        #UserSettings#
        self.zoomSensitivity = 2
        self.upperZoomLimit = 10
        self.lowerZoomLimit = -1
        self.panJumpLimit = 20
    def initUI(self):
        widgetSize = self.size()
        self.setMinimumSize(0, 0)
        self.setGeometry(0, 0, 0, 0)
        self.setMouseTracking(True)
    def mousePressEvent(self, a):
        self.startMouseX = a.pos().x()
        self.startMouseY = a.pos().y()
        b = str(a.button())
        if b.rsplit('.', 1)[1] == 'MiddleButton' or b.rsplit('.', 1)[1] == 'MidButton':
            self.middleClick = True
        elif b.rsplit('.', 1)[1] == 'LeftButton':
            self.leftClick = True
        elif b.rsplit('.', 1)[1] == 'RightButton':
            self.rightClick = True
        #QtGui.QMessageBox.information(self, 'Message', c)
    def mouseReleaseEvent(self, a):
        b = str(a.button())
        if b.rsplit('.', 1)[1] == 'MiddleButton' or b.rsplit('.', 1)[1] == 'MidButton':
            self.middleClick = False
        elif b.rsplit('.', 1)[1] == 'LeftButton':
            self.leftClick = False
        elif b.rsplit('.', 1)[1] == 'RightButton':
            self.rightClick = False
        self.clickEventRestart = True
        self.marqMode = False
        self.update()
    def mouseMoveEvent(self, a):
        widgetSize = self.size()
        self.curMouseX = a.pos().x()
        self.curMouseY = a.pos().y()
        if self.clickEventRestart == True:
            self.clickEventRestart = False
            self.startGraphS = self.curGraphS
            self.startMouseX, self.startMouseY = self.curMouseX, self.curMouseY
            self.startGraphX, self.startGraphY = self.curGraphX, self.curGraphY
            self.widgetSizeX, self.widgetSizeY = widgetSize.width(), widgetSize.height()
            if self.startGraphS > -1:
                self.startGrabX = (self.startMouseX-self.startGraphX)/(self.startGraphS+1)
                self.startGrabY = (self.startMouseY-self.startGraphY)/(self.startGraphS+1)
            else:
                self.startGrabX, self.startGrabY = 0, 0
        if self.middleClick == True and self.leftClick == False:
            self.panMode = True
            if self.zoomMode == True or self.marqMode == True:
                self.zoomMode, self.marqMode = False, False
                self.clickEventRestart = True
            else:
                if self.curGraphS > -1:
                    newGraphX = self.startGraphX+(self.curMouseX-self.startMouseX)   
                    newGraphY = self.startGraphY+(self.curMouseY-self.startMouseY)
                    panJumpSize = self.panJumpLimit*(self.curGraphS+1)
                    if newGraphX > self.curGraphX+panJumpSize or newGraphX < self.curGraphX-panJumpSize:
                        self.clickEventRestart = True
                    elif newGraphY > self.curGraphY+panJumpSize or newGraphY < self.curGraphY-panJumpSize:
                        self.clickEventRestart = True
                    else:
                        self.curGraphX = newGraphX
                        self.curGraphY = newGraphY
                        self.update()
        elif self.middleClick == True and self.leftClick == True:
            self.zoomMode = True
            if self.panMode == True or self.marqMode == True:
                self.panMode, self.marqMode = False, False
                self.clickEventRestart = True
            else:
                scaleX = (self.curMouseX-self.startMouseX)/100
                scaleY = ((self.curMouseY-self.startMouseY)/100)*-1
                self.curGraphS = self.startGraphS+(scaleX+scaleY)/2*self.zoomSensitivity
                if self.curGraphS < self.lowerZoomLimit:
                    self.curGraphS = self.lowerZoomLimit
                if self.curGraphS > self.upperZoomLimit:
                    self.curGraphS = self.upperZoomLimit
                difScale = (self.curGraphS)-(self.startGraphS)
                self.curGraphX = self.startGraphX-(self.startGrabX*difScale)
                self.curGraphY = self.startGraphY-(self.startGrabY*difScale)
                self.update()
        elif self.middleClick == False and self.leftClick == True:
            self.marqMode = True
            if self.panMode == True or self.zoomMode == True:
                self.panMode, self.zoomMode = False, False
                self.clickEventRestart = True
            else:
                self.startMarqX = self.startMouseX
                self.startMarqY = self.startMouseY
                self.endMarqX = self.curMouseX
                self.endMarqY = self.curMouseY
                self.update()
        else:
            self.clickEventRestart = True 
            
            #QtGui.QMessageBox.information(self, 'Message', str(gridCenterX))
            #QtGui.QMessageBox.information(self, 'Message', str(gridCenterY))
            
    def paintEvent(self, a):
        widgetSize = self.size()
        
        painter = QtGui.QPainter(self)
        
        #BG
        painter.setBrush(QtGui.QColor(50,50,50))
        painter.setPen(QtGui.QColor(100,100,100))
        painter.drawRect(0, 0, widgetSize.width(), widgetSize.height())
        #/BG
        
        graphTrans = QtGui.QTransform()
        graphTrans.translate(self.curGraphX, self.curGraphY)
        graphTrans.scale(self.curGraphS+1, self.curGraphS+1)
        painter.setTransform(graphTrans)

        
        painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0), .5))
        painter.setFont(Core.AppPrefs['AppFont'])
        for nodeName in Core.Nodes:
            Core.Nodes[nodeName].drawNode(self, painter)
            painter.setTransform(graphTrans)
            
        if self.marqMode == True:
            marqX = [self.startMarqX, self.endMarqX]
            marqY = [self.startMarqY, self.endMarqY]
            marqX.sort()
            marqY.sort()
            painter.setBrush(QtGui.QColor(255,255,255,25))
            painter.setPen(QtGui.QPen(QtGui.QColor(204,204,204), 2))
            painter.drawRect(marqX[0], marqY[0], marqX[1]-marqX[0], marqY[1]-marqY[0]) 
        painter.end()