#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/6 10:49
# @Author  : tignting.lv
# @Site    : 
# @File    : AddCustomRules.py
# @Software: PyCharm
#@Contact  : sunfiyes@163.com
import Aiml_Custom
import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
if __name__ == "__main__":
    timeMark = time.asctime(time.localtime(time.time()))
    Aiml_Custom.add_oneCustom("ltt", "ltt", "Alice", "订车票|订票|定票|定车票|车票","订车票")
    Aiml_Custom.add_oneCustom("ltt", "ltt", "Alice", "订餐|定餐|订饭|定饭|定中午饭|订中午饭|", "订餐")
    debug, userId, ownerId, botId, history, response = Aiml_Custom.Custom("ltt","ltt","Alice","订车票我要")
    print (response)
    Aiml_Custom.add_oneCustom("ltt", "ltt", "Alice", "火车|汽车|飞机|轮船", "我要坐汽车")
    debug, userId, ownerId, botId, history, response = Aiml_Custom.Custom("ltt","ltt","Alice","我要坐汽车")
    print (response)
    result =  re.search("火车|汽车|飞机|轮船","我要坐汽车").group()
    print (result.decode('utf-8'))
