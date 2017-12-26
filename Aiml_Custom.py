#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/4 9:32
# @Author  : tignting.lv
# @Site    : 
# @File    : Aiml_Custom.py
# @Software: PyCharm
#@Contact  : sunfiyes@163.com
import os
import sys
import time
from DebugInfo import DebugInfo
from CustomDesigns import CustomDesign
import CustomConfig
from QuestionDB import  Dialog
import Config as cf
from werkzeug.utils import secure_filename
import json
cd = CustomDesign(verbose=True)
'''
Custom 自定义对话
入参：userId 用户Id， ownerId 拥有者Id，botId 机器人Id， context 问题
出参：B.context json debug 信息， userId 用户Id， ownerId 拥有者Id，botId 机器人Id，history 对话历史记录, response 回复内容
'''
def strNone(conext):
    if conext.strip() == "" or conext == None:
        conext = cf.DEFAULT_ID
    return conext
def isNone(userId, ownerId, botId):
    userId = strNone(userId)
    ownerId = strNone(ownerId)
    botId = strNone(botId)
    return userId, ownerId, botId
def Custom(userId, ownerId, botId, context):
    if context.strip() == "" or context == None:
        return "输入查询内容不能为空"
    userId, ownerId, botId = isNone(userId, ownerId, botId)
    B = DebugInfo()
    cd = CustomDesign(verbose=True)
    response, debug = cd.match(ownerid=ownerId, userid=userId, botid=botId,
                               timemark=time.asctime(time.localtime(time.time())), moduletype=cf.moduleType,
                               query=context.encode('utf-8'))
    return response,debug
'''
添加一条自定义规则
入参：
userIdOne 用户Id
ownerIdOne 拥有者Id
botIdOne 机器人Id
matchOne 正则表达式
requestOne 匹配项

出参：
结果为  0 表示已存在
结果为  1 表示成功
结果为 -1 表示出错
'''
def add_oneCustom(userIdOne,ownerIdOne,botIdOne,matchOne,requestOne):
    if matchOne.strip() == "" or matchOne == None:
        return "输入的正则表达式不能为空"
    userIdOne, ownerIdOne, botIdOne = isNone(userIdOne, ownerIdOne, botIdOne)
    result = cd.setSingleRule(CustomConfig.custom_designColl, ownerIdOne, userIdOne, botIdOne, matchOne, requestOne)
    return result
'''
添加多条自定义规则
入参：
userIdMul 用户Id
ownerIdMul 拥有者Id
botIdMul 机器人Id
matchMul  多条正则表达式+匹配项 

出参：
结果为  0 表示已存在
结果为  1 表示成功
结果为 -1 表示出错
'''
def add_MulCustom(userIdMul,ownerIdMul,botIdMul,matchMul):
    if matchMul.strip() == "" or matchMul == None:
        return "输入的匹配规则不能为空"
    userIdMul, ownerIdMul, botIdMul = isNone(userIdMul, ownerIdMul, botIdMul)
    result = cd.setRuleBatch(collection=CustomConfig.custom_designColl,ownerID = ownerIdMul, userID = userIdMul, botID =botIdMul, ruleList =matchMul)
    print (result)
    return result

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['doc', 'file', 'txt'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
'''
文件添加自定义规则
入参：
userIdFile 用户Id
ownerIdFile 拥有者Id
botIdFile 机器人Id
file  文件正则表达式+应答项

出参：
结果为  0 表示已存在
结果为  1 表示成功
结果为 -1 表示出错
'''
def add_FileCustom(userIdFile,ownerIdFile,botIdFile, file):
    if file and allowed_file(file.filename):
        os.chdir('./rules')
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.getcwd(), filename))
        result = cd.setRuleFromFile(collection=CustomConfig.custom_designColl ,ownerID=ownerIdFile, userID= userIdFile, botID= botIdFile, file_name=filename)
    return result