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

from .IconFromSVG import *
from .IconFromColor import IconFromColor

import os, sys, types
import AppCore
           
for BaseDirectory in AppCore['BaseDirectories']:
    for SubDirectory in AppCore.AppSettings['IconDirectories']:
        if os.path.isdir(BaseDirectory+SubDirectory):
            for file in os.listdir(BaseDirectory+SubDirectory):
                if file.rsplit('.',1)[-1] == 'svg':
                    ThisModule = sys.modules[__name__]
                    FunctionName = file.rsplit('.',1)[0]
                    NewMethod = types.MethodType(IconFromSVG, BaseDirectory+SubDirectory+'/'+file)
                    setattr(ThisModule, FunctionName, NewMethod)
