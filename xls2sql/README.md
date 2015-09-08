### 根据Excel生成SQL文件

------
*拿到内容团队整理出来的内容，需要写入数据库，于是编写了这个脚本，为什么不用java写个导入功能或用mysql导入cvs文件？因为到部分内容已经存在，不能直接Insert。脚本的特点是便于扩展、规则可配，根据`xls`文档生成SQL文件，可根据定义的SQL模板对一条记录生成不同的sql语句，具体模板格式请参照`conf.yaml`*


### 安装依赖
----
> * PyYAML  # 配置文件格式
> * xlrd    # Excel文档解析库

``` shell
pip install -r requirements.txt
```


### 配置说明
------
```
# 文件目录，需要处理的Excel文件夹，支持相对路径
xls-file-dir: files

# 文件目录，sql文件输出目录，支持相对路径
output-dir: result

# xsld读取的数字默认会转换成float类型，这个选项控制是否需要把float强转成int
float2int: True 

# 有效数据起始行号，程序会从行号等于validrow开始生成SQL
validrow: 3

# 生成的SQL语句模板: 根据Excel每一行数据对SQL模板进行匹配和填充
# 支持一对多: 一条Excel记录生成多条SQL，sql-templates可以有多个SQL模板
# 模板属性：
#       * : 星号取列所有值进行填充
#       $n: 美元符号和下标组合，取列的特定下标的值
#       +n: 加号和数字组合，以n+1的方式进行填充
sql-templates: 
    - "INSERT INTO episode(id, title) VALUES(*);"
    - "UPDATE episode SET id = $0, title = $1 WHERE id = +1;"


```
