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

import os, sys
import hashlib

LibDir = __file__.replace('\\','/').rsplit('/',1)[0]
LicenseFound = False
CoreRun = False
if os.path.isfile(LibDir+'/LICENSE') and not os.path.exists(LibDir+'/MediaApp'):
    with open(LibDir+'/LICENSE', 'rb') as licenseFile:
        licenseHash = hashlib.sha256(licenseFile.read()).hexdigest()
    if licenseHash == 'fc90421b0c8175781a7744dd573e032924a2c70dc02f7c6f49b0a8705e580c3f':
        CoreRun = True
        LicenseFound = True
elif os.path.isfile(LibDir+'/MediaApp/LICENSE'):
    with open(LibDir+'/MediaApp/LICENSE', 'rb') as licenseFile:
        licenseHash = hashlib.sha256(licenseFile.read()).hexdigest()
    if licenseHash == 'fc90421b0c8175781a7744dd573e032924a2c70dc02f7c6f49b0a8705e580c3f':
        LicenseFound = True
if LicenseFound is True:
    #MediaApp Imports if this is MediaApp Library
    if CoreRun is True:  
        sys.path.append(LibDir.rsplit('/',1)[0])
        
        import PyQt
        sys.modules['PyQt'] = PyQt
        import AppCore
        sys.modules['AppCore'] = AppCore.Core()
        import DataStructures
        sys.modules['DataStructures'] = DataStructures
        import Icons
        sys.modules['MediaAppIcons'] = Icons
        import Knobs
        sys.modules['MediaAppKnobs'] = Knobs
        import Nodes
        sys.modules['MediaAppNodes'] = Nodes
        import Widgets
        sys.modules['MediaAppWidgets'] = Widgets
        import Windows
        sys.modules['MediaAppWindows'] = Windows
    else:
        import MediaApp
    #Only import run.py globals if Parent Directory has no run.py
    if not os.path.isfile(LibDir.rsplit('/',1)[0]+'/'+'run.py'):
        from run import *
    
