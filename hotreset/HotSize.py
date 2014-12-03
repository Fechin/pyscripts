#! /usr/bin/env python:
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Fechin <lihuoqingfly@163.com>
#
# Distributed under terms of the MIT license.

"""
热点缩放工具

根据原图(O)和新图(N)的高度变化等比例缩放热点
例(需通过此脚本改变坐标startY、endY):
    原热点：60,430,143,558
    新热点：60,323,143,419

总结公式：
N.startY = O.startY * ( N.height / O.height )
N.endY   = O.endY * ( N.height / O.height )

适用场合：原图高大于新图高; 原图和新图宽度相同
"""

import os , sys
import struct

FILE_UNKNOWN = "对不起，文件大小获取失败!"
O_HEIGHT = 600
O_WIDTH  = 600

def getZoomSize( imgFile ):
    """获取原图和新图高度缩放比例

    :imgFile: 新图
    :returns: 差值

    """
    try:
        width, height = get_image_size( imgFile )
        # 根据宽度等比缩放后的高度
        zoomed_height = float( O_WIDTH ) / float( width ) * height
        return zoomed_height / O_HEIGHT
    except UnknownImageFormat:
        pass

def resetHot( O_HOT, N_IMG ):
    """根据缩放比例调整坐标startY,endY并返回

    :O_HOT: 待调整热点
    :N_IMG: 新图
    :returns: 最终热点

    """
    hotLst = O_HOT.split(",")
    zoom = getZoomSize( N_IMG )

    hotLst[1] = str(int(int(hotLst[1]) * zoom))
    hotLst[3] = str(int(int(hotLst[3]) * zoom))

    hotStr = ""
    for hot in hotLst:
        hotStr = hotStr + hot + ','
    return hotStr[:-1]

def get_image_size(file_path):
    """获取文件尺寸

    :file_path: 文件路径
    :returns: 宽，高

    """

    size = os.path.getsize(file_path)
    with open(file_path) as input:
        height = -1
        width = -1
        data = input.read(25)
        msg = " raised while trying to decode as JPEG."

        if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
            # GIFs
            w, h = struct.unpack("<HH", data[6:10])
            width = int(w)
            height = int(h)
        elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
              and (data[12:16] == 'IHDR')):
            # PNGs
            w, h = struct.unpack(">LL", data[16:24])
            width = int(w)
            height = int(h)
        elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
            # older PNGs
            w, h = struct.unpack(">LL", data[8:16])
            width = int(w)
            height = int(h)
        elif (size >= 2) and data.startswith('\377\330'):
            # JPEG
            input.seek(0)
            input.read(2)
            b = input.read(1)
            try:
                while (b and ord(b) != 0xDA):
                    while (ord(b) != 0xFF): b = input.read(1)
                    while (ord(b) == 0xFF): b = input.read(1)
                    if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                        input.read(3)
                        h, w = struct.unpack(">HH", input.read(4))
                        break
                    else:
                        input.read(int(struct.unpack(">H", input.read(2))[0])-2)
                    b = input.read(1)
                width = int(w)
                height = int(h)
            except struct.error:
                raise UnknownImageFormat("StructError" + msg)
            except ValueError:
                raise UnknownImageFormat("ValueError" + msg)
            except Exception as e:
                raise UnknownImageFormat(e.__class__.__name__ + msg)
        elif size >= 2:
        	#see http://en.wikipedia.org/wiki/ICO_(file_format)
        	input.seek(0)
        	reserved = input.read(2)
        	if 0 != struct.unpack("<H", reserved )[0]:
        		raise UnknownImageFormat(FILE_UNKNOWN)
        	format = input.read(2)
        	assert 1 == struct.unpack("<H", format)[0]
        	num = input.read(2)
        	num = struct.unpack("<H", num)[0]
        	if num > 1:
        		import warnings
        		warnings.warn("ICO File contains more than one image")
        	w = input.read(1)
        	h = input.read(1)
        	width = ord(w)
        	height = ord(h)
        else:
            raise UnknownImageFormat(FILE_UNKNOWN)

    return width, height

class UnknownImageFormat(Exception):
    pass

if __name__ == '__main__':
    O_HOT    = "60,430,143,558"
    N_IMG    = "067c69c3-85d9-44e4-bec1-f176057d0e1f-b.jpg"
    for arg in sys.argv:
        if arg.startswith('-i'):
            N_IMG = arg[2:]
        if arg.startswith('-h'):
            O_HOT = arg[2:]
    print resetHot( O_HOT, N_IMG )
