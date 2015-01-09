#===============================================================================
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

{
#'*NWSTORAGE' : 'C:/',
'*NWSTORAGE' : os.getenv('*NWSTORAGE'),
'*BLACK' : 'somePath',

'AppFont' : QtGui.QFont('Times', 10, QtGui.QFont.Bold),
'NodeNamePadding' : 3,

'App-Window' : QtGui.QColor(50,50,50),
#'App-Background' : QtGui.QColor(0,50,0), IGNORED
'App-WindowText' : QtGui.QColor(255,255,255),
#'App-Foreground' : QtGui.QColor(0,50,0), IGNORED
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


'NodeGraph-bgColor' : QtGui.QColor(50,50,50),
'NodeGraph-nodeTrimPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'NodeGraph-marqBoxColor' : QtGui.QColor(255,255,255,25),
'NodeGraph-marqOutlinePen' : QtGui.QPen(QtGui.QColor(204,204,204), 2),
'NodeGraph-nodeSelectColor' : QtGui.QBrush(QtGui.QColor(252.45,186.15,99.45)),
'NodeGraph-nodeSelectPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'NodeGraph-gridPen' : QtGui.QPen(QtGui.QColor(204,204,204), 0),
'NodeGraph-pathPen01' : QtGui.QPen(QtGui.QColor(0,0,0), 5),

'Viewer-bgColor' : QtGui.QColor(0,0,0),
'Viewer-ResBoxColor' : QtGui.QColor(255,255,255,25),
'Viewer-ResBoxPen' : QtGui.QPen(QtGui.QColor(204,204,204), 1),
'Viewer-marqBoxColor' : QtGui.QColor(255,255,255,0),
'Viewer-marqOutlinePen' : QtGui.QPen(QtGui.QColor(204,0,0), 1),

'TimelineWidget-bgColor' : QtGui.QColor(50,50,50),
'TimelineWidget-nodeTrimPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'TimelineWidget-marqBoxColor' : QtGui.QColor(255,255,255,25),
'TimelineWidget-marqOutlinePen' : QtGui.QPen(QtGui.QColor(204,204,204), 2),
'TimelineWidget-nodeSelectColor' : QtGui.QBrush(QtGui.QColor(252.45,186.15,99.45)),
'TimelineWidget-nodeSelectPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'TimelineWidget-gridPen' : QtGui.QPen(QtGui.QColor(204,204,204,255), 1),
}
