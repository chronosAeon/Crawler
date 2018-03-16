# -*-coding:utf-8 -*-
from flask import Flask
import __init__
from pandaSpider.Spyder import spider, serie_enum
from CDUTSpiders.ClassSpider.classSpider import classSpider
app = Flask(__name__)

'''
获取学习到的数据或者数据库里面的数据进行反馈
'''
@app.route('/')
def index():
    return 'pleasing to come to my datacollector'

@app.route('/pandas')
def pandas():
    pandaSpy = spider(serie=serie_enum.overwatch)
    pandaSpy.go()
    return "ok"

@app.route('/curriculum')
def curriculum():
     Spider = classSpider(201702, 201505090215,False)
     response = Spider.go()
    #  print(response)
     return response


if __name__ == "__main__":
    app.debug = True
    app.run()
