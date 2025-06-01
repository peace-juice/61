from flask import Flask,render_template,jsonify
from flask_cors import CORS
import pymysql

#       初始化flask
app=Flask(__name__)
#   允许与浏览器共享服务器资源
CORS(app)



#   定义获取mysql里面数据的方法
def get_data(sql):
    #   建立与mysql的连接
    connect=pymysql.connect(host='192.168.40.110',user='root',password='123456',database='yds',charset='utf8')
    #   创建游标对象
    cursor=connect.cursor()
    #   执行sql语句，返回数据
    cursor.execute(sql)
    #   fetchall()函数返回一个列表。列表里面是元组，每一个元组是一行数据
    data=cursor.fetchall()
    #   存储转换成字典格式的数据
    data_dict=[]
    #   处理数据的格式
    for x in data:
        #   todo 得到数据存在三个字段
        if len(x)==3:
            data_dict.append(
                {
                    "x":x[0],
                    "y":x[1],
                    "z":x[2]
                }
            )
        #   todo 数据只有两个字段
        else:
            #   todo 词云图要求的key必须是name   值必须是value
            data_dict.append(
                {
                    "name":x[0],
                    "value":x[1]
                }
            )
    #   将数据返回
    return data_dict

#   todo 图1:每种小说类型的数量
data1=get_data('select * from yds.r1  ')
#   todo 图2:小说完结和未完结的占比图
data2=get_data('select * from r2')
#   todo 图3:每种类型的小说的平均字数
data3=get_data('select * from r3 order by avg_number desc limit 10')
#   todo 图4：用户总字数Top10
data4=get_data('select user_name,round(number) as number from r4')
#   todo 图5:男生看的小说类型的词云图
data5=get_data('select * from r5')
#   todo 图6:女生看的小说的类型的半环形图
data6=get_data('select * from r6')

#   定义浏览器输入url跳转到可视化大屏
#   todo Flask 的装饰器，用于定义 URL 路由规则。 输入http://0.0.0.0:5000/即可触发下面的index函数
@app.route('/')

def index():
    return render_template(
        #   todo 渲染指定的 HTML 模板并传递数据。
        #   todo 右侧是python里面的变量，左边的data1是html里面的变量
        '可视化大屏展示.html',data1=data1,data2=data2,data3=data3,data4=data4,
        data5=data5,data6=data6
    )



#   启动flask渲染
#   在浏览器输入:   http://127.0.0.1:5000/访问可视化大屏
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=8088)
