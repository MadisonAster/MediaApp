from PySide import QtGui, QtCore

#TODO-004: cleanup this module later, it's pretty ugly
class MainWindow(QtGui.QMainWindow):
    #settings = QtCore.QSettings('NoBS', 'GUIStuff')
    def __init__(self):
        super(MainWindow, self).__init__()
        self.NodeList = []
        self.widgetList = []
    def getPrefs(self):
        #TODO-001: call Core to get preferences, 
        #maybe we should push this instead of pulling?
        return {}
    def initUI(self):
        self.WindowFont = QtGui.QFont('Courier')
        self.WindowFont.setPixelSize(16)
        self.WindowFontMetrics = QtGui.QFontMetrics(self.WindowFont)
        
        self.AllowNestedDocks
        self.ForceTabbedDocks
        
        
        #Menu Actions#
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        restoreLayout = QtGui.QAction('Restore Layout 1', self)
        restoreLayout.setShortcut('Shift+F1')
        restoreLayout.setStatusTip('Restore Saved Layout')
        #restoreLayout.triggered.connect(self.restoreState)
        
        saveLayout = QtGui.QAction('Save Layout 1', self)
        saveLayout.setShortcut('Ctrl+F1')
        saveLayout.setStatusTip('Save Layout')
        saveLayout.triggered.connect(self.saveLayoutData)
        
        getSize = QtGui.QAction('Info Alert', self)
        getSize.setStatusTip('Get vertical size')
        getSize.triggered.connect(self.infoAlert)
        #/Menu Actions#
        
        #Menu Bar#
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        layoutMenu = menubar.addMenu('&Layout')
        layoutMenu.addAction(restoreLayout)
        layoutMenu.addAction(saveLayout)
        layoutMenu.addAction(getSize)
        #MenuBar#
        
        #ToolBar#
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        #/ToolBar#
        
        #Status Bar#
        self.statusBar()
        #/Status Bar#
        
        self.center()
        self.setWindowTitle('MediaApp')
        self.setWindowIcon(QtGui.QIcon('Toolbox.ico'))        
        self.show()
        self.resize(QtGui.QDesktopWidget().availableGeometry().width()/2, QtGui.QDesktopWidget().availableGeometry().height())
        titleBarSize = self.frameGeometry().height()-QtGui.QDesktopWidget().availableGeometry().height()
        sideBarSize = self.frameGeometry().width()-QtGui.QDesktopWidget().availableGeometry().width()/2
        self.resize(QtGui.QDesktopWidget().availableGeometry().width()/2-sideBarSize, QtGui.QDesktopWidget().availableGeometry().height()-titleBarSize)
        
        
    def allNodes(self):
        return self.NodeList
    def createNode(self, nodeName, nodeType, posX, posY):
        self.NodeList.append([nodeName, eval(nodeType+'("'+nodeName+'", '+str(posX)+', '+str(posY)+')')])
    def saveLayoutData(self, settings):
            settings.setValue("windowState", self.saveState)
    def changeTitle(self, state):
        if state == QtCore.Qt.Checked:
            self.setWindowTitle('Checkbox')
        else:
            self.setWindowTitle('')
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', 
        'Are you sure you want to quit?', QtGui.QMessageBox.Yes |
        QtGui.QMessageBox.No, QtGui.QMessageBox.No)        
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def infoAlert(self):
        cp = self.frameGeometry().width()
        ca = QtGui.QDesktopWidget().availableGeometry().height()
        ca = str(ca)
        cp = str(cp)
        titleBarSize = 47
        QtGui.QMessageBox.information(self, 'Message', cp)
    def center(self):
        qr = self.frameGeometry()
        cenX = self.frameGeometry().width()/2
        cenY = self.frameGeometry().height()/2
        #cp = QtGui.QDesktopWidget().screenGeometry().center()
        cp = QtCore.QPoint(cenX, cenY)
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def toNode(self, nodeName):
        for a in self.NodeList:
            if nodeName == a[0]:
                return a[1]