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

from PySide import QtCore, QtGui, QtSvg

import AppCore

def IconFromSVG(iconPath):
    with open(iconPath, 'r') as iconFile:
        iconText = iconFile.read()

    iconText = iconText.replace('#111111', AppCore.AppPrefs['AppIconColor1'].name().encode("utf8"))
    iconText = iconText.replace('#222222', AppCore.AppPrefs['AppIconColor2'].name().encode("utf8"))
    iconText = iconText.replace('#333333', AppCore.AppPrefs['AppIconColor3'].name().encode("utf8"))
    iconText = iconText.replace('#444444', AppCore.AppPrefs['AppIconColor4'].name().encode("utf8"))
    iconText = iconText.replace('#555555', AppCore.AppPrefs['AppIconColor5'].name().encode("utf8"))
    iconText = iconText.replace('#666666', AppCore.AppPrefs['AppIconColor6'].name().encode("utf8"))
    iconText = iconText.replace('#777777', AppCore.AppPrefs['AppIconColor7'].name().encode("utf8"))
    iconText = iconText.replace('#888888', AppCore.AppPrefs['AppIconColor8'].name().encode("utf8"))
    iconText = iconText.replace('#999999', AppCore.AppPrefs['AppIconColor9'].name().encode("utf8"))
    iconText = iconText.replace('#AAAAAA', AppCore.AppPrefs['AppIconColorA'].name().encode("utf8"))
    iconText = iconText.replace('#BBBBBB', AppCore.AppPrefs['AppIconColorB'].name().encode("utf8"))
    iconText = iconText.replace('#CCCCCC', AppCore.AppPrefs['AppIconColorC'].name().encode("utf8"))
    iconText = iconText.replace('#DDDDDD', AppCore.AppPrefs['AppIconColorD'].name().encode("utf8"))
    iconText = iconText.replace('#EEEEEE', AppCore.AppPrefs['AppIconColorE'].name().encode("utf8"))
    iconStream = QtCore.QXmlStreamReader(iconText)
    svg_renderer = QtSvg.QSvgRenderer(iconStream)

    image = QtGui.QImage(64, 64, QtGui.QImage.Format_ARGB32)

    image.fill(0x00000000)
    svg_renderer.render(QtGui.QPainter(image))

    pixmap = QtGui.QPixmap.fromImage(image)

    return QtGui.QIcon(pixmap)
    
for file in os.listdir(AppCore['CoreDirectory']+'/Icons/'):
    if file.rsplit('.',1)[-1] == 'svg':
        exec('def '+file.rsplit('.',1)[0]+'(): return IconFromSVG(AppCore["CoreDirectory"]+"/Icons/'+file+'")')