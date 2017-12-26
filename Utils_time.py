# -*- coding:utf-8 -*-
import time
import TimeAnlz
import json
import datetime
def getCurrentTime():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

#时间间隔处理
def getVaildTime(vaildtime):
	tn = TimeAnlz.TimeAnlz()
	res = tn.parse(unicode(vaildtime))
	dic = json.loads(res)
	if 'timedelta'  in dic.keys():
		dic = json.loads(res)
		nowTime = dic['timedelta']
		timedelta = nowTime[0].split(", ")
		day = timedelta[0].split(" ")
		day2second = int(day[0]) *24*3600
		sec = timedelta[1].split(":")
		if sec[1] == "00":
			sec[1] = 0
		elif sec[1] == "01":
			sec[1] = 1;
		elif sec[1] == "02":
			sec[1] =2
		elif sec[1] == "03":
			sec[1] = 3
		elif sec[1] == "04":
			sec[1] = 4
		elif sec[1] == "05":
			sec[1] = 5
		elif sec[1] == "06":
			sec[1] = 6
		elif sec[1] == "07":
			sec[1] = 7
		elif sec[1] == "08":
			sec[1] = 8
		elif sec[1] == "09":
			sec[1] = 9
		hour2second = (int(sec[0])*60 + int(sec[1]))*60
		return hour2second + day2second
	return 3600

def isVaild(datetime, validTime):
	try:
		date = time.strptime(datetime, "%Y-%m-%d %H:%M:%S")
		date = int(time.mktime(date))
		cur = int(time.time())
		valid = getVaildTime(validTime)
		if cur - date < valid: #有效期1小时
			return True
		else:
			return False
	except:
		return False

# if __name__ == "__main__":
# 	isVaild("2017-12-26 10:28:00","一小时")

