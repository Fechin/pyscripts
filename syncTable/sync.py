#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Fechin <mr.fechin@gmail.com>
#
# Distributed under terms of the MIT license.
"""
数据同步脚本
"""

from yaml import load
import sys,time, MySQLdb

def conf():
    '''
    加载配置文件
    '''
    f = open(sys.path[0] + '/conf.yml')
    result = load(f)
    f.close()
    return result

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

def build_select_sql():
    '''
    根据配置过滤条件组织查询SQL
    '''
    sql = "SELECT * FROM " + conf()['table-name'] + " WHERE 1=1 "
    params = conf()['query-params']
    if not params:
        return
    for key,val in params.items():
        if isinstance(val,list):
            keys = str(tuple(set(val))).replace(",)", ")")
            sql += " AND " + key + " in " + keys
        else:
            sql += " AND " + key + " = " + str(val)
    log(sql)
    return sql


def build_update_sql(data):
    '''
    根据待同步数据组织更新SQL
    '''
    sql = ""
    if not data:
        return
    for i in range(len(data)):
        temp = "UPDATE " + conf()['table-name'] + " SET " +\
                "uniqueValue = '" + data[i]['uniqueValue'] + \
                "' WHERE uniqueKey = '" + data[i]['uniqueKey'] + "';"
        sql += temp;
    log(sql)
    return sql

def log(str):
    '''
    打印日志
    '''
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\t" + str

def main():
    log("sync start...")
    try:
        select_sql = build_select_sql()
        data = select(conf()['origin-server'], select_sql)
        update_sql = build_update_sql(data)
        update(conf()['dest-server'], update_sql)
        log("sync successfully!")
    except Exception, e:
        log("sync filed!")
        raise e

if __name__ == '__main__':
    main()
