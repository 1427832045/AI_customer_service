#!/user/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse

def report(question):
    '''
    函数功能：对于特定问题进行特定回复，对于其他非特定问题进行智能回复

    参数描述：
    question： 聊天内容或问题

    返回值： 回复内容
    '''
    if '你好' in question:
        answer = "你好"
    elif '我喜欢你' in question:
        answer = "嘻嘻我也喜欢你哦"
    elif '你在干什么呀' in question:
        answer = "我在想你呀"
    else:
        try:
        # 调用NLP接口实现智能回复
            params = urllib.parse.urlencode({'msg': question}).encode()  # 接口参数需要进行URL编码
            req = urllib.request.Request("http://api.itmojun.com/chat_robot",params,method = "POST")  # 创建请求
            answer = urllib.request.urlopen(req).read().decode()  # 调用接口(即像目标服务器发出HTTP请求)
        except Exception as e:
            answer = "AI机器人出现故障!(原因：%s)" %e
    return answer

if __name__ == '__main__':
    # 测试
    a = True
    print("输入你想说的话,想结束输入就输入结束\n")
    while(a):
        i = input("")
        b = report(i)
        print(b)
