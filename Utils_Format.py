# -*- coding utf-8 -*-
import json
import Config


def getFormat(
		ownerid, userid, botid, timemark, moduletype, query,
		response=[],
		response_type=Config.resp_unknow_error,
		msg=None
):
	query = query.decode("utf-8") if isinstance(query, str) else query
	retV = {}
	retV["moduleType"] = moduletype
	retV["timeMark"] = timemark
	retV["query"] = query
	retV["userID"] = userid if userid else Config.DEFAULT_ID
	retV["botID"] = botid if botid else Config.DEFAULT_ID
	retV["ownerID"] = ownerid if ownerid else Config.DEFAULT_ID
	retV["response"] = {}
	if response_type == Config.resp_success:
		if len(response) == 0:
			retV["code"] = Config.response_type[Config.resp_no_found]["code"]
			retV["msg"] = Config.response_type[Config.resp_no_found]["msg"]
		else:
			for idx, ele in enumerate(response):
				retV["response"]["res"+str(idx)] = ele
	else:
		retV["code"] = Config.response_type[response_type]["code"]
		retV["msg"] = msg if msg else Config.response_type[response_type]["msg"]
	retV = json.dumps(retV, ensure_ascii=False)
	return retV