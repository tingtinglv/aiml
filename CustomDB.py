# -*- coding:utf-8 -*-
import os
import re
from pymongo.errors import *
from Utils_errors import *
from MongoDB import _mongoDB
import CustomConfig as Config
import Utils_time as time
from DebugInfo import DebugInfo

class CustomDB(object):
	def __init__(self, verbose=False):
		self._verbose = verbose
		if self._verbose:
			A = DebugInfo()
			A.addInfo("Init CustomDB")
			print("Init CustomDB")
		self.ruleColl = Config.basic_ruleColl
		self._filters = {"userID": Config.DEFAULT_ID, "botID": Config.DEFAULT_ID}
		self._proj = {"_id": 0, "ruleID": 1, "matched": 1, "response": 1, "datetime": 1}
		self._sort_by = [("ruleID", -1)]

	def getRules(self, collection, ownerID, userID, botID):
		try:
			self._filters["ownerID"] = ownerID
			self._filters["userID"] = userID
			self._filters["botID"] = botID
			cursor = _mongoDB.search(
				collection,
				self._filters,
				self._proj,
				self._sort_by,
				0
			)
			if not cursor:
				A = DebugInfo()
				A.addInfo("Rule between {0} and {1} is None \n".format(userID, botID))
				print("Rule between {0} and {1} is None ".format(userID, botID))
				return {}
			retV = {}
			for ele in cursor:
				retV[ele["matched"]] = (ele["response"], ele["ruleID"])
			return retV
		except KeyError as e:
			print(e)
			return {}

	def setSingleRule(self, collection, ownerID, userID, botID, matched, response):
		"""
		插入单条规则，成功则返回 1， 存在则返回 0 失败则返回 -1
		:return:
		"""
		try:
			# is exist?
			data = {
				"ownerID": ownerID,
				"userID": userID,
				"botID": botID,
				"matched": matched,
				"response": response
			}
			is_exist = _mongoDB.count(collection, data)
			if is_exist:
				return 0
			self._filters["ownerID"] = ownerID
			self._filters["userID"] = userID
			self._filters["botID"] = botID
			nextidx = _mongoDB.count(collection, self._filters) + 1
			datetime = time.getCurrentTime()
			data["datetime"] = datetime
			data["ruleID"] = nextidx
			if self._verbose:
				A = DebugInfo()
				A.context += ("Insert", data)
				print ("Insert", data)
			result = _mongoDB.insert(collection, data)
			if result:
				return 1
			else:
				return -1
		except PyMongoTimeOutError as e:
			DebugInfo.context += "Custom Design:\n\t MongoDB Error: {0}".format(e)
			print("Custom Design:\n\t MongoDB Error: {0}".format(e))
			return -1
		except Exception as e:
			DebugInfo.context +="Custom Design:\n\t{0}".format(e)
			print ("Custom Design:\n\t{0}".format(e))
			return -1

	def setRuleBatch(self, collection, ownerID, userID, botID, ruleList):
		"""
		:param list: a list of (match, response)
		:return: size of rule List, insert number, Success number , Has number, Error number
		"""
		numS = numH = numE = numA = 0
		try:
			self._filters["ownerID"] = ownerID
			self._filters["userID"] = userID
			self._filters["botID"] = botID
			nextidx = _mongoDB.count(collection, self._filters) + 1
			check = {
				"ownerID": ownerID,
				"userID": userID,
				"botID": botID
			}
			datetime = time.getCurrentTime()
			data = {
				"ownerID": ownerID,
				"userID": userID,
				"botID": botID,
				"datetime": datetime
			}
			# for (matched, response) in ruleList:
			for ele in ruleList:
				matched = ele[0]
				response = ele[1]
				numA += 1
				check["matched"] = matched
				check["response"] = response
				isExist = _mongoDB.count(collection, check)
				if isExist:
					numH += 1
					continue
				data["matched"] = matched
				data["response"] = response
				data["ruleID"] = nextidx
				result = _mongoDB.insert(collection, data)
				if result:
					numS += 1
					try: data.pop("_id")
					except:
						pass
				else:
					numE += 1
					if self._verbose:
					    print ("Fail in inserting the ruleList {0}".format(numA))
				nextidx += 1
		except:
			pass
		finally:
			return len(ruleList), numA, numS, numH, numE

	def setRuleFromFile(self, collection, ownerID, userID, botID, file_name):
		assert (isinstance(file_name, str))
		assert (os.path.isfile(file_name))
		numS = numH = numE = numA = numL = 0
		try:
			self._filters["ownerID"] = ownerID
			self._filters["userID"] = userID
			self._filters["botID"] = botID
			nextidx = _mongoDB.count(collection, self._filters) + 1
			datetime = time.getCurrentTime()
			check = {
				"ownerID": ownerID,
				"userID": userID,
				"botID": botID
			}
			data = {
				"ownerID": ownerID,
				"userID": userID,
				"botID": botID,
				"datetime": datetime
			}
			comment = re.compile('^##')
			with open(file_name, "r") as f:
				for line in f:
					numL += 1
					if isinstance(line, str):
						line = line.decode("GBK")
					if comment.match(line):
						continue
					if "#@#@#@" in line:
						line = line.split("#@#@#@")
					else:
						continue
					numA += 1
					matched, response = line
					matched = re.match(r'^\s*(.*?)\s*$', matched, flags=re.I).group(1)
					response = re.match(r'^\s*(.*?)\s*$', response).group(1)
					# print (u"'{0}'".format(matched))
					# print (u"'{0}'".format(response))
					check["matched"] = matched
					check["response"] = response
					isExit = _mongoDB.count(collection, check)
					if isExit:
						numH += 1
						continue
					data["matched"] = matched
					data["response"] = response
					data["ruleID"] = nextidx
					result = _mongoDB.insert(collection, data)
					if result:
						numS += 1
						try:
							data.pop("_id")
						except:
							pass
					else:
						numE += 1
						if self._verbose: print ("Fail in inserting line: {0}".format(numL))
					nextidx += 1
		except IOError as e:
			print("Error in set rules from file :\n\t", e)
		finally:
			return numA, numS, numH, numE

	def listRule(self, collection, ownerID, userID, botID):
		"""show the Rules matched filter"""
		cursor = _mongoDB.selectCustom(collection, ownerID, userID, botID)
		count = 0
		rev = []
		for ele in cursor:
			# print (ele)
			rev.append(ele)
			count += 1
		print (count)
		return count,rev
if __name__ == "__main__":
	A = CustomDB()
	count, cursor = A.listRule(collection= "user_rule", ownerID= "ltt", userID="ltt", botID="ltt")
	for ele in cursor:
		print (ele)