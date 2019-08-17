#===============================================================================
# @Author: Madison Aster
# @ModuleDescription: User End Preferences that can be edited and overridden via the 
#                     Preferences Menu. Default prefs can be overridden by wrapper
#                     Apps by copying this file from the MediaApp directory to the
#                     App Level directory and customizing it.
# @License: 
#    This example file is public domain. See ADDENDUM section in LICENSE.
#    You may do the following things with this file without restrictions or conditions:
#        1. Modify it.
#        2. Remove or modify this section to your liking.
#        3. Redistribute it under any licensing terms that you wish.
#        4. Make copyright claims to derivative works of this file.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#===============================================================================
import os, AppCore
from Qt import QtCore, QtGui

Data = {
#'*NWSTORAGE' : 'C:/',
'*NWSTORAGE' : os.getenv('*NWSTORAGE'),
'*BLACK' : None,

'AppFont' : QtGui.QFont('Times', 10, QtGui.QFont.Bold),
'AppIconColor1' : QtGui.QColor(17,17,17),
'AppIconColor2' : QtGui.QColor(34,34,34),
'AppIconColor3' : QtGui.QColor(51,51,51),
'AppIconColor4' : QtGui.QColor(68,68,68),
'AppIconColor5' : QtGui.QColor(85,85,85),
'AppIconColor6' : QtGui.QColor(102,102,102),
'AppIconColor7' : QtGui.QColor(119,119,119),
'AppIconColor8' : QtGui.QColor(136,136,136),
'AppIconColor9' : QtGui.QColor(153,153,153),
'AppIconColorA' : QtGui.QColor(170,170,170),
'AppIconColorB' : QtGui.QColor(187,187,187),
'AppIconColorC' : QtGui.QColor(204,204,204),
'AppIconColorD' : QtGui.QColor(221,221,221),
'AppIconColorE' : QtGui.QColor(238,238,238),
'NodeNamePadding' : 3,

'App-Window' : QtGui.QColor(50,50,50),
'App-Background' : QtGui.QColor(50,50,50), #IGNORED
'App-WindowText' : QtGui.QColor(255,255,255),
'App-Foreground' : QtGui.QColor(255,255,255), #IGNORED
'App-Base' : QtGui.QColor(50,50,50),
'App-AlternateBase' : QtGui.QColor(50,50,50),
'App-ToolTipBase' : QtGui.QColor(50,50,50),
'App-ToolTipText' : QtGui.QColor(50,50,50),
'App-Text' : QtGui.QColor(255,255,255),
'App-Button' : QtGui.QColor(100,100,100),
'App-ButtonText' : QtGui.QColor(255,255,255),
'App-BrightText' : QtGui.QColor(255,255,255),
'App-Light' : QtGui.QColor(100,100,100),
'App-Midlight' : QtGui.QColor(50,0,0),
'App-Dark' : QtGui.QColor(35,35,35),
'App-Mid' : QtGui.QColor(75,75,75),
'App-Shadow' : QtGui.QColor(10,10,10),
'App-Highlight' : QtGui.QColor(150,150,150),
'App-HighlightedText' : QtGui.QColor(50,50,50),
'App-Link' : QtGui.QColor(50,50,50),
'App-LinkVisited' : QtGui.QColor(50,50,50),
'App-NoRole' : QtGui.QColor(50,50,50),

'GraphWidget-Shortcuts-openNodes' : ['Enter'],
'GraphWidget-Shortcuts-marqMode' : ['LeftButton'],

'NodeGraph-bgColor' : QtGui.QColor(50,50,50),
'NodeGraph-nodeTrimPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'NodeGraph-marqBoxColor' : QtGui.QColor(255,255,255,25),
'NodeGraph-marqOutlinePen' : QtGui.QPen(QtGui.QColor(204,204,204), 2),
'NodeGraph-nodeSelectColor' : QtGui.QBrush(QtGui.QColor(252.45,186.15,99.45)),
'NodeGraph-nodeSelectPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'NodeGraph-gridPen' : QtGui.QPen(QtGui.QColor(204,204,204), 0),
'NodeGraph-pathPen01' : QtGui.QPen(QtGui.QColor(0,0,0), 5),

'ViewerWidget2D-bgColor' : QtGui.QColor(0,0,0),
'ViewerWidget2D-ResBoxColor' : QtGui.QColor(255,255,255,25),
'ViewerWidget2D-ResBoxPen' : QtGui.QPen(QtGui.QColor(204,204,204), 1),
'ViewerWidget2D-marqBoxColor' : QtGui.QColor(255,255,255,0),
'ViewerWidget2D-marqOutlinePen' : QtGui.QPen(QtGui.QColor(204,0,0), 1),
'ViewerWidget2D-Shortcuts-marqMode' : ['LeftButton', 'Shift'],
'ViewerWidget2D-Shortcuts-playForward' : ['Space'],
'ViewerWidget2D-Shortcuts-cacheFrames' : ['C'],
'ViewerWidget2D-Shortcuts-frameForward' : ['Right'],
'ViewerWidget2D-Shortcuts-frameBackward' : ['Left'],
'ViewerWidget2D-Features-3DView' : True,
'ViewerWidget2D-Features-2DView' : True,
'ViewerWidget2D-Defaults-Show3DView' : True,



'TimelineWidget-bgColor' : QtGui.QColor(50,50,50),
'TimelineWidget-nodeTrimPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'TimelineWidget-marqBoxColor' : QtGui.QColor(255,255,255,25),
'TimelineWidget-marqOutlinePen' : QtGui.QPen(QtGui.QColor(204,204,204), 2),
'TimelineWidget-nodeSelectColor' : QtGui.QBrush(QtGui.QColor(252.45,186.15,99.45)),
'TimelineWidget-nodeSelectPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'TimelineWidget-gridPen' : QtGui.QPen(QtGui.QColor(204,204,204,255), 1),
'TimelineWidget-ztiPen' : QtGui.QPen(QtGui.QColor(255,255,255,255), 1),
'TimelineWidget-ctiPen' : QtGui.QPen(QtGui.QColor(255,0,0,255), 1),
'TimelineWidget-Shortcuts-playForward' : ['Space'],
'TimelineWidget-Shortcuts-cacheFrames' : ['C'],
'TimelineWidget-Shortcuts-frameForward' : ['Right'],
'TimelineWidget-Shortcuts-frameBackward' : ['Left'],

'ColorKnob-DefaultColor' : QtGui.QColor(255,255,255),

'AbstractGraphArea-inputInterval' : 0.1,
'AbstractGraphArea-Shortcuts-zoom' : ['MidButton', 'LeftButton'],
'AbstractGraphArea-Shortcuts-pan' : ['MidButton'],

'FileMenu-Shortcuts-NewAction' : ['Ctrl+N'],
'FileMenu-Shortcuts-OpenAction' : ['Ctrl+O'],
'FileMenu-Shortcuts-ReloadAction' : ['Ctrl+R'],
'FileMenu-Shortcuts-SaveAction' : ['Ctrl+S'],
'FileMenu-Shortcuts-SaveAsAction' : ['Ctrl+Alt+S'],
'FileMenu-Shortcuts-CloseAction' : ['Ctrl+W'],
'FileMenu-Shortcuts-QuitAction' : ['Ctrl+Q'],

'EditMenu-Shortcuts-UndoAction' : ['Ctrl+Z'],
'EditMenu-Shortcuts-RedoAction' : ['Ctrl+Y'],
'EditMenu-Shortcuts-CutAction' : ['Ctrl+X'],
'EditMenu-Shortcuts-CopyAction' : ['Ctrl+C'],
'EditMenu-Shortcuts-PasteAction' : ['Ctrl+V'],
'EditMenu-Shortcuts-DeleteAction' : ['Delete'],
'EditMenu-Shortcuts-SelectAllAction' : ['Ctrl+A'],
'EditMenu-Shortcuts-RestoreLayoutAction' : ['Shift+F1'],
'EditMenu-Shortcuts-SaveLayoutAction' : ['Ctrl+F1'],
'EditMenu-Shortcuts-PrefsWindowAction' : ['Ctrl+Alt+P'],
'EditMenu-Shortcuts-PluginsWindowAction' : ['Ctrl+Shift+P'],
}
