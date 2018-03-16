#coding = utf-8
import re
from urllib import request as request

def getHtmlContent(url):
    page = request.urlopen(url)
    htmlcontent = page.read()
    htmlcontent = str(htmlcontent,encoding='utf-8')
    return htmlcontent
# pattern = '<span class="comments-count">评论 32</span>'
pattern ='<span class="comments-count">评论 32</span>'
content = getHtmlContent('https://www.jianshu.com/p/77a2e09b5285')
result = re.findall('评论 32',content)
index2 = content.index("span")
file = open('html.txt','w',encoding='utf-8')
file.write(content)
print(content)
print(result)
print(index2)