#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Fechin <mr.fechin@gmail.com>
#
# Distributed under terms of the MIT license.

"""
根据Excel生成SQL文件
"""

from yaml import load
from types import FloatType
from functools import partial

import sys
import xlrd
import os
import re

reload(sys)
sys.setdefaultencoding("utf-8")

def load_config(filepath = "/conf.yaml"):
    """
    加载配置文件
    """
    f = open(sys.path[0] + filepath)
    result = load(f)
    f.close()
    return result

def walk_dir(rootdir):
    """
    遍历目录下所有xls文件
    """
    lst = []
    for parent, dirnames, filenames in os.walk(rootdir):
        for fname in filenames:
            if fname.endswith(".xls") or fname.endswith(".xlsx"):
                lst.append(fname)
    return lst

def read_xls(filepath = "files/file.xls",by_index = 0):
    """
    读取xls文档, 返回第by_index个Sheet
    """
    book = xlrd.open_workbook(filepath)
    table = book.sheet_by_index(by_index)
    return table

def write_file(filepath, lst):
    """
    把内容列表写入到文件中
    """
    data = "\n".join(lst)
    path = "%s/%s" %(sys.path[0], filepath)
    with open (path, "w") as f:
        f.write(data)
        print "Successfully!"


def table2sql(table, templates, toint, validrow):
    """
    将Excel表格转换成sql语句
    """
    nrows = table.nrows
    patt = re.compile(r"(\$\d+)|(\+\d+)|(\*)", re.I)
    lst = []
    for index in range(validrow - 1, nrows):
        increase = index - validrow + 1
        repl = partial(replacement, table.row_values(index), increase, toint)
        for sql in templates:
            lst.append(re.sub(patt, repl, sql));
    return lst

def replacement(row, increase, toint, matched):
    """
    re.sub()的替换函数
    """
    try:
        matchstr = matched.group()
        first    = matchstr[0]
        num      = matchstr[1:]
        result   = ""
        if first == "*":
            for item in row:
                if toint and type(item) is FloatType:
                    item = int(item)
                if item:
                    result += "'%s'," %str(item)
            result = result[:-1]
        elif first == "$":
            col = row[int(num) + 1]
            if toint and type(col) is FloatType:
                col = int(col)
            result = "'%s'" %col
        elif first == "+":
            result = int(num) + increase;
        return str(result);
    except IndexError, e:
        print "出错啦：下标超出实际范围，请检查模板属性!"
    except Exception, e:
        raise e
    return None

def main():
    # 加载配置文件，存储配置项
    config        = load_config();
    sql_templates = config["sql-templates"]
    toint         = config["float2int"]
    validrow      = config["validrow"]
    fdir          = config["xls-file-dir"];
    outputdir     = config["output-dir"];

    # 遍历目录，为目录下的xls/xlsx生成SQL，写入同名文件到输出目录
    files = walk_dir(fdir)
    for f in files:
        table = read_xls("%s/%s" %(fdir, f));
        lst = table2sql(table, sql_templates, toint, validrow);
        filepath = "%s/%s" %(outputdir, f.replace(".xlsx", ".sql").replace(".xls", ".sql"))
        write_file(filepath, lst)

if __name__ == "__main__":
    main()
