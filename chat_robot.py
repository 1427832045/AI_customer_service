'''
文件描述：基于微信公众号实现AI客服
作者：ljk
邮箱：1427832045@qq.com
时间：2019-6-29 16:05
'''

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import urllib.request
import urllib.parse
import flask
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
import time
import xml.etree.ElementTree as et
import muban
from wechatpy.replies import TextReply
import xmltodict
import pacong1
from random import randint
from lxml import etree
import img
import talk_api
app = flask.Flask(__name__)
def get_robot_reply(question):
    '''
    函数功能：对于特定问题进行特定回复，对于非特定问题进行智能回复
    
    参数描述：
    question 聊天内容或问题

    返回值：str，回复内容
    '''

    if "你名字" in question:
        answer = "我是君哥"
    elif "我还有多少钱" in question:
        answer = "0.09元"
    elif "你多少岁" in question:
        answer = "18"
    elif "你是GG还是MM" in question:
        answer = "你猜呢"
    else:
        try:
            # 调用NLP接口实现智能回复
            params = urllib.parse.urlencode({'msg': question}).encode()  # 接口参数需要进行URL编码
            req = urllib.request.Request("http://api.itmojun.com/chat_robot", params, method="POST")  # 创建请求对象
            answer = urllib.request.urlopen(req).read().decode()  # 调用接口（即向目标服务器发出HTTP请求，并获取服务器的响应数据）
        except Exception as e:
            answer = "AI机器人出现故障！（原因：%s）" % e

    return answer

@app.route("/wx", methods=["GET","POST"])
def weixin_handle():
    token = "xxx"
    signature = flask.request.args.get("signature")
    timestamp = flask.request.args.get("timestamp")
    nonce = flask.request.args.get("nonce")
    echostr = flask.request.args.get("echostr")
    try:
        # 校验签名token
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        flask.abort(403) # 校验token失败，证明这条信息不是微信服务器发过来的
    if flask.request.method == "GET":
        return echostr
    elif flask.request.method == "POST":
        # 表示微信服务器转发消息过来
        xml_str = flask.request.data
        if not xml_str:
            return""
        # 对xml字符串进行解析
        xml_dict = xmltodict.parse(xml_str)
        xml_dict = xml_dict.get("xml")

        # 提取消息类型
        msg_type = xml_dict.get("MsgType")
        msg_Content = xml_dict.get("Content")
        fromUser=xml_dict.get("FromUserName")
        userid = fromUser[0:15]
        if msg_type == "text":
        # 表示发送的是文本消息
        # 构造返回值，经由微信服务器回复给用消息内容
            if "名字" in msg_Content:
                txt = "李金楷"
            elif "编号" in msg_Content:
                txt = "10"
            elif "你们小组成员" in msg_Content:
                txt = "袁海东青(组长) 李金楷 郭炳辰 沈彬 肖龙超 王君豪 杨中凡" 
            elif "你是GG还是MM" in msg_Content:
                txt = "GG"
            elif "你的最爱是谁" in msg_Content:
                txt = "小田田"
