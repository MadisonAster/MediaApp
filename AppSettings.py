#===============================================================================
# @License: 
#    This example file is public domain. See MediaApp_LGPL.txt ADDENDUM.
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

{
'AppTitle' : 'MediaApp',
'AppIcon' : self['AppDirectory']+'/'+'MediaApp.ico',
'AppID' : 'ThomasMcVay.MediaApp.Framework.v0.1',
'FocusPolicy' : QtCore.Qt.ClickFocus,

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

'ViewerWidget-zoomSensitivity' : 1.0,
'ViewerWidget-upperXZoomLimit' : 10,
'ViewerWidget-upperYZoomLimit' : 10,
'ViewerWidget-lowerXZoomLimit' : -0.9,
'ViewerWidget-lowerYZoomLimit' : -0.9,
'ViewerWidget-ZoomXYJoined' : True,
'ViewerWidget-XPixelsPerUnit' : 1,
'ViewerWidget-YPixelsPerUnit' : 1,


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
}
