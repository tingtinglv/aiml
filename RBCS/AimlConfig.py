# -*- coding:utf-8 -*-
from Config import *
DEFAULT_ID = "DEFAULT_ID"
empty_history = {
    "userID": DEFAULT_ID,
    "botID": DEFAULT_ID,
    "inputHistory": "",
    "outputHistory": "",
    "datatime": "",
    "idx": "",
}
#记录对话状态，完成为1，未完成为0，默认未完成
dialog_state = 0
moduletype = "AIML"
valitime = "一小时"
# MongoDB collections name
historyColl = "history"
varColl = "vars"
stateColl = "state"
# response type
resp_success = "SUCCESS"
resp_time_out = "TIME OUT"
resp_no_found = "NO FOUND"
resp_type_error = "TYPE ERROR"
resp_unknow_error = "UNKNOW"
response_type = {
    resp_success: {
        "code": 200,
        "msg": "OK"
    },
    resp_time_out: {
        "code": 500,
        "msg": "MongoDB Connect Time Out"
    },
    resp_no_found: {
        "code": 404,
        "msg": "No found"
    },
    resp_type_error: {
        "code": 304,
        "msg": "Module type Error"
    },
    resp_unknow_error: {
        "code": 0,
        "msg": ""
    }
}
