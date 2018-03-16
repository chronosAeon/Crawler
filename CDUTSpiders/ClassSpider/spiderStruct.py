# -*- coding:utf-8 -*-
import datetime

'''
初始化spider父类框架
'''


class spider():
    '''
        配置私有变量
        url:当前爬取网址
        category:当前爬取栏目类别
        is_print:是否在控制栏打印信息
        crawl_time:本次爬取时间
    '''

    def __init__(self,url,category='', is_Print=True):
        assert url != ''
        self.url = url
        self.category = category
        self.is_Print = is_Print
        self.crawl_time = datetime.datetime.now()
        print(self.crawl_time)

    def __fetch_content(self):
        pass

    def __analysis(self, htmls):
        pass

    def __refine(self, anchors):
        pass

    def __sort(self, anchors):
        pass

    def __sort_seed(self, anchor):
        pass

    def __print_result(self, anchors):
        pass

    def go(self):
        pass
