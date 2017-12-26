# -*- coding:utf-8 -*-
question_table = "question"
dialog_table = "dialog"
moduleType = "Custom Design"
AIMLTYPE = "AIML"
CUSTOMTYPE = "CUSTOMTYPE"
TREETYPE = "TREETYPE"
DEFAULT_TITLE = "DEFAULT_TITLE"
DEFAULT_CONTEXT = "DEFAULT_CONTEXT"
DEFAULT_ID = "DEFAULT_ID"
mongodbURL = "127.0.0.1"
mongodbPort = 2222
database = "test"

# 默认user,bot,owner ID
DEFAULT_ID = "DEFAULT_ID"

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