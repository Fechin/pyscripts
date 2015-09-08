#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Fechin <mr.fechin@gmail.com>
#
# Distributed under terms of the MIT license.

"""
列错位修复脚本
"""

from yaml import load
import sys,time, MySQLdb, xlrd

def load_config( filepath = '/conf.yaml' ):
    '''
    加载配置文件
    '''
    f = open(sys.path[0] + filepath)
    result = load(f)
    f.close()
    return result

def read_xls( filepath = 'file.xls',by_index = 0 ):
    '''
    读取xls文档, 返回第by_index个Sheet
    '''
    book = xlrd.open_workbook( filepath )
    table = book.sheet_by_index( by_index )
    return table

def select(sv,sql):
    '''
    查询数据
    '''
    try:
        db  = MySQLdb.connect(host=sv['host'], user=sv['user'],\
                passwd=sv['pawd'], db=sv['db'])
        cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        rs = cur.fetchall()
        cur.close()
        return rs
    except Exception, e:
        raise e

def update(sv,sql):
    '''
    更新数据
    '''
    try:
        db  = MySQLdb.connect(host=sv['host'], user=sv['user'],\
                passwd=sv['pawd'], db=sv['db'])
        cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        n = cur.execute(sql)    
        cur.close()
        db.commit()
        return n > 0
    except Exception, e:
        raise e


def log(str):
    '''
    打印日志
    '''
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\t" + str

def main():
    config        = load_config()
    select_server = config['select-server']
    update_server = config['update-server']
    table_name    = config['table-name']
    column_name   = config['column-name']

    table    = read_xls()
    colright = table.col_values( config['xls-col-right'] )
    colerror = table.col_values( config['xls-col-error'] )

    for i in range(1, table.nrows):
        if colerror[i]:
            sql = 'SELECT id FROM %s.%s WHERE %s = "%s"' \
                    %(select_server['db'], table_name, column_name, colerror[i])
            data = select(select_server, sql)
            if data:
                ids = tuple(str(x) for y in data for x in y.values())
                sql = 'UPDATE %s.%s SET %s = "%s" WHERE id in %s' \
                    %(update_server['db'], table_name, column_name, colright[i], ids)
                log("%s:%s:%s" %(i, colerror[i] , sql))
                update(update_server, sql)

if __name__ == '__main__':
    main()
