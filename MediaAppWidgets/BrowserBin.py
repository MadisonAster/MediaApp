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

from Qt import QtGui, QtCore, QtWidgets
    
import AppCore
#import MediaAppIcons
import MediaAppKnobs

class BrowserBin(QtWidgets.QWidget):
    def __init__(self):
        super(BrowserBin, self).__init__()
        self.setAccessibleName('BrowserBin')  #override visible name here
        ##################################
        self.binLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.binLayout)
        
        self.FilePath = MediaAppKnobs.FileKnob('C:/', name = '')
        self.FilePath.ValueChanged.connect(self.PathChanged)
        self.binLayout.addWidget(self.FilePath)
        
        self.fileTree = QtWidgets.QTreeWidget()
        self.fileTree.setColumnCount(3)
        self.fileTree.setHeaderLabels(['Name','Path','Size','Date']) 
        
        items = []
        for i in range(10):
            items.append(QtWidgets.QTreeWidgetItem(None, ['item_'+str(i),'W:/item_'+str(i),'0kb','142312']))
        self.fileTree.addTopLevelItems(items)
        self.binLayout.addWidget(self.fileTree)
        
        self.buttonLayout = QtWidgets.QHBoxLayout()
        
        Import_Button = QtWidgets.QPushButton("Import",self)
        ChangeName_Button = QtWidgets.QPushButton("ChangeName",self)
        ChangePath_Button = QtWidgets.QPushButton("ChangePath",self)
        SellectAssociated_Button = QtWidgets.QPushButton("SellectAssociated",self)
        Remove_Button = QtWidgets.QPushButton("Remove",self)
        
        self.buttonLayout.addWidget(Import_Button)
        self.buttonLayout.addWidget(ChangeName_Button)
        self.buttonLayout.addWidget(ChangePath_Button)
        self.buttonLayout.addWidget(SellectAssociated_Button)
        self.buttonLayout.addWidget(Remove_Button)
        
        self.binLayout.addLayout(self.buttonLayout)
        
        
    def PathChanged(self, newvalue):
        print('PathChanged!', newvalue)
        