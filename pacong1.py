import urllib.request
import re
from random import randint

def pa():
    url = "http://news.baidu.com/guonei"
    #header参数是一个字典，将爬虫伪装浏览器用户
#    header = {
#        'User-Agent':'User-Agent:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'
#    }
#    req = urllib.request.Request(url,headers=header)
    req = urllib.request.Request(url)
    
    #执行请求获取响应信息
    res = urllib.request.urlopen(req)
    
    # 从响应对象中读取信息并解码
    html = res.read().decode("utf-8")
    #使用正则表达式筛选新闻标题信息
    pat = '<a href="(.*?)" .*? target="_blank">(.*?)</a>'
    
    #获取字符串html中所有匹配的pat，返回一个data的列表
    data = re.findall(pat,html)
#    for news in data:
#        print(news)
    return data
#把列表data 遍历输出结果
#for v in data:
#    print(v[1]+":"+v[0])
pa()


