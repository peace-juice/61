import pymysql
import pandas as pd


data=pd.read_csv('source.csv')


#     将处理好的数据写入mysql
#   建立与mysql的连接
connect=pymysql.connect(host='192.168.40.110',user='root',password='123456',database='datas',charset='utf8')
#   通过连接创建游标对象
cursor=connect.cursor()
#   定义sql如果存在表就删除表
drop_table_sql='drop table if exists source;'
cursor.execute(drop_table_sql)
#   定义创建表格的sql
CreateTable_sql="""
create table if not exists source(
            id int primary key AUTO_INCREMENT,
            name varchar(500),
            info_url varchar(500),
            image_url varchar(500),
            user_name varchar(500),
            user_url varchar(500),
            book_class varchar(500),
            book_status varchar(500),
            number_words varchar(500),
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
    insert into source(
         name,info_url,image_url,user_name,user_url,book_class,book_status,number_words,jianjie,chapters,new_chapters_url,
         time,sex
    )
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
print("数据已经保存到mysql..............")