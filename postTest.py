#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/11 14:31
# @Author  : tignting.lv
# @Site    : 
# @File    : postTest.py
# @Software: PyCharm
#@Contact  : sunfiyes@163.com

# !/usr/bin/env python3
# *--coding=utf-8--*
import requests
import sys
import os
import json
import time
import hashlib
import random
import threading


def nonce_gen(n):
    seed = "1234567890abcdefghijklmnopqrstuvwxyz"
    sa = []
    for i in range(n):
        sa.append(random.choice(seed))
        salt = ''.join(sa)
    return salt


def sign_gen(src):
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    #    print("md5",m2.hexdigest().upper())
    return m2.hexdigest().upper()


def qizhi_chat():
    global input_, result
    src = input_
    url = "https://api.smartnlp.cn/cloud/robot/57b7106f1a0000c8cd3e4cc7/answer"
    param = {}
    param['q'] = src
    r = requests.get(url=url, params=param)
    #  print(r.json())
    #   print('Qizhi:\t',r.json()["answers"][0]["respond"])
    #   print("="*30)
    result['Qizhi'] = "\t%s\n%s" % (r.json()["answers"][0]["respond"], "=" * 30)
    return r.json()["answers"][0]["respond"]


def tuling_chat():
    global input_, result
    src = input_
    url = "http://www.tuling123.com/openapi/api"
    sk = "4f0605167fa572d485015227e6e122af"
    param = {}
    param['key'] = sk
    param['info'] = src
    param['userid'] = 'user1'
    r = requests.post(url, data=param)
    #    print(r.json())
    #    print('Tuling:\t',r.json()["text"])
    #    print("="*30)
    result['Tuling'] = "\t%s\n%s" % (r.json()["text"], "=" * 30)
    return r.json()["text"]


def our_chat():
    global input_, result
    src = input_
    url = "http://192.168.100.202:9066"
    param = {}
    param['query'] = src
    r = requests.post(url=url, data=json.dumps(param))
    # print('Our:\t',r.json()["answer"])
    # print("="*30)
    result['Our'] = "\t%s\n%s" % (r.json()["answer"], "=" * 30)
    return r.json()["answer"]


def diting_chat():
    global input_, result
    src = input_
    url = 'http://www.ditingai.com/remote/chat/info'
    param = {}
    param["uuid"] = nonce_gen(5)
    param["question"] = src
    param["username"] = "18646048336"
    r = requests.post(url=url, data=json.dumps(param))
    # print('Diting:\t',r.json()["answer"])
    # print("="*30)
    result['Diting'] = "\t%s\n%s" % (r.json()["answer"], "=" * 30)
    return r.json()["answer"]

if __name__ == '__main__':
    result = {}

    while 1:
       input_ = raw_input("INPUT :\t")
       print('Qizhi:',qizhi_chat())
       print("="*30)
       print('Tuling:',tuling_chat())
       print("="*30)
       print('Diting:',diting_chat())
       print("="*30)
       print('our:',our_chat())
       print("="*30)
