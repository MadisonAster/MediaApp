#===============================================================================
# @Author: Madison Aster
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with Qt Library
#    Copyright (C) 2013 Madison Aster
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

#from .Clip import Clip
#from .ViewerNode import ViewerNode
#from .TimelineNode import TimelineNode


import os, sys, imp
from pprint import pprint
#import importlib.util
#import importlib
import AppCore

NodeConstructor = imp.load_source('NodeConstructor', __file__.replace('\\','/').rsplit('/',1)[0]+'/NodeConstructor.py')
#from .NodeConstructor import *
sys.modules['NodeConstructor'] = NodeConstructor

for BaseDirectory in AppCore['BaseDirectories']:
    for SubDirectory in AppCore.AppSettings['NodeDirectories']:
        if os.path.isdir(BaseDirectory+SubDirectory):
            for file in os.listdir(BaseDirectory+SubDirectory):
                if file.rsplit('.',1)[-1] == 'py':
                    ThisModule = sys.modules[__name__]
                    FunctionName = file.rsplit('.',1)[0]
                    #exec('from .'+FunctionName+' import *') #TODO: make imp work
                    
                    if FunctionName not in ['NodeConstructor', '__init__']:
                        #spec = importlib.util.spec_from_file_location(FunctionName, BaseDirectory+SubDirectory+'/'+file)
                        #module = importlib.util.module_from_spec(spec)
                        
                                                
                        #module = importlib.import_module(FunctionName)

                        #globals().update(
                        #    {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') 
                        #    else 
                        #    {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
                        #})
                        
                        #pprint(dir(ThisModule))
                        
                        #print(spec.loader.exec_module(module))
                        
                        
                        #exec('from .'+FunctionName+' import *') #TODO: make imp work
                        
                        module = imp.load_source(FunctionName, BaseDirectory+SubDirectory+'/'+file)
                        #from NewModule import *
                        
                        #print('dir', dir(module))
                        for d in dir(module):
                            dobj = type(getattr(module, d))
                            #print(d, dobj, isinstance(dobj, class))
                            #print(d, getattr(module, d).__module__)
                        #print('a;;', module.__module__)
                        #raise Exception('stop')
                        
                        for attrname in dir(module):
                            if not attrname.startswith('_') and attrname not in dir(ThisModule):
                                attr = getattr(module, attrname)
                               
                                #print('attr', attr, type(getattr(module, attr)))
                                setattr(ThisModule, attrname, attr)
                    
                    #foo.MyClass()
                    
                    #imp.load_source(FunctionName, BaseDirectory+SubDirectory+'/'+file)
                    
#from . import NodeConstructor