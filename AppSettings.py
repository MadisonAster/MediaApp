#===============================================================================
# @Author: Thomas McVay
# @ModuleDescription: Application Level settings that can be overridden by the wrapper
#                     App by copying this file from the Media App directory to the App
#                     Level directory and customizing it.
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
'AppTitle' : 'MediaApp',
'AppIcon' : AppCore['CoreDirectory']+'/'+'MediaApp.ico',
'AppID' : 'ThomasMcVay.MediaApp.Framework.v0.1',
'FocusPolicy' : QtCore.Qt.ClickFocus,

'IconDirectories' : ['/Icons', '/MediaAppIcons'],
'KnobDirectories' : ['/Knobs', '/MediaAppKnobs'],
'NodeDirectories' : ['/Nodes', '/MediaAppNodes'],
'PluginDirectories' : ['/Plugins', '/MediaAppPlugins'],
'WidgetDirectories' : ['/Widgets', '/MediaAppWidgets'],
'WindowDirectories' : ['/Windows', '/MediaAppWindows'],

'NodeGraph-zoomSensitivity' : 1.0,
'NodeGraph-upperXZoomLimit' : 10,
'NodeGraph-upperYZoomLimit' : 10,
'NodeGraph-lowerXZoomLimit' : -0.9,
'NodeGraph-lowerYZoomLimit' : -0.9,
'NodeGraph-ZoomXYJoined' : True,

'NodeGraph-XPixelsPerUnit' : 1,
'NodeGraph-YPixelsPerUnit' : 1,
'NodeGraph-PaintXGridLines' : False,
'NodeGraph-PaintYGridLines' : False,

'ViewerWidget2D-zoomSensitivity' : 1.0,
'ViewerWidget2D-upperXZoomLimit' : 10,
'ViewerWidget2D-upperYZoomLimit' : 10,
'ViewerWidget2D-lowerXZoomLimit' : -0.9,
'ViewerWidget2D-lowerYZoomLimit' : -0.9,
'ViewerWidget2D-ZoomXYJoined' : True,
'ViewerWidget2D-XPixelsPerUnit' : 1,
'ViewerWidget2D-YPixelsPerUnit' : 1,


'TimelineWidget-zoomSensitivity' : 1.0,
'TimelineWidget-upperXZoomLimit' : 10,
'TimelineWidget-upperYZoomLimit' : 5,
'TimelineWidget-lowerXZoomLimit' : -0.9,
'TimelineWidget-lowerYZoomLimit' : 0.0,
'TimelineWidget-ZoomXYJoined' : False,

'TimelineWidget-XPixelsPerUnit' : 10,
'TimelineWidget-YPixelsPerUnit' : 24,
'TimelineWidget-YInverted' : False,
'TimelineWidget-PaintXGridLines' : False,
'TimelineWidget-PaintYGridLines' : False,


'FileMenu-Labels-NewAction' : 'New Project',
'FileMenu-Labels-OpenAction' : 'Open Project',
'FileMenu-Labels-ReloadAction' : 'Reload Project',
'FileMenu-Labels-SaveAction' : 'Save Project',
'FileMenu-Labels-SaveAsAction' : 'Save Project As',
'FileMenu-Labels-CloseAction' : 'Close Project',
'FileMenu-Labels-QuitAction' : 'Quit App',
'EditMenu-Labels-UndoAction' : 'Undo Action',
'EditMenu-Labels-RedoAction' : 'Redo Action',
'EditMenu-Labels-CutAction' : 'Cut Action',
'EditMenu-Labels-CopyAction' : 'Copy Action',
'EditMenu-Labels-PasteAction' : 'Paste Action',
'EditMenu-Labels-DeleteAction' : 'Delete Action',
'EditMenu-Labels-SelectAllAction' : 'Select All Action',
'EditMenu-Labels-RestoreLayoutAction' : 'Restore Layout',
'EditMenu-Labels-SaveLayoutAction' : 'Save Layout',
'EditMenu-Labels-PrefsWindowAction' : 'Edit Preferences',
'EditMenu-Labels-PluginsWindowAction' : 'Edit Plugins',

'FileMenu-StatusTips-NewAction' : 'New Project',
'FileMenu-StatusTips-OpenAction' : 'Open Project',
'FileMenu-StatusTips-ReloadAction' : 'Reload Project',
'FileMenu-StatusTips-SaveAction' : 'Save Project',
'FileMenu-StatusTips-SaveAsAction' : 'Save Project As',
'FileMenu-StatusTips-CloseAction' : 'Close Project',
'FileMenu-StatusTips-QuitAction' : 'Quit App',
'EditMenu-StatusTips-UndoAction' : 'Undo Action',
'EditMenu-StatusTips-RedoAction' : 'Redo Action',
'EditMenu-StatusTips-CutAction' : 'Cut Action',
'EditMenu-StatusTips-CopyAction' : 'Copy Action',
'EditMenu-StatusTips-PasteAction' : 'Paste Action',
'EditMenu-StatusTips-DeleteAction' : 'Delete Action',
'EditMenu-StatusTips-SelectAllAction' : 'Select All Action',
'EditMenu-StatusTips-RestoreLayoutAction' : 'Restore Layout',
'EditMenu-StatusTips-SaveLayoutAction' : 'Save Layout',
'EditMenu-StatusTips-PrefsWindowAction' : 'Edit Preferences',
'EditMenu-StatusTips-PluginsWindowAction' : 'Edit Plugins',

'FileMenu-Connections-NewAction' : 'self.NewFunction',
'FileMenu-Connections-OpenAction' : 'self.OpenFunction',
'FileMenu-Connections-ReloadAction' : 'self.ReloadFunction',
'FileMenu-Connections-SaveAction' : 'self.SaveFunction',
'FileMenu-Connections-SaveAsAction' : 'self.SaveAsFunction',
'FileMenu-Connections-CloseAction' : 'self.CloseFunction',
'FileMenu-Connections-QuitAction' : 'self.QuitFunction',

'EditMenu-Connections-UndoAction' : 'self.UndoFunction',
'EditMenu-Connections-RedoAction' : 'self.RedoFunction',
'EditMenu-Connections-CutAction' : 'self.CutFunction',
'EditMenu-Connections-CopyAction' : 'self.CopyFunction',
'EditMenu-Connections-PasteAction' : 'self.PasteFunction',
'EditMenu-Connections-DeleteAction' : 'self.DeleteFunction',
'EditMenu-Connections-SelectAllAction' : 'self.SelectAllFunction',
'EditMenu-Connections-RestoreLayoutAction' : 'self.RestoreLayoutFunction',
'EditMenu-Connections-SaveLayoutAction' : 'self.SaveLayoutFunction',
'EditMenu-Connections-PrefsWindowAction' : 'self.PrefsWindowFunction',
'EditMenu-Connections-PluginsWindowAction' : 'self.PluginsWindowFunction',

}
