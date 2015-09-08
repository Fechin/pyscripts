#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Fechin <mr.fechin@gmail.com>
#
# Distributed under terms of the MIT license.

"""
根据xls生成键值对的配置文件
"""

import re
import sys
import xlrd
from yaml import load

reload(sys)
sys.setdefaultencoding( "utf-8"  )

def _path( filename ):
    '''
    文件绝对路径
    '''
    return sys.path[0] + '/' + filename

def read_config( filename = 'conf.yaml' ):
    ''' 
    加载配置文件
    '''
    result = None
    with open (_path(filename), "r") as f:
        result = load(f)
    return result

def read_xls( filename= 'file.xls',by_index = 0 ):
    '''
    读取xls文档, 返回第by_index个Sheet
    '''
    book  = xlrd.open_workbook( _path(filename) )
    table = book.sheet_by_index( by_index )
    return table

def deal_title( title ):
    '''
    去除字符!',./\?-()*&:;？（），和空格
    '''
    title = str(title.lower())
    _p = re.compile( r"(!|'|,|\.|/|\\|\?|-|\(|\)|\*|&|:|;|？|（|）|，)| " )
    title = _p.sub( "", title )
    return title

def build_list( config ):
    '''
    生成键值对内容列表
    '''
    cols   = config['xls-col-keys']
    value  = config['xls-col-val']
    table  = read_xls( config['xls-name'], 0 )

    lst = []
    keylst = []

    for row in range(1, table.nrows):
        val = table.cell_value(row, value)
        for col in cols:
            title = table.cell_value(row,col)
            key = deal_title( title )

            # 判断key是否有重复
            repeats = [x for x in keylst if x == key]
            if repeats:
                print "警告:发现重复key:", title

            keylst.append(key)
            lst.append( "%s%s%s" %( key, "=", val ) )
    return lst

def write_file( config ):
    '''
    把内容列表写入到文件中
    '''
    filename = config['file-name']
    lst      = build_list( config )
    header   = """
        # 该配置通过脚本buildprops/build.py生成
        # @Author : Fechin
        # @link   : https://github.com/Fechin/pyscripts/tree/master/buildprops \n\n"""
    data     = "\n".join(lst)

    with open (_path(filename), "w") as f:
        f.write( header )
        f.write( data )
        print "Successfully!"

if __name__ == '__main__':
    config   = read_config()
    write_file( config )
