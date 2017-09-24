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

import sys, os
if 'MediaApp' in sys.modules:
    import MediaApp

def DefaultSetup():
    global MainWindow, NodeGraph, BrowserBin, PropertiesBin, ViewerWidget
    MainWindow = MediaApp.Windows.MainWindow()
    
    #Required for ViewerNode
    NodeGraph = MediaApp.Widgets.NodeGraph()
    MainWindow.dockThisWidget(NodeGraph)
    
    BrowserBin = MediaApp.Widgets.BrowserBin()
    PropertiesBin = MediaApp.Widgets.PropertiesBin()
    ViewerWidget = MediaApp.Widgets.ViewerWidget()
    
    MainWindow.dockThisWidget(BrowserBin)
    MainWindow.dockThisWidget(PropertiesBin)
    MainWindow.dockThisWidget(ViewerWidget)

def run():
    DefaultSetup()
    def appThreadCall():
        import AppCore
        AppCore.App.exec_()
    MainWindow.initUI()
    MainWindow.show()
    appThreadCall()
if __name__ == '__main__':
    if os.path.abspath(__file__).split(os.sep)[-2] == 'MediaApp':
        if __package__ != 'MediaApp':
            import __init__ as MediaApp
        else:
            import MediaApp
        
    if os.path.abspath(__file__).split(os.sep)[-2] == 'MediaApp':
        run()
    else:
        import MediaApp
        MediaApp.run()