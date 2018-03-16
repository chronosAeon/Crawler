# -*- conding:utf-8 -*-
import threading
import time
import __init__
from pandaSpider.Spyder import spider,serie_enum


def fun_timer():
    # 一天等于多少秒
    DAY_SECONDS = 86400
    for category in serie_enum:
        panda_spider = spider(serie=category.value)
        panda_spider.go()
    global timer
    '''
    一天等于86400秒
    '''
    timer = threading.Timer(DAY_SECONDS,fun_timer)
    timer.start()

if __name__ == '__main__':
    # 开始启动的间隔时间 
    START_INTERVAL = 1
    timer = threading.Timer(START_INTERVAL,fun_timer)
    timer.start()