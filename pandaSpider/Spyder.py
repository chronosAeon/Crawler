#coding = utf-8
'''
ver 1.0 此版本没办法应对熊猫的highlight栏
改进意见：1.定时器自动抓取数据，并且放到数据库里面
'''
from urllib import request
import re
import time
import datetime
from enum import Enum, unique
import __init__
from DbOperator.Mongo import MongoConn


def printer(func):
    def warp(*arg, **kw):
        print(time.time())
        func(*arg, **kw)
    return warp


@unique
class serie_enum(Enum):
    lol = "lol"
    overwatch = "overwatch"


class spider:
    def __init__(self,url = 'https://www.panda.tv/cate/',serie=serie_enum.lol):
        '''
        配置私有变量
        url:当前爬取网址
        category:当前爬取栏目类别
        is_print:是否在控制栏打印信息
        crawl_time:本次爬取时间
        '''
        self.url = url+serie.value
        self.category = serie.value
        self.is_Print = True
        self.crawl_time = datetime.datetime.now()
    '''
    下面是之前1.0版本没办法支持熊猫highlight栏目是主播的版本
    而且这个版本对于其他的板块也可以使用
    '''

    '''
    获取根数据，包含有highlight的标签也要被提取到
    '''
    # root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    '''
    姓名在hightlight为主播栏目里面的匹配原则是不一样的
    '''
    # name_pattern = ''
    # number_pattern = ''
    # 这个版本熊猫的highlight框没法显示
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<span class="video-number">([\s\S]*?)</span>'

    def __fetch_content(self):
        r = request.urlopen(self.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    def __analysis(self, htmls):
        ResultSlice = re.findall(spider.root_pattern, htmls)
        anchors = []
        for item in ResultSlice:
            name = re.findall(spider.name_pattern, item)
            number = re.findall(spider.number_pattern, item)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        return anchors

    def __refine(self, anchors):
        def solveItem(anchor): return {
            'name': anchor['name'][0].strip(),
            'number': anchor['number'][0]
        }
        return map(solveItem, anchors)

    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        digital = re.findall('^(\d+[.]*\d*)', anchor['number'])
        digital = float(digital[0])
        if '万' in anchor['number']:
            digital = digital*10000
        return digital

    def __print_result(self, anchors):
        for itemNumber in range(0, len(anchors)):
            print(str(itemNumber+1)+'-----------' +
                  anchors[itemNumber]['name']+'------'+anchors[itemNumber]['number'])

    # @printer
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        '''
        是否在控制台打印数据
        '''
        if(self.is_Print == True):
            self.__print_result(anchors)
        '''
        把数据存进mongodb数据库
        '''
        my_conn = MongoConn()
        '''
        字典列表推导式
        '''
        datas = []
        for i in range(0, len(anchors)):
            data = {  
                        'name': anchors[i]['name'],
                        'number':anchors[i]['number'],
                        'catagory':self.category,
                        'time':self.crawl_time
                    }
            datas.append(data)
        my_conn.db['mytest'].insert(datas)
        res = my_conn.db['mytest'].find({})
        for k in res:
            print(k)
        # print(anchors)
        # print(list(anchors)[0])
if __name__ == "__main__":
    spider().go()
