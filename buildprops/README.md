### 键值对生成脚本

------
*根据`xls`文档及`conf.yaml`文件配置的键/值对应的列，生成`config.properties`配置文件，内容以键值对(Key-Value)存储，生成效果如下：*

``` 
key1=value1
key2=value1
key3=value1
key4=value2
key5=value3
```
### 安装依赖
----
> * PyYAML  # 配置格式
> * xlrd    # xls读取

``` shell
pip install -r requirements.txt
```

### 配置说明
------
``` yaml
# 待处理xls数据
xls-name     : "file.xls"

# keys同时对应xls-col-val
xls-col-keys : [0,2,3]
xls-col-val  : 1

# 生成的文件名
file-name    : "config.properties"

```
