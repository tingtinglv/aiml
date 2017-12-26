#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/7 17:58
# @Author  : tignting.lv
# @Site    : 
# @File    : views.py
# @Software: PyCharm
#@Contact  : sunfiyes@163.com
# -*- coding:utf-8 -*-
import os
import RBCS as aiml
from flask import Flask,render_template,request,redirect,url_for
import sys
import time
from DebugInfo import DebugInfo
import Config as cf
from QuestionDB import Dialog
from Aiml_result import *
import json
app = Flask(__name__)
# app.config['DEBUG'] = True
# app.debug = True
reload(sys)
sys.setdefaultencoding('utf-8')
flag = True
userId = cf.DEFAULT_ID
ownerId = cf.DEFAULT_ID
botId = cf.DEFAULT_ID
#-------------------------------Alice aiml部分---------------------------------------------------
@app.route("/")
def alice():
    return render_template('alice.html',yx_aiml=None,userId = userId, ownerId = ownerId, botId = botId)

@app.route('/getId',methods=['POST'])
def getId():
    global userId
    global ownerId
    global botId
    user = request.form.get("userId")
    bot = request.form.get("botId")
    owner = request.form.get("ownerId")
    if user == "" or user == None:
        user = cf.DEFAULT_ID
    if owner == "" or owner == None:
        owner = cf.DEFAULT_ID
    if bot == "" or bot == None:
        bot = cf.DEFAULT_ID
    userId = user
    ownerId = owner
    botId = bot
    return render_template('alice.html',yx_aiml = None, userId = userId, ownerId = ownerId, botId = botId)
@app.route('/alice_detail/',methods=['POST'])
def alice_detail():
    global userId
    global ownerId
    global botId
    A = DebugInfo()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    context = request.form.get("context")
    if context == None or context == "":
        return redirect(url_for('alice'))
    timemark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    response, debug = result(ownerId, userId, botId,context.encode("utf-8"), timemark)
    A.addInfo(debug)
    session = Dialog()
    session.insert(cf.dialog_table, ownerId, userId, botId, context.encode('utf-8'), response, cf.AIMLTYPE)
    history = session.getDialog(ownerId=ownerId, userId=userId, botId=botId, type=cf.AIMLTYPE)
    return render_template('alice.html', history=history, yx_aiml=A.context, userId=userId, ownerId=ownerId,
                           botId=botId)
#---------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    os.chdir('./alice')
    alice = aiml.Kernel()
    alice.learn("startup.xml")
    alice.match(query='LOAD ALICE')
    os.chdir("../")
    app.run(
        host= '0.0.0.0',
        port='5002',
    )
