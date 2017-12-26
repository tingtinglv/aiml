# -*- coding: utf-8 -*-
import requests
import urllib
import json
import datetime
import time
try: import urllib2
except:
	pass
# API processors
class APIProcessors(object):
	def __init__(self):
		# set up processor type
		self._Processor = {
			"http"      : {
				"tuling"    :   self._requestTuLing,
				"ourchat"   :   self._requestOurChat,
				"chat": self._requestChat
				},
			"database"  : {
				"None"      : self._requestDB
				}
		}

		# set the url corresponding the API name
		self._requestURL = {
			"tuling"            : "http://www.tuling123.com/openapi/api",
			"ourchat"           : "http://192.168.100.202:9066",
			"chat": "http://192.168.100.202:9066"
			}

		# responseParser
		self._ResponseParser = {
			"tuling"            : self._tulingParser,
			"ourchat"           :self._ourChatParser,
			"chat": self._ourChatParser
			}

	# 不同 API 的处理

	# http 请求的处理
	# tuling
	def _requestTuLing(self, name, attrs, req):
		""" handle the request to tuling """
		# build and send request
		try:
			url = self._requestURL[name]
			key = attrs['key'].encode('utf-8') if 'key' in attrs else "8190486186fc431f8a5edaad91fd02a5"
			userid = attrs['userid'] if 'userid' in attrs else 0
			params = {
				'key': key,
				'info': req.encode('utf-8'),
				'userid': userid
			}

			try:
				response = urllib.request.urlopen(url=url, data=urllib.urlencode(params))
			except:
				try:
					response = urllib2.urlopen(url=url, data=urllib.urlencode(params))
				except:
					raise "urllib module ERROR"
		except KeyError:
			raise "No found the URL of {0} ".format(name)
		except Exception, ex:
			raise ex

		# handle the response
		try: retV = self._ResponseParser[name](response)
		except KeyError:
			raise "No found the response parser of {0}".format(name)
		except Exception, ex:
			raise ex

		return retV

	def handlleTime(self, req):
		tn = TimeConvert(isPreferFuture=True)
		res = tn.parse(unicode(req))
		dic = json.loads(res)
		if 'error' not in dic.keys():
			dic = json.loads(res)
			nowTime = dic[dic['type']]
			timeMark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
			d1 = datetime.datetime.strptime(timeMark, '%Y-%m-%d %H:%M:%S')
			d2 = datetime.datetime.strptime(nowTime, '%Y-%m-%d %H:%M:%S')
			if d2 >= d1:
				orderTime = "TIME " + nowTime
				return orderTime
			else:
				response = "我不能穿越时间呀"
				return response
		return req
	# http 请求的处理
	# ourChat
	def _requestChat(self, name, attrs, req):
		""" handle the request to our_chating"""
		result = self.handlleTime(req)
		if result == req:
			# build and send request
			try:
				url = self._requestURL[name]
				param = {}
				param['query'] = req
				try:
					response = requests.post(url=url, data=json.dumps(param))
				except:
					try:
						response = urllib2.urlopen(url=url, data=urllib.urlencode(param))
					except:
						raise "urllib module ERROR"
			except KeyError:
				raise "No found the URL of {0} ".format(name)
			except Exception, ex:
				raise ex
			# handle the response
			try:
				retV = self._ResponseParser[name](response)
			except KeyError:
				raise "No found the response parser of {0}".format(name)
			except Exception, ex:
				raise ex
			return retV

		return result

	def _requestOurChat(self, name, attrs, req):
		""" handle the request to our_chating"""
		# build and send request
		try:
			url = self._requestURL[name]
			param = {}
			param['query'] = req
			try:
				response = requests.post(url=url, data=json.dumps(param))
			except:
				try:
					response = urllib2.urlopen(url=url, data=urllib.urlencode(param))
				except:
					raise "urllib module ERROR"
		except KeyError:
			raise "No found the URL of {0} ".format(name)
		except Exception, ex:
			raise ex

		# handle the response
		try:
			retV = self._ResponseParser[name](response)
		except KeyError:
			raise "No found the response parser of {0}".format(name)
		except Exception, ex:
			raise ex

		return retV
	# database 请求的处理
	def _requestDB(self, name, attr, req):
		"""handle the request to database"""
		pass


	# http响应解析
	# tuling
	def _tulingParser(self, response):
		response = response.read()
		src = json.loads(response)
		code = src["code"]
		retV = ""
		if code == 100000:
			return src["text"]
		elif code == 200000:
			# data with url
			retV += src["text"] + "\n\t" + src["url"]
			return retV
		elif code == 302000:
			# news
			retV += src["text"] + "\n\n\t\t"
			lst = src["list"]
			for ele in lst:
				tmp = ""
				tmp += ele["article"] + "\n\t\t"
				tmp += ele["detailurl"] + "\n\n\t\t"
				retV += tmp
			return retV
		elif code == 308000:
			retV += src["text"] + "\n\n\t\t"
			lst = src["list"]
			for ele in lst:
				tmp = ""
				tmp += ele["name"] + "\n\t\t"
				tmp += ele["info"] + "\n\t\t"
				tmp += ele["detailurl"] + "\n\n\t\t"
				retV += tmp
			return retV
		else:
			return "= ="

	def __call__(self, APIType, APIName, APIExAttr, APIReq):
		try:
			return self._Processor[APIType][APIName](APIName, APIExAttr, APIReq)
		except KeyError:
			raise "No found the processor of ({0}:{1})".format(APIType, APIName)
		except Exception, ex:
			raise ex
	# http响应解析
			# ourChating
	def _ourChatParser(self, response):
		code = response.status_code
		retV = ""
		if code == 200:
			# data with url
			retV = response.json()["answer"]
			return retV
		else:
			return "= ="
