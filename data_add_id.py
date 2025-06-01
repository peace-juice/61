#   todo 给源数据添加一个id字段
import pandas as pd

data=pd.read_csv('source.csv')

#   todo 增加一列，放在0索引位置，也就是排在第一列
#   第二个参数为字段名   第三个参数是列的值
data.insert(0, 'id', range(1, len(data) + 1))

data.to_csv('ods.csv',header=True,index=False)


