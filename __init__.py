#===============================================================================
# @Author: Thomas McVay
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with Qt Library
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

import os, sys
if os.path.abspath(__file__).split(os.sep)[-2] == 'MediaApp':
    sys.modules['MediaApp'] = sys.modules[__name__]
    if __name__ == '__init__':
        #import Qt
        #sys.modules['Qt'] = Qt
        #from Qt import QtGui
        #sys.modules['QtGui'] = QtGui
        #from Qt import QtCore
        #sys.modules['QtCore'] = QtCore
        import AppCoreX
        AppCore = AppCoreX.Core()
        sys.modules['AppCore'] = AppCore
        
        import DataStructures
        sys.modules['DataStructures'] = DataStructures
        import MediaAppIcons as Icons
        sys.modules['MediaAppIcons'] = Icons
        import MediaAppKnobs as Knobs
        sys.modules['MediaAppKnobs'] = Knobs
        import MediaAppNodes as Nodes
        sys.modules['MediaAppNodes'] = Nodes
        import MediaAppWidgets as Widgets
        sys.modules['MediaAppWidgets'] = Widgets
        import MediaAppWindows as Windows
        sys.modules['MediaAppWindows'] = Windows
    else:
        #from . import Qt
        #sys.modules['Qt'] = Qt
        #from Qt import QtGui
        #sys.modules['QtGui'] = QtGui
        #from Qt import QtCore
        #sys.modules['QtCore'] = QtCore
        from . import AppCoreX
        AppCore = AppCoreX.Core()
        sys.modules['AppCore'] = AppCore
        
        from . import DataStructures
        sys.modules['DataStructures'] = DataStructures
        from . import MediaAppIcons as Icons
        sys.modules['MediaAppIcons'] = Icons
        from . import MediaAppKnobs as Knobs
        sys.modules['MediaAppKnobs'] = Knobs
        from . import MediaAppNodes as Nodes
        sys.modules['MediaAppNodes'] = Nodes
        from . import MediaAppWidgets as Widgets
        sys.modules['MediaAppWidgets'] = Widgets
        from . import MediaAppWindows as Windows
        sys.modules['MediaAppWindows'] = Windows
    
    MainWindow = Windows.MainWindow()
    NodeGraph = Widgets.NodeGraph()
    AppCore.NodeGraph = NodeGraph
    BrowserBin = Widgets.BrowserBin()
    PropertiesBin = Widgets.PropertiesBin()
    ViewerWidget = Widgets.ViewerWidget()
    MainWindow.dockThisWidget(NodeGraph)
    MainWindow.dockThisWidget(BrowserBin)
    MainWindow.dockThisWidget(PropertiesBin)
    MainWindow.dockThisWidget(ViewerWidget)
    def run():
        MainWindow.initUI()
        MainWindow.show()
        AppCore.App.exec_()
else:
    if __name__ == '__init__':
        from MediaApp import *
    else:
        from .MediaApp import *
    ##### Add your App's import statements here #####
    
    