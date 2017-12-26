# -*- coding: utf-8 -*-
import re
import threading
import os
import copy
import json
import CustomConfig as Config
from CustomDB import CustomDB
import Utils_Format as Format
from Utils_errors import *
from pymongo.errors import *
class CustomDesign(object):
	def __init__(self, collections=Config.basic_ruleColl, verbose=False):
		self._CustomDB = CustomDB()
		self._basic_rule = self._getDefaultRules(collections)
		self._user_rule = {}
		self._CurUserID = None
		self._CurBotID = None
		self._CurOwnerID = None
		self._lock = threading.RLock()
		self._verbose = verbose
		self._rule = {"basic_rule": self._basic_rule}
		self._rule_inf = {
			"user_rule": {"ownerID": Config.DEFAULT_ID, "userID": None, "botID": None},
			"basic_rule": {"ownerID": Config.DEFAULT_ID, "userID": Config.DEFAULT_ID, "botID": Config.DEFAULT_ID}
		}
	def _getDefaultRules(self,collections):
		try:
			rules = self._CustomDB.getRules(collections, Config.DEFAULT_ID, Config.DEFAULT_ID, Config.DEFAULT_ID)
			return rules
		except PyMongoTimeOutError as e:
			print ("Custom Design:\n\tMongoDB Error: {0}".format(e))

	def _learn(self, ownerID, userID, botID, collection):
		if self._CurOwnerID and self._CurOwnerID == ownerID  \
				and self._CurUserID and self._CurUserID == userID \
				and self._CurBotID and self._CurBotID == botID:
			return
		self._CurOwnerID = ownerID
		self._CurUserID = userID
		self._CurBotID = botID
		self._user_rule = self._CustomDB.getRules(collection, ownerID, userID, botID)
		self._rule["user_rule"] = self._user_rule
		if self._verbose:
			print("Get {0} rules".format(len(self._user_rule)))

	def _getResponse(self, matched_list):
		response_list = []
		for rule_type, _rules in self._rule.items():
			for pattern in matched_list[rule_type]:
				response, ruleID = _rules[pattern]
				response_list.append({
					"txt": response,
					"path": "ruleID:" + str(ruleID) + "; matched:" + pattern
				})
		return response_list

	def _match(self, query, ownerID=Config.DEFAULT_ID, userID=Config.DEFAULT_ID, botID=Config.DEFAULT_ID, collection=Config.custom_designColl):

		query = query.decode("utf-8") if isinstance(query, str) else query
		self._learn(ownerID, userID, botID, collection)
		matched_list = {ele: [] for ele in self._rule}
		for rule_type, _rules in self._rule.items():
			for pattern in _rules:
				if self.matchIsRules(pattern, query):
					# retV = self._rule[pattern].encode("utf-8")
					matched_list[rule_type].append(pattern)
		return matched_list

	def matchIsRules(self,pattern, query):
		result = re.search(pattern, query)
		if result == None:
			return False
		return True


	def match(self, ownerid, userid, botid, timemark, moduletype, query):
		self._lock.acquire()
		try:
			if moduletype != Config.moduleType:
				resp_type = Config.resp_type_error
				retV = Format.getFormat(ownerid, userid, botid, timemark, moduletype, query, [], resp_type)
			else:
				matched_list = self._match(query, ownerid, userid, botid)
				response_list = self._getResponse(matched_list)
				retV = Format.getFormat(ownerid, userid, botid, timemark, moduletype, query, response_list,
										Config.resp_success)
			return response_list[0]['txt'],retV
		except PyMongoTimeOutError:
			retV = Format.getFormat(ownerid, userid, botid, timemark, moduletype, query,
									response_type=Config.resp_time_out)
			return response_list[0]['txt'],retV
		except Exception as e:
			print(e)
			result = "no pattern has matched"
			retV = Format.getFormat(ownerid, userid, botid, timemark, moduletype, query,
									response_type=Config.resp_unknow_error, msg=str(e))
			return result,retV
		finally:
			self._lock.release()

	def setSingleRule(self, collection, ownerID, userID, botID, matched, response):
		"""
		添加一条新的规则到 collection
		结果为  0 表示已存在
		结果为  1 表示成功
		结果为 -1 表示出错
		"""
		result = self._CustomDB.setSingleRule(collection, ownerID, userID, botID, matched, response)
		if self._verbose:
			print ("Insert rule result : {0}".format(result))
		return result

	def setRule(self, collection, ownerID, userID, botID, match, response):
		"""
		添加一条新的规则到 collection
		"""
		return self.setSingleRule(collection, ownerID, userID, botID, match, response)

	def setRuleBatch(self, collection, ownerID, userID, botID, ruleList):
		"""
		从 ruleList 批量添加多条规则到collection
		:param ruleList: 形如 [(matched, response)] 的列表
		:return: total number, insert number, Success number , Has number, Error number
		"""
		Tnum, Anum, Snum, Hnum, Enum = self._CustomDB.setRuleBatch(collection, ownerID, userID, botID, ruleList)
		if self._verbose:

			print ("Totally : {0} , insert number : {1} \n"
				"\t Success : {2} \t Exist : {3} \t Error : {4}".format(Tnum, Anum, Snum, Hnum, Enum))
		return Tnum, Anum, Snum, Hnum, Enum

	def setRuleFromFile(self, collection, ownerID, userID, botID, file_name):
		"""
		从文件file_name中获取规则到 colletion
		文件中每行为一条规则
		格式为：
			matched #@#@#@ response
		"""
		assert (isinstance(file_name, str))
		assert (os.path.isfile(file_name))
		Anum, Snum, Hnum, Enum = self._CustomDB.setRuleFromFile(collection, ownerID, userID, botID, file_name)
		if self._verbose:

			print ("Try insert number : {0} \n"
				"\t Success : {1} \t Exist : {2} \t Error : {3}".format(Anum, Snum, Hnum, Enum))
		return Anum, Snum, Hnum, Enum

	def listRule(self, collection, ownerID , userID , botID):
		try:
			count, lst = self._CustomDB.listRule(collection, ownerID, userID, botID)
			ret_lst = []
			# ret_lst.append("count":count)
			# if self._verbose:
			for ele in lst:
				# print (ele)
				ret_lst.append(ele)
			print ("Totally get {0} rules ".format(count))
			return ret_lst
		except PyMongoTimeOutError as e:
			print ("Custom Design:\n\tMongoDB Error: {0}".format(e))
			return None, None
if __name__ == "__main__":
	A= CustomDesign()
	result = A.listRule(collection= "user_rule", ownerID= "ltt", userID="ltt", botID="ltt")
	print ("customeDegin")
	for ele in result:
		print (ele)