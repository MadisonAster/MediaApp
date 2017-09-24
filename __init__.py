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
import cmd, threading
import hashlib

sys.path.append(os.path.abspath(__package__))

import PyQt
sys.modules['PyQt'] = PyQt
from PyQt import QtGui
sys.modules['QtGui'] = QtGui
from PyQt import QtCore
sys.modules['QtCore'] = QtCore
import AppCoreX
sys.modules['AppCore'] = AppCoreX.Core()
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

try:
    from .run import *
except:
    from run import *
    
