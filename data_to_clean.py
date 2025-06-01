#   todo 本文件为数据的处理清洗
import pandas as pd
from hdfs.client import Client
import pymysql

#   修改pandas的内置参数，让其显示所有的行和列
#   显示所有列数据
pd.set_option('display.max_columns',None)
#   显示所有行数据
pd.set_option('display.max_rows',None)
#   设置value的长度
pd.set_option('max_colwidth',100)
#   设置1000列时才换行
pd.set_option('display.width',1000)


data=pd.read_csv('ods.csv')
# print(data.columns)

#   todo 1.对数据进行去重
print("数据去重前的数量:",len(data))
data.drop_duplicates(inplace=True)
print("数据去重后的数量:",len(data))

#   todo 后面发现number_words字段还存在一个“--”的值，下面把他赛选掉
data=data[data['number_words'] != "--"]

#   todo 2.将小说字数里面的中文去掉
# print(data['number_words'])
data['number_words']=data['number_words'].apply(lambda x: x.split("万")[0])
# print(data['number_words'])


#   todo 3.将小说字数小于1万的用小数代替取两位小数
print(data['number_words'])
data['number_words']=data['number_words'].apply(
    lambda x: round(float(x.split("字")[0]) / 10000,2) if "字" in x else int(x)
)
print(data['number_words'])


#   todo 4.将小说完结状态的值改为数字类型 1为未完结    0为已经完结
data['book_status']=data['book_status'].apply(lambda x:1 if x=="连载" else 0)
print(data['book_status'])

#   todo 5.将性别的值改为数字类型
data['sex']=data['sex'].apply(lambda x: 1 if x=="男" else 0)
print(data['sex'])

#   todo 把数据保存到本地，然后才可以上传hdfs
data.to_csv('dwd.csv',header=True,index=False)


#   todo 下面将数据写入mysql和hdfs
#   todo 把数据写入到hdfs
#   创建一个hdfs的客户端实例(9870是web访问hdfs的端口号)
client=Client('http://192.168.40.110:9870')
#   hdfs上面存储的路径
hdfs_path="/yds/"
#   使用客户端的upload方法将文件上传到hdfs
client.upload(hdfs_path=hdfs_path,local_path='dwd.csv',overwrite=True)
print("处理完的数据已经保存到hdfs,保存的路径为:/yds/dwd.csv........................")


#     将处理好的数据写入mysql
#   建立与mysql的连接
connect=pymysql.connect(host='192.168.40.110',user='root',password='123456',database='yds',charset='utf8')
#   通过连接创建游标对象
cursor=connect.cursor()
#   定义sql如果存在表就删除表(data_processing:数据处理)
drop_table_sql='drop table if exists dwd;'
cursor.execute(drop_table_sql)
#   定义创建表格的sql
CreateTable_sql="""
create table if not exists dwd(
            id int primary key AUTO_INCREMENT,
            name varchar(500),
            info_url varchar(500),
            image_url varchar(500),
            user_name varchar(500),
            user_url varchar(500),
            book_class varchar(500),
            book_status int,
            number_words decimal(10,2),
            jianjie varchar(800),
            chapters varchar(500),
            new_chapters_url varchar(500),
            time varchar(500),
            sex varchar(500)

);
"""
#   执行创建表的语句
cursor.execute(CreateTable_sql)
#   定义插入数据的sql语句
insert_sql="""
    insert into dwd(
         id,name,info_url,image_url,user_name,user_url,book_class,book_status,number_words,jianjie,chapters,new_chapters_url,
         time,sex
    )
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
"""
#   换成list[row]的形式方便写入mysql
data_list=data.values.tolist()
#   执行插入数据
cursor.executemany(insert_sql,data_list)

#   提交任务(只有提交了任务才会执行sql)
connect.commit()
#   关闭游标对象
cursor.close()
#   关闭连接
connect.close()
print("处理完的数据已经保存到mysql的yds数据库的dwd表..............")




