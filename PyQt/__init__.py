#===============================================================================
# @Author: Thomas McVay
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with PyQt Library
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

import sys

versionList = reversed(range(2, 99))
for a in versionList:
    version = 'PyQt'+str(a)
    try:
        exec('import '+version)
        sys.modules['__QtTemp__'] = sys.modules[version]
        from . import QtCore
        from . import QtGui
        from __QtTemp__ import QtSvg
        from __QtTemp__ import QtSql
        break
    except:
        pass
else:
    try:
        version = 'PySide'
        import PySide
        from PySide import QtGui, QtCore
        from PySide import QtSvg, QtSql
    except:
        #try:
        version = 'PySide2'
        import PySide2
        from PySide2 import QtGui, QtCore
        from PySide2 import QtSvg, QtSql
        from PySide2 import QtWidgets
        #except:
        #    raise Exception('MediaApp requires some version of PyQt or PySide to be installed in your /Python/site-packages folder')

print('QtWrapper: '+version)
print(sys.version)


#from . import QtCore
#from . import QtGui
#from __QtTemp__ import QtSvg
#from __QtTemp__ import QtSql

#del sys.modules['__QtTemp__']