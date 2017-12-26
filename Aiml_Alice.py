# -*- coding: utf-8 -*-
#!/usr/bin/env python

# @Time    : 2017/12/4 9:25
# @Author  : tignting.lv
# @Site    : 
# @File    : Aiml_Alice.py
# @Software: PyCharm
#@Contact  : sunfiyes@163.com
import os
import RBCS as aiml
from flask import Flask,render_template,request,redirect,url_for
import sys
import time
from DebugInfo import DebugInfo
import Config as cf
from QuestionDB import Dialog
os.chdir('./alice')
alice = aiml.Kernel()
alice.learn("startup.xml")
alice.match(query='LOAD ALICE')
os.chdir("../")

def strNone(conext):
    if conext.strip() == "" or conext == None:
        conext = cf.DEFAULT_ID
    return conext
def isNone(userId, ownerId, botId):
    userId = strNone(userId)
    ownerId = strNone(ownerId)
    botId = strNone(botId)
    return userId, ownerId, botId
'''Alice对话接口
userId 用户定义Id
ownerId拥有者Id
botId 机器人Id
context 输入的问题
:return参数：
A.context json debug信息
userId 用户Id
ownerId 拥有者Id
botId 机器人Id
history 对话历史记录
response 回复内容
'''
def Alice(userId, ownerId, botId, context):
    if context.strip() == "" or context == None:
        return "输入查询内容不能为空"
    userId, ownerId, botId = isNone(userId, ownerId, botId)
    A = DebugInfo()
    response,debug = alice.match(ownerId, userId, botId, time.asctime(time.localtime(time.time())),"AIML", context.encode("utf-8"))
    session = Dialog()
    A.addInfo(debug)
    session.insert(cf.dialog_table, ownerId, userId, botId, context.encode('utf-8'), response, cf.AIMLTYPE)
    history = session.getDialog(ownerId = ownerId, userId = userId, botId = botId, type= cf.AIMLTYPE)
    return A.context,userId, ownerId, botId, history, response
if __name__ == "__main__":
    strNone("")