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

import os, time
from Qt import QtGui, QtCore, QtWidgets
    
import AppCore
import MediaAppIcons
import MediaAppKnobs

class BrowserBin(QtWidgets.QWidget):
    def __init__(self):
        super(BrowserBin, self).__init__()
        self.setAccessibleName('BrowserBin')  #override visible name here
        ##################################
        self.binLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.binLayout)
        
        self.RootPath = ''
        self.FilePath = MediaAppKnobs.FileKnob(self.RootPath, name = 'RootPath')
        self.FilePath.ValueChanged.connect(self.PathChanged)
        self.binLayout.addWidget(self.FilePath)
        
        self.fileTree = QtWidgets.QTreeWidget()
        self.fileTree.setColumnCount(3)
        self.fileTree.setHeaderLabels(['Name','Size','Modified'])
        self.fileTree.header().resizeSection(0, 300)
        
        self.binLayout.addWidget(self.fileTree)
                
        self.fileTree.itemExpanded.connect(self.ScanItem)
        
        self.FilePath.setValue('C:/')
    def RemoveAllItems(self):
        root = self.fileTree.invisibleRootItem()
        for i in reversed(range(root.childCount())):
            root.removeChild(root.child(i))
            
    def PathChanged(self, newvalue):
        self.RootPath = newvalue
        
        self.RemoveAllItems()
        items = []
        for root, dirs, files in os.walk(self.RootPath):
            for dir in dirs:
                newitem = QtWidgets.QTreeWidgetItem(None, [dir, '-', time.ctime(os.path.getmtime(root+'/'+dir))])
                newitem.setIcon(0, MediaAppIcons.Folder1())
                newitem.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)
                items.append(newitem)
            for file in files:
                newitem = QtWidgets.QTreeWidgetItem(None, [file, str(os.path.getsize(root+'/'+file)/1000)+' KB', time.ctime(os.path.getmtime(root+'/'+file))])
                newitem.setIcon(0, MediaAppIcons.File1())
                items.append(newitem)
            break
        self.fileTree.addTopLevelItems(items)
        
    def ScanItem(self, item):
        itempath = self.RootPath
        treestack = [item.text(0)]
        parentitem = item.parent()
        while type(parentitem) != type(None):
            treestack.insert(0,parentitem.text(0))
            parentitem = parentitem.parent()
        for treeitem in treestack:
            itempath += '/'+treeitem
        
        for root, dirs, files in os.walk(itempath):
            for dir in dirs:
                newitem = QtWidgets.QTreeWidgetItem(None, [dir, '-', time.ctime(os.path.getmtime(root+'/'+dir))])
                newitem.setIcon(0, MediaAppIcons.Folder1())
                newitem.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)
                item.addChild(newitem)
            for file in files:
                newitem = QtWidgets.QTreeWidgetItem(None, [file, str(os.path.getsize(root+'/'+file)/1000)+' KB', time.ctime(os.path.getmtime(root+'/'+file))])
                newitem.setIcon(0, MediaAppIcons.File1())
                item.addChild(newitem)
            break