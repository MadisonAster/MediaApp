#===============================================================================
# @Author: Thomas McVay
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with PySide Library
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

import os
LibDir = __file__.replace('\\','/').rsplit('/',1)[0]

#MediaApp Imports if this is MediaApp Library
if os.path.isfile(LibDir+'/MediaApp_LGPL.txt') and not os.path.exists(LibDir+'/MediaApp'):    
    import Widgets
    import Windows
    #import FileManager
    #import Timer
    #import TCP
    #import Phonon
    from Core import *
elif os.path.isfile(LibDir+'/MediaApp/MediaApp_LGPL.txt'):
    import MediaApp


#Only import run.py globals if Parent Directory has no run.py
if not os.path.isfile(LibDir.rsplit('/',1)[0]+'/'+'run.py'):
    from run import *
    
