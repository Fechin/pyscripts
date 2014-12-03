### 使用说明
------
*该脚本实现跨服务器同步单表数据，可以配置query-params进行过滤，如果query-params为空，将完整同步表的所有数据，这个脚本采用[Yaml](http://www.yaml.org/)配置风格，所以需要安装Yaml for python 模块支持，请切换到root权限进行安装：*

> wget http://pyyaml.org/download/pyyaml/PyYAML-3.11.tar.gz

> tar -zxvf PyYAML-3.11.tar.gz 

> cd PyYAML-3.11 && python setup.py install

------
> wget http://jaist.dl.sourceforge.net/project/mysql-python/mysql-python-test/1.2.4b4/MySQL-python-1.2.4b4.tar.gz

> tar -zxvf MySQL-python-1.2.4b4.tar.gz

> cd MySQL-python-1.2.4b4

> python setup.py build && python setup.py install

### 配置说明
------
``` yaml
# 待同步服务器连接
origin-server:
    host: "192.168.20.130"
    port: "3306"
    db: "ivmall"
    user: "orbit_java"
    pawd: "orbit_java"

# 同步目标服务器连接
dest-server:
    host: "192.168.20.130"
    port: "3306"
    db: "ivmall"
    user: "orbit_java"
    pawd: "orbit_java"

# 需同步的表
table-name: "platform_configuration"

# 同步过滤条件,可添加类似uniqueKey列表/固定id的条件
query-params:
    # id: 1
    uniqueKey:
      - "wxc4921110daeec4f6"
      - "wxc4921110daeec4f6"
      - "wxc4921110daeec4f6"
      - "wxc4921110daeec4f6"
```
