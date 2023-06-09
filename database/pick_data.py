import os

import pandas as pd

# 读取csv文件
path1 = 'data/2009年居民消费性支出数据.csv'
path2 = 'data/2010年居民消费性支出数据.csv'
path3 = 'data/2011年居民消费性支出数据.csv'
path4 = 'data/2012年居民消费性支出数据.csv'
path5 = 'data/2013年居民消费性支出数据.csv'
path6 = 'data/2014年居民消费性支出数据.csv'
path7 = 'data/2015年居民消费性支出数据.csv'
path8 = 'data/2016年居民消费性支出数据.csv'
path9 = 'data/2017年居民消费性支出数据.csv'
path10 = 'data/2018年居民消费性支出数据.csv'
path11 = 'data/2019年居民消费性支出数据.csv'
path12 = 'data/2020年居民消费性支出数据.csv'

# 2009年
data1 = pd.read_csv(path1, header=None)

# 2012年
data2 = pd.read_csv(path2, header=None)

# 2011年
data3 = pd.read_csv(path3, header=None)

# 2012年
data4 = pd.read_csv(path4, header=None)

# 2013年
data5 = pd.read_csv(path5, header=None)

# 2014年
data6 = pd.read_csv(path6, header=None)

# 2015年
data7 = pd.read_csv(path7, header=None)

# 2016年
data8 = pd.read_csv(path8, header=None)

# 2017年
data9 = pd.read_csv(path9, header=None)

# 2018年
data10 = pd.read_csv(path10, header=None)

# 2019年
data11 = pd.read_csv(path11, header=None)

# 2020年
data12 = pd.read_csv(path12, header=None)

data = pd.concat([data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12],
                 ignore_index=True)
data.to_csv('data/12.csv', index=False, float_format='%.2f', header=None)
print(data)
