### 使用说明
------


*该脚本用于修复列错位的数据，需提供`xls`修复文档，格式如下，将列值等于`oldContentID`更新为`contentID`*

contentID     | oldContentID
--------------| -------------
SER_Bill_Ep19 |
SER_Bill_Ep20 |
SER_Bill_Ep22 | SER_Bill_Ep21
SER_Bill_Ep24 | SER_Bill_Ep22
SER_Bill_Ep25 | SER_Bill_Ep23
SER_Bill_Ep27 | SER_Bill_Ep23

### 安装依赖
----
* PyYAML  # 配置格式
* xlrd    # xls读取
* MySQL-python

```
pip install -r requirements.txt
```

### 配置说明
------
```yml
# 查询服务器
select-server:
    host: "192.168.20.130"
    port: "3306"
    db  : "mnj_heartbeat"
    user: "orbit_java"
    pawd: "orbit_java"

# 更新服务器
update-server:
    host: "192.168.20.130"
    port: "3306"
    db  : "ivmall"
    user: "orbit_java"
    pawd: "orbit_java"

# 待处理xls数据
xls-name: "file.xls"
# 正确列的rownum
xls-col-right: 0
# 错误列的rownum
xls-col-error: 1

# 表名
table-name : "question"
# 字段名
column-name: "contentId"
```
