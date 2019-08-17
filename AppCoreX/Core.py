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
import os, imp
import sys, inspect
import pprint
import ctypes

from Qt import QtGui, QtCore, QtWidgets, QtCompat

class Core(dict):
    def __init__(self, argString = '', CoreRun = False):
        super(Core, self).__init__()
        sys.modules['AppCore'] = self
        #QtGui.QApplication.setColorSpec(QtGui.QApplication.ManyColor)
        
        self['CoreRun'] = CoreRun
        
        try:
            self.App = QtWidgets.QApplication([argString])
        except:
            self.App = QtGui.QApplication([argString])
        
        self.setPaths()
        
        self.AppAttributes = self.ParsePrefDicts(self['AppAttributes'])
        self.AppSettings = self.ParsePrefDicts(self['AppSettings'])
        try:
            self.AppPrefs = self.ParsePrefDicts(self['UserAppPrefs'])
        except:
            self.AppPrefs = self.ParsePrefDicts(self['AppPrefs'])
            
        self.setImpliedAppAttributes()
        self.setImpliedAppPrefs()
        self.setImpliedAppSettings()
        
        #self.AppAttributes = Values common across all apps, loaded on a per project basis, curXpos, curYpos, root settings (see nuke) etc.
        #self.AppPrefs = Settings that change on a per user basis, colors, fonts, app particulars, etc
        #self.AppSettings = Settings that change on per app basis, graph functions, widgets, font availability, preferences window etc
        
        self.App.setPalette(self.getPalette('App'))
        self.App.setStyleSheet(self.generateStyleSheet())
        
        #Nodes go here
        self.Nodes = {}
        
        #iterable temp containers go here
        self.data = {}
        self.ctypesMagic()
        
        #A sensitive node modifies it's behavior based on the active node (ie viewer paints activeNode.ViewerOverlays)
        self.SensitiveObjects = []
        self.activeNode = None
        
    def ImportPlugins(self):
        pass
        
        
    def setPaths(self):
        self['CoreDirectory'] = __file__.replace('\\','/').rsplit('/',2)[0]
        self['AppDirectory'] = self['CoreDirectory']
        self['BaseDirectories'] = [self['CoreDirectory']]
        
        for fileName in os.listdir(self['CoreDirectory']):
            if fileName.rsplit('.',1)[-1] == 'py':
                if fileName not in ['__init__.py', 'run.py', 'ExampleScript.py']:
                    self[fileName.rsplit('.',1)[0]] = self.GetOverriddenFiles(fileName)
        self['AppDataDirectory'] = os.getenv('APPDATA')+'/MediaApp/'+self['AppDirectory'].rsplit('/',1)[1]
        self['UserAppPrefs'] = self['AppDataDirectory']+'/'+'UserAppPrefs.py'
        
    def GetOverriddenFiles(self, FileName):
        PathList = [self['CoreDirectory']+'/'+FileName] #Put Core version of file first so that overridden values are given priority
        if not self['CoreRun']:
            if os.path.isfile(self['CoreDirectory'].rsplit('/',1)[0]+'/'+FileName) == True:
                if self['AppDirectory'] == self['CoreDirectory']:
                    self['AppDirectory'] = self['CoreDirectory'].rsplit('/',1)[0]
                    self['BaseDirectories'].append(self['AppDirectory'])
                PathList.append(self['CoreDirectory'].rsplit('/',1)[0]+'/'+FileName)
        return PathList
    
    def GetOverriddenPath(self, RelativePath):
        #Takes: RelativePath as path to file
        #Performs: Checks to see if file exists in wrapper application
        #Returns: Path to the wrapper app's version of the file if it exists
        RelativePath = RelativePath.replace('\\','/').strip('/')
        if os.path.isfile(self['CoreDirectory'].rsplit('/',1)[0]+'/'+RelativePath) == True:
            return self['CoreDirectory'].rsplit('/',1)[0]+'/'+RelativePath
        else:
            return self['CoreDirectory']+'/'+RelativePath
    
    def LoadUI(self, obj):
        path = inspect.getsourcefile(obj.__class__).replace('\\','/')
        relpath = path.split(self['CoreDirectory'],1)[-1].rsplit('.',1)[0]+'.ui'
        uipath = self.GetOverriddenPath(relpath)
        print('path', path)
        print('self[CoreDirectory]', self['CoreDirectory'])
        print('relpath', relpath)
        print('uipath', uipath)
        
        if os.path.exists(uipath):
            QtCompat.loadUi(uipath, baseinstance=obj)
    
    def ctypesMagic(self):
        #Windows Taskbar icon work around
        winAppID = self.AppSettings['AppID']
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(winAppID)
        
    def RegisterObject(self, objectPointer, objectString = None):
        if objectString == None:
            objectString = type(objectPointer).__name__
        exec('self.'+objectString+' = objectPointer')
        
    def ParsePrefDicts(self, FilePaths):
        DataDict = {}
        for path in FilePaths:
            module = imp.load_source('module.name', path)
            for key in module.Data.keys():
                DataDict[key] = module.Data[key]
                
        return DataDict
       
    def setImpliedAppAttributes(self):
        pass
    def setImpliedAppPrefs(self):
        self.AppPrefs['AppFontMetrics'] = QtGui.QFontMetrics(self.AppPrefs['AppFont'])
        
        globalList = []
        for key in self.AppPrefs:
            if '*' in key:
                globalList.append(key)
        self.AppPrefs['GLOBALS'] = globalList
    def setImpliedAppSettings(self):
        pass
    
    def getSensitiveObjects(self):
        return self.SensitiveObjects
    def addSensitiveObject(self, node):
        self.SensitiveObjects.append(node)
    def getActiveNode(self):
        return self.activeNode
    def setActiveNode(self, node):
        self.activeNode = node
        for object in self.getSensitiveObjects():
            object.setActiveNode(self.activeNode)

    def createNode(self, NodeClassName, parent = None, baseClass = None):
        #Takes: NodeClassName as str 
        #Performs:
        #Returns:
        import MediaAppNodes
        NodeClass = getattr(MediaAppNodes, NodeClassName)
        print('NodeClass', NodeClass)
        
        
        #evalString = 'MediaAppNodes.'+nodeClass
        #if 'Nodes' in sys.modules:
        #    import Nodes
        #    if hasattr(Nodes, nodeClass):
        #        evalString = 'Nodes.'+nodeClass
        #nodeClass = eval(evalString)
        
        if parent is None:
            parent = self
        
        #if baseClass is None:
        #    baseClass = MediaAppNodes.NodeConstructor.GraphNode
        #elif type(baseClass) is str:
        #    baseClass = eval ('MediaAppNodes.NodeConstructor.'+baseClass)
        
        #ConstructedClass = type(nodeClass.__name__, (nodeClass, baseClass, object), {})
        
        #class ConstructedClass(nodeClass, baseClass):
        #    def __init__(self, parent):
        #        super(ConstructedClass, self).__init__(parent)
                
        #node = ConstructedClass(parent)
        
        node = NodeClass(parent)
        self.Nodes[node.name()] = node
        return node
    def removeNode(self, node):
        if node in self.SensitiveObjects:
            self.SensitiveObjects.remove(node)
        del self.Nodes[node.name()]
        
    def getChildrenOf(self, parent):
        returnList = []
        for node in self.Nodes:
            if node.parent == parent:
                returnList.append(node)
        return returnList
    
    def allNodes(self):
        returnList = []
        for nodeName in self.Nodes:
            returnList.append(self.Nodes[nodeName])
        return returnList
            
    def selectedNodes(self):
        returnList = []
        for nodeName in self.Nodes:
            if self.Nodes[nodeName]['selected'].getValue() == True:
                returnList.append(self.Nodes[nodeName])
        return returnList
        
    def getNodesByName(self, searchString):
        returnList = []
        for name in self.Nodes:
            if searchString in name:
                returnList.append(name)
        return returnList
        
    def getIncrementedName(self, searchString):
        counter = 0
        existingNodes = self.getNodesByName(searchString)
        while True:
            for name in existingNodes:
                if name.replace(searchString,'') == str(counter).zfill(self.AppPrefs['NodeNamePadding']):
                    break
            else:
                break
            counter += 1
        return searchString+str(counter).zfill(self.AppPrefs['NodeNamePadding'])
       
    def saveProject(self, filePath = None):
        if filePath == None:
            filePath = self.AppAttributes['ProjectPath']
        str_AppAttributes = pprint.pformat(self.AppAttributes)
        str_Nodes = pprint.pformat(self.Nodes)
        with open(filePath,'w') as file:
            file.write('\n#AppAttributes\n')
            file.write(str_AppAttributes)
            file.write('\n#/AppAttributes\n')
            file.write('\n#Nodes\n')
            file.write(str_Nodes)
            file.write('\n#/Nodes\n')
            
    def loadProject(self, filePath = None):
        if filePath == None:
            filePath = self.AppAttributes['ProjectPath']
        with open(filePath,'r') as file:
            fileText = file.read()
        str_AppAttributes = fileText.split('\n#AppAttributes\n',1)[1].split('\n#/AppAttributes\n',1)[0]
        str_Nodes = fileText.split('\n#Nodes\n',1)[1].split('\n#/Nodes\n',1)[0]
        
        self.AppAttributes = eval(str_AppAttributes)
        self.Nodes = eval(str_Nodes)
    
    def generateBlack(self):
        return QtGui.QImage(self.AppAttributes['ResolutionWidth'], self.AppAttributes['ResolutionHeight'], QtGui.QImage.Format_ARGB32)
    
    def getPalette(self, widgetName):
        palette = QtGui.QPalette()
        
        palette.setColor(QtGui.QPalette.Window, self.AppPrefs[widgetName+'-Window'])
        palette.setColor(QtGui.QPalette.Background, self.AppPrefs[widgetName+'-Background']) #IGNORED
        palette.setColor(QtGui.QPalette.WindowText, self.AppPrefs[widgetName+'-WindowText'])
        palette.setColor(QtGui.QPalette.Foreground, self.AppPrefs[widgetName+'-Foreground']) #IGNORED
        palette.setColor(QtGui.QPalette.Base, self.AppPrefs[widgetName+'-Base'])
        palette.setColor(QtGui.QPalette.AlternateBase, self.AppPrefs[widgetName+'-AlternateBase'])
        palette.setColor(QtGui.QPalette.ToolTipBase, self.AppPrefs[widgetName+'-ToolTipBase'])
        palette.setColor(QtGui.QPalette.ToolTipText, self.AppPrefs[widgetName+'-ToolTipText'])
        palette.setColor(QtGui.QPalette.Text, self.AppPrefs[widgetName+'-Text'])
        
        palette.setColor(QtGui.QPalette.Button, self.AppPrefs[widgetName+'-Button'])
        #palette.setColor(QtGui.QPalette.ButtonText, self.AppPrefs[widgetName+'-ButtonText'])
        palette.setColor(QtGui.QPalette.BrightText, self.AppPrefs[widgetName+'-BrightText'])
        palette.setColor(QtGui.QPalette.Light, self.AppPrefs[widgetName+'-Light'])
        palette.setColor(QtGui.QPalette.Midlight, self.AppPrefs[widgetName+'-Midlight'])
        palette.setColor(QtGui.QPalette.Dark, self.AppPrefs[widgetName+'-Dark'])
        palette.setColor(QtGui.QPalette.Mid, self.AppPrefs[widgetName+'-Mid'])
        palette.setColor(QtGui.QPalette.Shadow, self.AppPrefs[widgetName+'-Shadow'])
        palette.setColor(QtGui.QPalette.Highlight, self.AppPrefs[widgetName+'-Highlight'])
        palette.setColor(QtGui.QPalette.HighlightedText, self.AppPrefs[widgetName+'-HighlightedText'])
        palette.setColor(QtGui.QPalette.Link, self.AppPrefs[widgetName+'-Link'])
        palette.setColor(QtGui.QPalette.LinkVisited, self.AppPrefs[widgetName+'-LinkVisited'])
        palette.setColor(QtGui.QPalette.NoRole, self.AppPrefs[widgetName+'-NoRole'])
        
        return palette
    def generateStyleSheet(self):
        palette = self.App.palette()
        Window = palette.window().color().name()
        WindowText = palette.windowText().color().name()
        Base = palette.base().color().name()
        AlternateBase = palette.alternateBase().color().name()
        ToolTipBase = palette.toolTipBase().color().name()
        ToolTipText = palette.toolTipText().color().name()
        Text = palette.text().color().name()
        Button = palette.button().color().name()
        ButtonText = palette.buttonText().color().name()
        BrightText = palette.brightText().color().name()
        Light = palette.light().color().name()
        Midlight = palette.midlight().color().name()
        Dark = palette.dark().color().name()
        Mid = palette.mid().color().name()
        Shadow = palette.shadow().color().name()
        Highlight = palette.highlight().color().name()
        HighlightedText = palette.highlightedText().color().name()
        Link = palette.link().color().name()
        LinkVisited = palette.linkVisited().color().name()
        
        stylesheet = 'QPushButton {background: '+Button+'; color: '+ButtonText+';}\n'
        stylesheet += 'QLineEdit {background: '+Mid+'; color: '+ButtonText+'; border: '+Shadow+';}\n'
        stylesheet += 'QComboBox {background: '+Button+'; color: '+ButtonText+'; border: '+Shadow+';}\n'
        stylesheet += 'QDockWidget {border: '+Shadow+';}\n'
        stylesheet += 'QDockWidget::title {background: '+Dark+';}\n'
        stylesheet += 'QMessageBox {background: '+Window+'; color: '+WindowText+';}\n'
        stylesheet += 'QMenuBar {background: '+Window+'; color: '+WindowText+';}\n'
        stylesheet += 'QMenuBar::item {background: '+Window+';}\n'
        stylesheet += 'QMenu {background: '+Window+'; color: '+WindowText+';}\n'
        
        stylesheet += 'QScrollBar:vertical {background: '+Window+'; border: 1px inset;}\n'
        stylesheet += 'QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: none;}\n'
        stylesheet += 'QScrollBar::handle:vertical {background: '+Button+'; margin: 24px 0 24px 0;}\n'
       
        stylesheet += 'QScrollBar:horizontal {background: '+Window+'; border: 1px inset;}\n'
        stylesheet += 'QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {background: none;}\n'
        stylesheet += 'QScrollBar::handle:horizontal {background: '+Button+'; margin: 0 24px 0 24px;}\n'
        
        stylesheet += 'QToolBar{background: '+Window+'; spacing: 3px;}\n'
        #stylesheet += "QScrollBar::add-line:vertical { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130)); height: px; subcontrol-position: bottom; subcontrol-origin: margin;}"
        
        stylesheet += 'QHeaderView::section {background: '+Button+';}'
        return stylesheet
    def getEventName(self, event):
        eventType = str(event.type())
        if not eventType.isdigit():
            return eventType.rsplit('.',1)[-1]
        else:
            enum = {
            0 : 'None',
            114 : 'ActionAdded',
            113 : 'ActionChanged',
            115 : 'ActionRemoved',
            99 : 'ActivationChange',
            121 : 'ApplicationActivate',
            122 : 'ApplicationDeactivate',
            36 : 'ApplicationFontChange',
            37 : 'ApplicationLayoutDirectionChange',
            38 : 'ApplicationPaletteChange',
            214 : 'ApplicationStateChange',
            35 : 'ApplicationWindowIconChange',
            68 : 'ChildAdded',
            69 : 'ChildPolished',
            71 : 'ChildRemoved',
            40 : 'Clipboard',
            19 : 'Close',
            200 : 'CloseSoftwareInputPanel',
            178 : 'ContentsRectChange',
            82 : 'ContextMenu',
            183 : 'CursorChange',
            52 : 'DeferredDelete',
            60 : 'DragEnter',
            62 : 'DragLeave',
            61 : 'DragMove',
            63 : 'Drop',
            170 : 'DynamicPropertyChange',
            98 : 'EnabledChange',
            10 : 'Enter',
            150 : 'EnterEditFocus',
            124 : 'EnterWhatsThisMode',
            206 : 'Expose',
            116 : 'FileOpen',
            8 : 'FocusIn',
            9 : 'FocusOut',
            23 : 'FocusAboutToChange',
            97 : 'FontChange',
            198 : 'Gesture',
            202 : 'GestureOverride',
            188 : 'GrabKeyboard',
            186 : 'GrabMouse',
            159 : 'GraphicsSceneContextMenu',
            164 : 'GraphicsSceneDragEnter',
            166 : 'GraphicsSceneDragLeave',
            165 : 'GraphicsSceneDragMove',
            167 : 'GraphicsSceneDrop',
            163 : 'GraphicsSceneHelp',
            160 : 'GraphicsSceneHoverEnter',
            162 : 'GraphicsSceneHoverLeave',
            161 : 'GraphicsSceneHoverMove',
            158 : 'GraphicsSceneMouseDoubleClick',
            155 : 'GraphicsSceneMouseMove',
            156 : 'GraphicsSceneMousePress',
            157 : 'GraphicsSceneMouseRelease',
            182 : 'GraphicsSceneMove',
            181 : 'GraphicsSceneResize',
            168 : 'GraphicsSceneWheel',
            18 : 'Hide',
            27 : 'HideToParent',
            127 : 'HoverEnter',
            128 : 'HoverLeave',
            129 : 'HoverMove',
            96 : 'IconDrag',
            101 : 'IconTextChange',
            83 : 'InputMethod',
            207 : 'InputMethodQuery',
            169 : 'KeyboardLayoutChange',
            6 : 'KeyPress',
            7 : 'KeyRelease',
            89 : 'LanguageChange',
            90 : 'LayoutDirectionChange',
            76 : 'LayoutRequest',
            11 : 'Leave',
            151 : 'LeaveEditFocus',
            125 : 'LeaveWhatsThisMode',
            88 : 'LocaleChange',
            176 : 'NonClientAreaMouseButtonDblClick',
            174 : 'NonClientAreaMouseButtonPress',
            175 : 'NonClientAreaMouseButtonRelease',
            173 : 'NonClientAreaMouseMove',
            177 : 'MacSizeChange',
            43 : 'MetaCall',
            102 : 'ModifiedChange',
            4 : 'MouseButtonDblClick',
            2 : 'MouseButtonPress',
            3 : 'MouseButtonRelease',
            5 : 'MouseMove',
            109 : 'MouseTrackingChange',
            13 : 'Move',
            197 : 'NativeGesture',
            208 : 'OrientationChange',
            12 : 'Paint',
            39 : 'PaletteChange',
            131 : 'ParentAboutToChange',
            21 : 'ParentChange',
            212 : 'PlatformPanel',
            75 : 'Polish',
            74 : 'PolishRequest',
            123 : 'QueryWhatsThis',
            106 : 'ReadOnlyChange',
            199 : 'RequestSoftwareInputPanel',
            14 : 'Resize',
            204 : 'ScrollPrepare',
            205 : 'Scroll',
            117 : 'Shortcut',
            51 : 'ShortcutOverride',
            17 : 'Show',
            26 : 'ShowToParent',
            50 : 'SockAct',
            192 : 'StateMachineSignal',
            193 : 'StateMachineWrapped',
            112 : 'StatusTip',
            100 : 'StyleChange',
            87 : 'TabletMove',
            92 : 'TabletPress',
            93 : 'TabletRelease',
            94 : 'OkRequest',
            171 : 'TabletEnterProximity',
            172 : 'TabletLeaveProximity',
            22 : 'ThreadChange',
            1 : 'Timer',
            120 : 'ToolBarChange',
            110 : 'ToolTip',
            184 : 'ToolTipChange',
            194 : 'TouchBegin',
            209 : 'TouchCancel',
            196 : 'TouchEnd',
            195 : 'TouchUpdate',
            189 : 'UngrabKeyboard',
            187 : 'UngrabMouse',
            78 : 'UpdateLater',
            77 : 'UpdateRequest',
            111 : 'WhatsThis',
            118 : 'WhatsThisClicked',
            31 : 'Wheel',
            132 : 'WinEventAct',
            24 : 'WindowActivate',
            103 : 'WindowBlocked',
            25 : 'WindowDeactivate',
            34 : 'WindowIconChange',
            105 : 'WindowStateChange',
            33 : 'WindowTitleChange',
            104 : 'WindowUnblocked',
            203 : 'WinIdChange',
            126 : 'ZOrderChange',
            }
            try:
                return enum[int(eventType)]
            except:
                return int(eventType)
                
    def getMouseButtonName(self, button):
        if not button.isdigit():
            return button.rsplit('.',1)[-1]
        else:
            enum = {
            1 : 'LeftButton',
            2 : 'RightButton',
            4 : 'MiddleButton',
            }
            try:
                return enum[int(button)]
            except:
                return int(button)
    
    def getClassPrefs(self, object):
        returnList = []
        classList = []
        for classObject in object.__class__.__mro__:
            classList.append(classObject.__name__)
        
        for key1 in self.AppPrefs.keys():
            if key1.split('-',1)[0] in classList:
                for key2 in returnList:
                    if key2.split('-',1)[1] == key1.split('-',1)[1]:
                        break
                else:
                    returnList.append(key1)
        return returnList