#            elif "快递" in msg_Content:
            elif "笑话" in msg_Content:
 #               txt = pacong1.pa()
                url="https://www.qiushibaike.com/text/" 
                print("here1") 
                r = requests.get(url) 
                tree = etree.HTML(r.text) 
                contentlist = tree.xpath('//div[@class="content"]/span/text()') 
                jokes = [] 
                #print("here2",contentlist[0]) 
     
                for i in contentlist: 
     
                    contentstring = ''.join(i) 
                    contentstring = contentstring.strip('\n') 
                    jokes.append(contentstring) 
                #print("here3",jokes) 
                txt = jokes[randint(0, len(jokes))] 
            elif "新闻" in msg_Content:
 #               txt = pacong1.pa()
                b = [] 
                b = pacong1.pa()
                #print("here3",jokes) 
                b = b[randint(0, len(b))]
                txt=''.join(b)
            else:
                try:
                    # 调用NLP接口实现智能回复763e45654321q
                    params = urllib.parse.urlencode({'msg': msg_Content}).encode()  # 接口参数需要进行URL编码
                    req = urllib.request.Request("http://api.itmojun.com/chat_robot", params, method="POST")  # 创建请求对象
                    txt = urllib.request.urlopen(req).read().decode()  # 调用接口（即向目标服务器发出HTTP请求，并获取服务器的响应数据）
                except Exception as e:
                    txt = "AI机器人出现故障！（原因：%s）" % e
            
            resp_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": txt
                    }
            }
            # 将字典转换为xml字符串
            resp_xml_str = xmltodict.unparse(resp_dict)
            # 返回消息数据给微信服务器
            return resp_xml_str
        elif msg_type == 'voice':
            msg_Content = xml_dict.get('Recognition')
            print(msg_Content)
            print(str(msg_Content))
 #           msg = talk_api.talk(msg_Content, userid)
            if "你叫什么名字" in msg_Content:
                txt = "李金楷"
            elif "编号" in msg_Content:
                txt = "10"
            elif "成员" in msg_Content:
                txt = "袁海东青(组长) 李金楷 郭炳辰 沈彬 肖龙超 王君豪 杨中凡" 
            elif "你是GG还是MM" in msg_Content:
                txt = "GG"
            elif "你的最爱是谁" in msg_Content:
                txt = "小田田"
#            elif "快递" in msg_Content:
            elif "笑话" in msg_Content:
 #               txt = pacong1.pa()
                url="https://www.qiushibaike.com/text/" 
                print("here1") 
                r = requests.get(url) 
                tree = etree.HTML(r.text) 
                contentlist = tree.xpath('//div[@class="content"]/span/text()') 
                jokes = [] 
                #print("here2",contentlist[0]) 
     
                for i in contentlist: 
     
                    contentstring = ''.join(i) 
                    contentstring = contentstring.strip('\n') 
                    jokes.append(contentstring) 
                #print("here3",jokes) 
                txt = jokes[randint(0, len(jokes))] 
            elif "新闻" in msg_Content:
 #               txt = pacong1.pa()
                b = [] 
                b = pacong1.pa()
                #print("here3",jokes) 
                b = b[randint(0, len(b))]
                txt=''.join(b)
            else:
                try:
                    # 调用NLP接口实现智能回复763e45654321q
                    params = urllib.parse.urlencode({'msg': msg_Content}).encode()  # 接口参数需要进行URL编码
                    req = urllib.request.Request("http://api.itmojun.com/chat_robot", params, method="POST")  # 创建请求对象
                    txt = urllib.request.urlopen(req).read().decode()  # 调用接口（即向目标服务器发出HTTP请求，并获取服务器的响应数据）
                except Exception as e:
                    txt = "AI机器人出现故障！（原因：%s）" % e


            resp_dict = {
                "xml": {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": txt
                }
            }
            resp_xml_str = xmltodict.unparse(resp_dict)
            # 返回消息数据给微信服务器
            return resp_xml_str
        elif msg_type == 'image':
            picurl = xml_dict.get('PicUrl')
            datas = img.imgtest(picurl)
            txt=''.join(datas)
            print(txt)
            resp_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": txt
                    }
            }
            # 将字典转换为xml字符串
            resp_xml_str = xmltodict.unparse(resp_dict)
            # 返回消息数据给微信服务器
            return resp_xml_str
if __name__ == '__main__':
    # 测试get_robot_reply函数
    # print(get_robot_reply("你叫什么名字"))    
    # print(get_robot_reply("你多少岁"))
    # print(get_robot_reply("武汉明天天气如何"))
    # print(get_robot_reply("你是男是女"))
    # print(get_robot_reply("你到底是谁"))
    app.run(debug=True, host="0.0.0.0", port="80")

    
