# -*- coding:utf-8 -*-
import os
import RBCS as aiml
from CustomDesigns import CustomDesign
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
cd = CustomDesign(verbose=True)
os.chdir('./alice')
alice = aiml.Kernel()
alice.learn("startup.xml")
alice.match(query='LOAD ALICE')
os.chdir("../")
import TimeAnlz
import json
import datetime
def handlleTime(req):
    tn = TimeAnlz.TimeAnlz()
    res = tn.parse(unicode(req))
    dic = json.loads(res)
    if 'N/A' not in dic.keys():
        dic = json.loads(res)
        nowTime = dic[dic['type']]
        timeMark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        d1 = datetime.datetime.strptime(timeMark, '%Y-%m-%d %H:%M:%S')
        print (d1)
        d2 = datetime.datetime.strptime(nowTime, '%Y-%m-%d %H:%M:%S')
        print (d2)
        if d2 >= d1:
            orderTime = "TIME " + nowTime
            return orderTime
        else:
            response = "我不能穿越时间呀"
            return response
    return req
def result(ownerId, userId,botId,input_, timeMark):
    newinput_ = handlleTime(input_)
    if input_ == newinput_:
        response, debug = alice.match(ownerId, userId, botId, timeMark, "AIML", input_)
        return response, debug
    if "TIME" in newinput_:
        response, debug = alice.match(ownerId, userId, botId, timeMark, "AIML", newinput_)
        return response, debug
    else:return newinput_,""
while 1:
    reload(sys)
    sys.setdefaultencoding('utf8')
    input_ = raw_input("INPUT :\t")
    timemark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    info, debug = result("zhangsan","zhangsan","zhangsan",input_,timemark)
    print "Alice :",(info)
    print ("debug information:",(debug))


