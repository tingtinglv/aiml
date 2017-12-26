#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 11:45
# @Author  : tignting.lv
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
#@Contact  : sunfiyes@163.com

str = "0||selection||0||[2,5]||[(2||selection||1||[0,1]||[(6||selection||2||[]||[]),(4||selection||3||[]||[])]),(1||condition||4||[0,1]||[(7||selection||5||[]||[]),(3||selection||6||[3,4]||[(6||selection||7||[]||[]),(5||selection||8||[]||[])])])]"
str1 = str[1:-1]
str2 = str1.split("||", 4)
print (str1)
print (str2)







