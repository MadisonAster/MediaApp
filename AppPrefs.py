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
#'*NWSTORAGE' : 'C:/',
'*NWSTORAGE' : os.getenv('*NWSTORAGE'),

'AppFont' : QtGui.QFont('Times', 10, QtGui.QFont.Bold),
'NodeNamePadding' : 3,

'GraphWidget-bgColor' : QtGui.QColor(50,50,50),
'GraphWidget-nodeTrimPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'GraphWidget-marqBoxColor' : QtGui.QColor(255,255,255,25),
'GraphWidget-marqOutlinePen' : QtGui.QPen(QtGui.QColor(204,204,204), 2),
'GraphWidget-nodeSelectColor' : QtGui.QBrush(QtGui.QColor(252.45,186.15,99.45)),
'GraphWidget-nodeSelectPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'GraphWidget-gridPen' : QtGui.QPen(QtGui.QColor(204,204,204), 0),

'ViewerWidget-bgColor' : QtGui.QColor(0,0,0),
'ViewerWidget-ResBoxColor' : QtGui.QColor(255,255,255,25),
'ViewerWidget-ResBoxPen' : QtGui.QPen(QtGui.QColor(204,204,204), 1),
'ViewerWidget-marqBoxColor' : QtGui.QColor(255,255,255,0),
'ViewerWidget-marqOutlinePen' : QtGui.QPen(QtGui.QColor(204,0,0), 1),

'Timeline-bgColor' : QtGui.QColor(50,50,50),
'Timeline-nodeTrimPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'Timeline-marqBoxColor' : QtGui.QColor(255,255,255,25),
'Timeline-marqOutlinePen' : QtGui.QPen(QtGui.QColor(204,204,204), 2),
'Timeline-nodeSelectColor' : QtGui.QBrush(QtGui.QColor(252.45,186.15,99.45)),
'Timeline-nodeSelectPen' : QtGui.QPen(QtGui.QColor(0,0,0), .5),
'Timeline-gridPen' : QtGui.QPen(QtGui.QColor(204,204,204,255), 1),
}
