from PySide import QtGui, QtCore
import os
import sys
import pprint

import NodeTypes

class CoreObject(dict):
    def __init__(self, AppPointer, MainWindowPointer):
        self.App = AppPointer
        self.MainWindow = MainWindowPointer
        super(CoreObject, self).__init__()
        #self['AppDirectory'] = os.curdir().replace('\\','/')
        self['AppDirectory'] = 'C:/Portfolio/Source/MediaApp'
        
        #Values common across all apps, loaded on a per project basis, curXpos, curYpos, root settings (see nuke) etc.
        self['AppAttributes'] = self['AppDirectory']+'/'+'AppAttributes.py'
        self.AppAttributes = self.parseFile(self['AppAttributes'])
        self.setImpliedAppAttributes()
        
        #Settings that change on a per user basis, colors, fonts, app particulars, etc
        self['AppPrefs'] = self['AppDirectory']+'/'+'AppPrefs.py'
        self.AppPrefs = self.parseFile(self['AppPrefs'])
        self.setImpliedAppPrefs()
        
        #Settings that change on per app basis, graph functions, widgets, font availability, preferences window etc
        self['AppSettings'] = self['AppDirectory']+'/'+'AppSettings.py'
        self.AppSettings = self.parseFile(self['AppSettings'])
        self.setImpliedAppSettings()
        
        self.Nodes = {}
        
    def parseFile(self, filePath):
        with open(filePath, 'r') as file:
            fileText = file.read()
        return eval(fileText)
       
    def setImpliedAppAttributes(self):
        pass
    def setImpliedAppPrefs(self):
        self.AppPrefs['AppFontMetrics'] = QtGui.QFontMetrics(self.AppPrefs['AppFont'])    
    def setImpliedAppSettings(self):
        pass
    
    
    def createNode(self, nodeType):
        node = eval('NodeTypes.'+nodeType+'(self)')
        self.Nodes[node.name()] = node
        return node
        
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
        str_Nodes = pprint.pformat(self.AppAttributes)
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