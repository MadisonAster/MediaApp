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

from PySide import QtGui, QtCore
import imageio

import os, gc
import sys
import pprint
import ctypes


class Core(dict):
    def __init__(self, argString = ''):
        super(Core, self).__init__()
        
        #QtGui.QApplication.setColorSpec(QtGui.QApplication.ManyColor)
        self.App = QtGui.QApplication(argString)
        
        self.setPaths()
        
        self.AppAttributes = self.parseFile(self['AppAttributes'])
        self.AppSettings = self.parseFile(self['AppSettings'])
        try:
            self.AppPrefs = self.parseFile(self['UserAppPrefs'])
        except:
            self.AppPrefs = self.parseFile(self['AppPrefs'])
            
        self.setImpliedAppAttributes()
        self.setImpliedAppPrefs()
        self.setImpliedAppSettings()
        
        #self.AppAttributes = Values common across all apps, loaded on a per project basis, curXpos, curYpos, root settings (see nuke) etc.
        #self.AppPrefs = Settings that change on a per user basis, colors, fonts, app particulars, etc
        #self.AppSettings = Settings that change on per app basis, graph functions, widgets, font availability, preferences window etc
        
        self.App.setPalette(self.getPalette('App'))
        
        
        self.Nodes = {}
        
        self.ctypesMagic()
        
    def setPaths(self):
        self['CoreDirectory'] = __file__.replace('\\','/').rsplit('/',2)[0]
        self['AppDirectory'] = self['CoreDirectory'].rsplit('/',1)[0]
        
        
        #See if app specific pref files exist, otherwise use defaults in core directory
        foundCount = 0
        for fileName in ['AppAttributes.py', 'AppPrefs.py', 'AppSettings.py']:
            if os.path.isfile(self['AppDirectory']+'/'+fileName) == True:
                self[fileName.rsplit('.',1)[0]] = self['AppDirectory']+'/'+fileName
                foundCount += 1
            else:
                self[fileName.rsplit('.',1)[0]] = self['CoreDirectory']+'/'+fileName
                
        if foundCount == 0:
            self['AppDirectory'] = self['CoreDirectory']
        self['AppDataDirectory'] = os.getenv('APPDATA')+'/MediaApp/'+self['AppDirectory'].rsplit('/',1)[1]
        self['UserAppPrefs'] = self['AppDataDirectory']+'/'+'UserAppPrefs.py'
        
    def ctypesMagic(self):
        #Windows Taskbar icon work around
        winAppID = self.AppSettings['AppID']
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(winAppID)
        
    def RegisterObject(self, objectPointer, objectString = None):
        if objectString == None:
            objectString = type(objectPointer).__name__
        exec('self.'+objectString+' = objectPointer')
        
    def parseFile(self, filePath):
        with open(filePath, 'r') as file:
            fileText = file.read()
        return eval(fileText)
       
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
    
   
    def createNode(self, nodeType, parent = None):
        evalString = 'NodeTypes.'+nodeType+'()'
        node = eval(evalString)
        node.setParent(parent)
        self.Nodes[node.name()] = node
        return node
        
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
    def getCurrentFrame(self):
        return self.AppAttributes['ctiTop'][0]
        
    def getPalette(self, widgetName):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, self.AppPrefs[widgetName+'-Window'])
        #palette.setColor(QtGui.QPalette.Background, self.AppPrefs[widgetName+'-Background']) IGNORED
        palette.setColor(QtGui.QPalette.WindowText, self.AppPrefs[widgetName+'-WindowText'])
        #palette.setColor(QtGui.QPalette.Foreground, self.AppPrefs[widgetName+'-Foreground']) IGNORED
        palette.setColor(QtGui.QPalette.Base, self.AppPrefs[widgetName+'-Base'])
        palette.setColor(QtGui.QPalette.AlternateBase, self.AppPrefs[widgetName+'-AlternateBase'])
        palette.setColor(QtGui.QPalette.ToolTipBase, self.AppPrefs[widgetName+'-ToolTipBase'])
        palette.setColor(QtGui.QPalette.ToolTipText, self.AppPrefs[widgetName+'-ToolTipText'])
        palette.setColor(QtGui.QPalette.Text, self.AppPrefs[widgetName+'-Text'])
        palette.setColor(QtGui.QPalette.Button, self.AppPrefs[widgetName+'-Button'])
        palette.setColor(QtGui.QPalette.ButtonText, self.AppPrefs[widgetName+'-ButtonText'])
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
        return palette

#Importable Singleton Magic
Core.instance = Core() 
import sys
_ref = sys.modules[__name__]  # Reference to current module so it's not deleted
sys.modules['AppCore'] = Core.instance

import NodeTypes