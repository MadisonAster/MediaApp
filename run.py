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

from PySide import QtGui, QtCore
#import sys
import cmd
import threading

try:
    import MediaApp
except:
    import __init__ as MediaApp


Core = MediaApp.Core()
Cmd = cmd.Cmd()
MainWindow = MediaApp.Windows.createWindow(Core)

BrowserBin = MediaApp.Widgets.BrowserBin(Core)
PropertiesBin = MediaApp.Widgets.PropertiesBin(Core)
ViewerWidget = MediaApp.Widgets.ViewerWidget(Core)
TimelineWidget = MediaApp.Widgets.TimelineWidget(Core)

MainWindow.dockThisWidget(BrowserBin)
MainWindow.dockThisWidget(PropertiesBin)
MainWindow.dockThisWidget(ViewerWidget)
MainWindow.dockThisWidget(TimelineWidget)
 
def run():
    def cmdThreadCall():
        Cmd.cmdloop()
    def appThreadCall():
        Core.App.exec_()
        
    MainWindow.initUI()
    MainWindow.show()
        
    #cmdThread = threading.Thread(target=cmdThreadCall)
    #cmdThread.start()
    
    appThreadCall()
    #appThread = threading.Thread(target=appThreadCall)
    #appThread.start()
    #appThread.join(timeout)
    #if appThread.isAlive():
    #    print 'Terminating process'