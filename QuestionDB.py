#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/12 15:03
# @Author  : tignting.lv
# @Site    : 
# @File    : QuestionDB.py
# @Software: PyCharm
#@Contact  : sunfiyes@163.com
from DebugInfo import DebugInfo
import Config as cf
from MongoDB import _mongoDB
import time
from Utils_errors import *
######记录历史对话内容，用于前端页面显示
class Dialog:
    def __init__(self, verbose=False):
        self._verbose = verbose
        if self._verbose:
            A = DebugInfo()
            A.addInfo("Add dialog")
            print("Add dialog")
        self.question = cf.question_table
        self._filters = {"ownerId": cf.DEFAULT_ID, "userId": cf.DEFAULT_ID, "botId":cf.DEFAULT_ID, "dialog_context":cf.DEFAULT_CONTEXT, "dialog_answer":cf.DEFAULT_CONTEXT, "type":cf.AIMLTYPE}
        self._proj = {"_id": 0, "ownerId": 1, "userId": 1,"botId": 1, "dialog_context":1, "dialog_answer":1,  "create_time": 1, "type":1}
        self._sort_by = [("create_time", -1)]
    def insert(self, collection, ownerId, userId, botId, dialog_context, dialog_answer, type):
        try:
            if ownerId ==None or ownerId == "":
                ownerId = cf.DEFAULT_ID
            if userId == None or userId == "":
                userId = cf.DEFAULT_ID
            if botId == None or botId == "":
                botId = cf.DEFAULT_ID
            if type == None or type == "":
                type = cf.AIMLTYPE
            data = {
                "ownerId": ownerId,
                "userId": userId,
                "botId":botId,
                "dialog_context":dialog_context,
                "dialog_answer":dialog_answer,
                "type":type
            }
            datetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            data["create_time"] = datetime
            if self._verbose:
                A = DebugInfo()
                A.context += ("Insert", data)
                print ("Insert", data)
            result = _mongoDB.insert(collection, data)
            if result:
                return 1
            else:
                return -1
        except PyMongoTimeOutError as e:
            DebugInfo.context += " dialog:\n\t MongoDB Error: {0}".format(e)
            print("dialog:\n\t MongoDB Error: {0}".format(e))
            return -1
        except Exception as e:
            DebugInfo.context += "dialog:\n\t{0}".format(e)
            print ("dialog:\n\t{0}".format(e))
            return -1

    def getDialog(self, ownerId, userId, botId, type):
        try:
            cursor = _mongoDB.selectDialog(ownerId,userId,botId,type,collection=cf.dialog_table)
            if not cursor:
                return u""
            return cursor
        except KeyError:
            retV = u""
            return retV

if __name__ == "__main__":
    A = Dialog()
    cursor = A.getDialog( "ljj", "ltt","ljj", type="AIML")
    for e in cursor:
        print e
