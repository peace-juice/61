#   todo 本文件将爬取到的源数据上传到hdfs
from hdfs.client import Client

#   创建一个hdfs的客户端实例(9870是web端访问hdfs的端口号)
client=Client('http://192.168.40.110:9870')

#   hdfs上面存储的路径
hdfs_path="/yds/"

#   使用客户端的upload方法将文件上传到hdfs
client.upload(hdfs_path=hdfs_path,local_path='ods.csv',overwrite=True)




