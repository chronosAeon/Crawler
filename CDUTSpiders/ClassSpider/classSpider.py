# -*- coding:utf-8 -*-
#  from spiderStruct import spider 前面本来应该是对的，但是可能是编译器报错
#  类还有函数的注释写在函数体里面，这点和c#那些语言不一样
import spiderStruct
from urllib import request
import requests
from bs4 import BeautifulSoup
import re
from enum import Enum
from copy import deepcopy
import json
import hashlib
import time


class week_enum(Enum):
    '''
    the enum for a week
    '''
    Monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6
    sunday = 7


class day_class(object):
    '''
    a place to store the class in a day
    '''

    def __init__(self, date, class_dic):
        self.date = date
        self.class_dic = deepcopy(class_dic)

    def convert2_dic__(self):
        return self.class_dic


class classSpider(spiderStruct.spider):
    def __init__(self, semester, stu_number,password,is_update=False):
        self.file_handle = open('class.html', 'w+', encoding='utf-8')
        self.write_file = open('content.txt', 'w', encoding='utf-8')
        assert type(semester) == int, 'please semester is number'
        assert type(stu_number) == int, 'please stu_number is number'
        assert type(is_update) == bool, 'please is_update is number'
        self.semester = semester
        self.stu_number = stu_number
        self.password = password
        '''
        判断是否是要从学校网站上重新爬取数据
        '''
        self.is_update = is_update
        ClASSURL_format = "http://202.115.133.173:805/Classroom/ProductionSchedule/StuProductionSchedule.aspx?termid={}&stuID={}"
        class_schedule = ClASSURL_format.format(*[semester, stu_number])
        super(classSpider, self).__init__(url=class_schedule)

    def go(self):
        token = self.fetch_token()
        if self.is_update:
            '''
            这里选择更新数据就会调用方法获取访问网址获取数据
            这里在访问数据之前先去获取新的token
            '''

            html_str = self.fetch_content(token)
        else:
            '''
            要是不选择更新数据就会读取文件数据到html_str里面
            '''
            html_str = self.file_handle.read()
        crude_data = self.analysis(html_str)
        refined_data = self.handle_data(crude_data)
        self.file_handle.close()
        self.write_file.close()
        return refined_data
    '''
    序列化数据
    '''

    def handle_data(self, data):
        '''
        处理数据,第一个索引是是第几个table，第二个是第几周，第三个是第几天，存贮的是一个天课程对象
        '''
        handled_classdata = []
        for table_index, table in enumerate(data):

            if table_index == 1:
                for week in table:
                    week_data = []
                    # print(week_data)
                    for day_data in week:
                        week_data.append(day_data.class_dic)
                    handled_classdata.append(week_data)
        handled_classDataStr = json.dumps(handled_classdata)
        # print(handled_classDataStr)
        '''
        暂时先只返还课程数据
        '''
        return handled_classDataStr

    def cipherPassword(self, user, timesign, pwd):
        '''
        加密算法
        '''
        # hex_md5(user + sign + hex_md5(pwd.trim()))
        h1 = hashlib.md5()
        pwd = str(pwd).strip()
        h1.update(pwd.encode(encoding='utf-8'))
        md_password = str(h1.hexdigest())
        h2 = hashlib.md5()
        code = str(user)+str(timesign)+md_password
        h2.update(code.encode(encoding='utf-8'))
        password = h2.hexdigest()
        return password



    def fetch_token(self):
        password = self.cipherPassword(self.stu_number,time.time,self.password)
        Token_url = 'http://202.115.133.173:805/Common/Handler/UserLogin.ashx'
        '''
        这里的md5加密最好处理一下，不确定每一个md5算法是不是一样的，所以看是用python的md5
        还是python调用js的md5，但是对面的验证应该都没有问题
        '''
        data = {'Action': 'Login',
                'userName': str(self.stu_number),
                'pwd': 'ef1885f9b5d637f35c93c3d51ca7ab9b',
                'sign': str(time.time)}
        data['pwd'] = password
        ''' 
        session方法自动处理cookie就可以直接拿到token访问第二网站，没试过，可以尝试一下
        '''
        # reqs = requests.session()
        response = requests.post(Token_url, data)
        print('header:'+str(response.headers))
        cookie = response.headers['Set-Cookie']
        print('cookie:'+str(cookie))
        '''
        这里采用正则表达式处理获取token值
        data存贮的sessionId和path两个数据
        '''
        data = re.findall('=(.*?);', cookie)
        print('data:'+str(data))
        '''
        ['0tjnrsihz5avnugw3hww5f3m', '/', '25c6c6a8-927d-42f0-801d-5cccacfd6c39']
        取第三位
        '''
        return data[2]

    def fetch_content(self, token):
        '''
        从固定网站获取数据
        return string html数据
        '''
        cookie_data = 'UserTokeID=' + token
        '''
        这里必须加头部信息，否则服务器内部报错
        '''
        header = {
            'Host': '202.115.133.173:805',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://202.115.133.173:805/SelectCourse/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        header['Cookie'] = cookie_data
        # 'Cookie': 'UserTokeID=bee56ebd-f253-4a98-b313-7934f5c8d7'
        # be729177-f119-4125-8550-e7459a592b22
        # 566964ca-d124-4065-8c4d-b6bf754e00dc
        print(header)
        res = requests.get(self.url, headers=header)
        res.encoding = 'utf-8'
        htmls = res.text
        if self.is_update == True:
            '''
            这里在flask运行是会有错的
            '''
            self.file_handle.write(htmls)
        return htmls

    # @classmethod
    def analysis(self, html_str):
        # html = classSpider.file_handle.read()
        html = html_str
        soup = BeautifulSoup(html, 'lxml')
        soup.encode(encoding='utf-8')
        '''
        找到所有的table标签,按照不同的table标签做出不同的处理
        这里使用字典代替switch,key为索引
        '''
        table_router = {
            0: self.__first_tableHandle,
            1: self.__second_tableHandle,
            2: self.__third_tableHandle
        }
        table_tags = soup.find_all('table')
        '''
        可以用如下方法把生成器变为list
        '''
        table_list = list(table_tags)
        # print(len(table_list))
        tables_data = []
        for table_index, table_tag in enumerate(table_tags):
            tables_data.append(table_router.get(table_index)(table_tag))

        return tables_data

    def __first_tableHandle(self, table_tag):
        return 0

    def __third_tableHandle(self, table_tag):
        return 2
    '''
    params table_tag传入bs4解析完的table_tag
    return 返回二维数组，每周为一个数组存贮每天的类信息
    '''

    def __second_tableHandle(self, table_tag):
        '''

        '''
        '''
        这里开始对每一周的数据进行提取tr，然后就把数据给合适的格式放到mmongodb里面去
        '''
        self.write_file.write('---------------------------'+'\r')
        '''
        tr_tags为每周数据
        '''
        tr_tags = table_tag.find_all('tr')
        all_data = []

        for tr_index, tr_tag in enumerate(tr_tags):
            week_data = []
            day_dic = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None,
                       7: None, 8: None, 9: None, 10: None, 11: None, 12: None}
            # week_list = [day_dic for item in range(12)]
            # week_list[0][1] = 2
            # for item in week_list:
            #     print(item[1])
            # day_date = None
            '''
            课表第二个tr之后才是课
            '''
            if tr_index > 1:
                '''
                td_tags为每节课数据
                '''
                # classSpider.write_file.write(str(tr_index-1)+'周的课\r')
                td_tags = tr_tag.find_all('td')
                '''
                每周有多少结课
                '''
                Aday_td = 12
                '''
                从星期几开始
                '''
                date_counter = 1
                class_counter = 0
                day_date = week_enum.Monday
                '''
                一周的数据遍历
                '''
                for tditem in td_tags:
                    # 标签如果是一个内含标签的话就没办法用string输出内部数据，就会输出Nonetype
                    # if tditem.stripped_strings is not None and tditem.stipped_string is None:
                    if 'align' in tditem.attrs:
                        content = ''
                        # for item_string in tditem.stripped_strings:
                        #     # print(type(item_string))
                        #     classSpider.write_file.write(item_string+'\r')
                        for item_string in tditem.stripped_strings:
                            # classSpider.write_file.write(item_string+'\r')
                            content += item_string+'\r'
                        # print(content)
                        span = int(tditem['colspan'])
                        for pace in range(1, span+1):
                            day_dic[class_counter+pace] = content
                        class_counter += span

                    elif tditem['class'][0] == 'td1':
                        '''
                        去除开头第几周的表格内容
                        '''
                        pass
                    else:
                        '''
                        这里是应该是课名的位置没有课
                        '''
                        content = 'NoClass\r'
                        day_dic[class_counter+1] = content
                        class_counter += 1
                        # classSpider.write_file.write('NoClass'+'\r')
                    '''
                    课程计数器满足一天
                    '''
                    if class_counter >= Aday_td:
                        # classSpider.write_file.write(str(day_dic)+'\r')
                        '''
                        归位课程计数器
                        '''
                        class_counter = 0
                        '''
                        取出当天的日期
                        '''
                        if date_counter < 7:
                            day_date = week_enum(date_counter)
                            '''
                            把每天的数据和当天是星期几封装进类里面
                            '''
                            a_dayData = day_class(day_date, day_dic)
                            '''
                            这是个保留的测试部分，保留是为了提醒你千万别认为for in可以形成作用域
                            for in 里面的变量还有for in 里面遍历的都可以在外面获得
                            这里千万别用a_dayData这个名字，for in 在python3里面并不形成作用域
                            http://blog.cipherc.com/2015/04/25/python_namespace_and_scope/#for
                            '''
                            # for a_dayitem in week_data:
                            #     classSpider.write_file.write(
                            #         str(a_dayitem.class_dic)+'\r')
                            # classSpider.write_file.write(
                            #     '--------------------------------------\r')
                            # classSpider.write_file.write(str(a_dayData.class_dic)+'\r')

                            week_data.append(a_dayData)
                            date_counter += 1
                        elif date_counter == 7:
                            day_date = week_enum(date_counter)
                            '''
                            把每天的数据和当天是星期几封装进类里面
                            '''
                            a_dayData = day_class(day_date, day_dic)
                            week_data.append(a_dayData)
                            all_data.append(week_data)
                            date_counter = 1
                            week_data = []
                        else:
                            '''
                            星期计数器满足一周
                            这里面填写一周结束后的逻辑
                            这个地方可以不用归位，因为这一次做了就不用做了
                            '''
                            date_counter = 1
                            all_data.append(week_data)
        for week in all_data:
            for a_day in week:
                self.write_file.write(str(a_day.class_dic)+'\r')
        return all_data


if __name__ == '__main__':
    Spider = classSpider(201601, 201505090213,'51110219970702201X', is_update=True)
    Spider.go()
    # Spider.cipherPassword('201505090215','1520318555261','510104199705243179')
    # print(Spider.go())
    # classSpider.analysis()
    # file = open('class.html',mode='w',encoding='utf-8')
    # content = Spider.fetch_content()
    # file.write(content)
    # file.close()
