#===============================================================================
# @Author: Madison Aster
# @ModuleDescription: 
# @License:
#    MediaApp Library - Python Package framework for developing robust Media 
#                       Applications with Qt Library
#    Copyright (C) 2019 Madison Aster
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
import array, zlib
from struct import unpack
from collections import namedtuple

#############Globals################
SENTINEL_LENGTH = 13
SENTINEL_DATA = (b'\0'*SENTINEL_LENGTH)
BIG_ENDIAN = (__import__('sys').byteorder != 'little')
HEADER_MAGIC_NUMBER = b'Kaydara FBX Binary\x20\x20\x00\x1a\x00'

FBXElement = namedtuple("FBXElement", ("id", "props", "props_type", "elems"))
####################################

def main():
    for arg in sys.argv[1:]:
        fbx_root_elem, fbx_version = ParseFBX(arg)
def ParseFBX(FilePath, UseTuple=True):
    RootElements = []
    
    with open(FilePath, 'rb') as file:
        read = file.read
        tell = file.tell
        
        if read(len(HEADER_MAGIC_NUMBER)) != HEADER_MAGIC_NUMBER:
            raise IOError('Invalid Header')
        
        FileVersion = ReadUint(read)
        
        while True:
            Element = ReadElement(read, tell)
            if Element is None:
                break
            RootElements.append(Element)
            
    args = (b'', [], bytearray(0), RootElements)
    if UseTuple:
        return FBXElement(*args)
    else:
        return args, fbx_version
        
def ReadElement(read, tell, UseTuple):
    ElementLength = ReadUint(read)
    if ElementLength = 0:
        return None
    
    PropertyCount = ReadUint(read)
    PropertyLength = ReadUint(read)
    PropertyTypes = bytearray(PropertyCount)
    PropertyData = [None]*PropertyCount
    ElementID = ReadString(read)
    ElementTree = []
    
    for i in range(PropertyCount):
        DataType = read(1)[0]
        PropertyTypes[i] = DataType
        PropertyData[i] = GetOperation[DataType](read)
    #Recurse through child elements
    if tell() < ElementLength:
        while tell() < (ElementLength-SENTINEL_LENGTH):
            ElementTree.append(ReadElement(read, tell, UseTuple))
        if read(SENTINEL_LENGTH) != SENTINEL_DATA:
            raise IOError('Reached the end of an element block unexpectedly. Corrupt file?')
    if tell() != ElementLength:
        raise IOError('Element block was shorter than expected. Corrupt file?')
    
    args = (ElementID, PropertyData, PropertyTypes, ElementTree)
    if UseTuple:
        return FBXElement(*args)
    else:
        return args
def ReadUint(read):
    return unpack(b'<I', read(4))[0]
def ReadUbyte(read):
    return unpack(b'B', read(1))[0]
def ReadString(read):
    StringSize = ReadUbyte(read)
    StringData = read(StringSize)
    return StringData
def ReadArray(read, DataType, DataSize, ByteSwap):
    ElementCount = ReadUint(read)
    ArrayEncoding = ReadUint(read)
    DataLength = ReadUint(read)
    Data = read(DataLength)
    
    if ArrayEncoding == 1:
        Data = zlib.decompress(Data)
    
    assert(ElementCount * DataSize == len(Data))
    
    DataArray = array.array(DataType, Data)
    if ByteSwap and _IS_BIG_ENDIAN:
        DataArray.byteswap()
    return DataArray
def GetOperation(DataType):
    Operations = {
        b'Y'[0]: lambda read: unpack(b'<h', read(2))[0],  # 16 bit int
        b'C'[0]: lambda read: unpack(b'?', read(1))[0],   # 1 bit bool (yes/no)
        b'I'[0]: lambda read: unpack(b'<i', read(4))[0],  # 32 bit int
        b'F'[0]: lambda read: unpack(b'<f', read(4))[0],  # 32 bit float
        b'D'[0]: lambda read: unpack(b'<d', read(8))[0],  # 64 bit float
        b'L'[0]: lambda read: unpack(b'<q', read(8))[0],  # 64 bit int
        b'R'[0]: lambda read: read(ReadUint(read)),      # binary data
        b'S'[0]: lambda read: read(ReadUint(read)),      # string data
        b'f'[0]: lambda read: ReadArray(read, 'f', 4, False),  # array (float)
        b'i'[0]: lambda read: ReadArray(read, 'i', 4, True),   # array (int)
        b'd'[0]: lambda read: ReadArray(read, 'd', 8, False),  # array (double)
        b'l'[0]: lambda read: ReadArray(read, 'q', 8, True),   # array (long)
        b'b'[0]: lambda read: ReadArray(read, 'b', 1, False),  # array (bool)
        b'c'[0]: lambda read: ReadArray(read, 'B', 1, False),  # array (ubyte)
    }
    return Operations[DataType]

if __name__ == '__main__':
    main()