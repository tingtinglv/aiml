#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/11 18:44
# @Author  : tignting.lv
# @Site    : 
# @File    : DebugInfo.py
# @Software: PyCharm
#@Contact  : sunfiyes@163.com

# 记录debug过程中的信息
class DebugInfo(object):
    context = "debug information....."
    def addInfo(self, cont):
        DebugInfo.context += cont
def A():
    A = DebugInfo()
    A.addInfo("aaaaaaaa")
    print (A.context)

if __name__ == "__main__":

    A()
    A()
    A()
