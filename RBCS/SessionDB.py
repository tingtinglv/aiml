# -*- coding:utf-8 -*-

from MongoDB import _mongoDB
import Utils_time as time
import copy
import AimlConfig

class SessionDB(object):
	def __init__(self, verbose=True):
		# connect = MongoClient(url, port)
		# self._database = connect[database_name]
		self._verbose = verbose
		self._CurOwnerID = None
		self._CurUserID = None
		self._CurBotID = None
		self._History = None
		self.nextidx = 0
		self.varColl = AimlConfig.varColl
		self.historyColl = AimlConfig.historyColl
		# 添加表查询参数
		self._filter_list = {
			self.historyColl: {
				"ownerID": AimlConfig.DEFAULT_ID,
				"userID": AimlConfig.DEFAULT_ID,
				"botID": AimlConfig.DEFAULT_ID
			},
			self.varColl: {
				"ownerID": AimlConfig.DEFAULT_ID,
				"userID": AimlConfig.DEFAULT_ID,
				"botID": AimlConfig.DEFAULT_ID,
				"name": ""
			}
		}
		self._proj_list = {
			self.historyColl: {"_id": 0, "inputHistory": 1, "outputHistory": 1, "idx": 1},
			self.varColl: {"_id": 0}
		}
		self._sort_by ={
			self.historyColl: [("idx", -1)],
			self.varColl: [("datetime", -1), ("2idx", -1)]
		}

	def getHistoryFromDB(self, ownerID, userID, botID, collection=AimlConfig.historyColl, limit=10):
		# 判断是否是当前缓存的session .是则不查询数据库

		if self._CurOwnerID and self._CurOwnerID == ownerID \
				and self._CurUserID and self._CurUserID == userID \
				and self._CurBotID and self._CurBotID == botID:
			return
		self._History = {"inputHistory": [], "outputHistory": [], "inputStack": []}
		self._CurOwnerID = ownerID
		self._CurUserID = userID
		self._CurBotID = botID
		self.nextidx = 0

		self._filter_list[self.historyColl]["ownerID"] = ownerID
		self._filter_list[self.historyColl]["userID"] = userID
		self._filter_list[self.historyColl]["botID"] = botID
		cursor = _mongoDB.search(
			collection,
			self._filter_list[self.historyColl],
			self._proj_list[self.historyColl],
			self._sort_by[self.historyColl],
			limit
		)
		if not cursor:
			return
		if self._verbose:
			print("Find Result : {0}".format(cursor.count()))

		for ele in cursor.sort("idx", 1):
			if self._verbose:
				print("ele : {0}".format(ele))
			self.nextidx = ele["idx"] + 1
			self._History["inputHistory"].append(ele["inputHistory"])
			self._History["outputHistory"].append(ele["outputHistory"])

	def getHistory(self, type):
		try:
			return self._History[type]
		except KeyError:
			print("No Key {0} in History session".format(type))

	def setInputHistory(self, inputHistory):
		self._History["inputHistory"] = inputHistory

	def setInputStack(self, inputStack):
		self._History["inputStack"] = inputStack

	def setOutputHistory(self, outputHistory, collection=AimlConfig.historyColl):
		self._History["outputHistory"] = outputHistory

		# make a new history data
		datetime = time.getCurrentTime()
		newInput = self._History["inputHistory"][-1]
		newOutput = self._History["outputHistory"][-1]
		if(newInput == "LOAD ALICE"):
			print ("load alice 不是对话内容")
			return
		datas = {"ownerID": self._CurOwnerID, "userID": self._CurUserID, "botID": self._CurBotID,
				"inputHistory": newInput, "outputHistory": newOutput,
				"idx": self.nextidx, "datetime": datetime}
		result = _mongoDB.insert(collection, datas)
		if self._verbose:
			if result:
				print("Insert History Result:\n\t {0}".format(result))
			else:
				print("Fail in inserting aiml history into mongoDB")
		if result:
			self.nextidx += 1

	def addSession(self, sessionID="DEFAULT_ID"):
		""" deprecated  """
		if self._verbose:
			print("Get session with ID : {0}".format(sessionID))

		if self._collection.count({"id": sessionID}) == 0:
			if self._verbose:
				print("Add a new session with ID : {0}".format(sessionID))
			tmpHistory = copy.deepcopy(AimlConfig.empty_history)
			tmpHistory["id"] = sessionID
			self._collection.insert_one(tmpHistory)

	def getPredicate(self, name, filename,ownerID, userID, botID, collection=AimlConfig.varColl):
		if self._verbose:
			try:
				name = name.encode("utf-8")
				ownerID = ownerID.encode("utf-8")
				userID = userID.encode("utf-8")
				botID = botID.encode("utf-8")
			except:
				pass
			try:
				print("Get data '{0}' from ({1} : ({2} : {3}))".format(name, ownerID, userID, botID))
			except:
				pass
		try:
			self._filter_list[self.varColl]["ownerID"] = ownerID
			self._filter_list[self.varColl]["userID"] = userID
			self._filter_list[self.varColl]["botID"] = botID
			self._filter_list[self.varColl]["name"] = name
			self._filter_list[self.varColl]["filename"] = filename
			cursor = _mongoDB.search(
				collection,
				self._filter_list[self.varColl],
				self._proj_list[self.varColl],
				self._sort_by[self.varColl],
				1
			)
			if not cursor:
				return u""
			result = cursor[0]
			# 判断变量有效性。这里直接依据在同个小时内发的有效，之后可自行定义
			# now_time = time.getCurrentTime()
			var_time = result["datetime"].encode("utf-8")
			try:
				validTime = result["vaildTime"].encode("utf-8")
			except KeyError:
				validTime = "一小时"
			if time.isVaild(var_time,validTime):
				retV = result["value"].encode("utf-8")
				if name == "topic":
					if result["state"] == 1:
						retV = ""
		except KeyError:
			retV = u""
			return retV
		if self._verbose:
			print("Data '{0}' : {1}".format(name, retV))
		return retV.decode("utf-8")

	def setPredicate(self, name, value, filename,ownerID ,userID, botID, vaildTime = AimlConfig.valitime,collection=AimlConfig.varColl):
		if self._verbose:
			try:
				name = name.encode("utf-8")
				if name == "topic":
					state = AimlConfig.dialog_state
				value = value.encode("utf-8")
				ownerID = ownerID.encode("utf-8")
				userID = userID.encode("utf-8")
				botID = botID.encode("utf-8")
			except:
				pass
			try:
				print("Set {0}: {1} in session ({2} :({3} : {4}))".format(name, value, ownerID, userID, botID))
			except:
				pass
		# make a new var
		# if value == "None" or value == "":
		# 	return
		datetime = time.getCurrentTime()
		if name == "topic":
			data = {"ownerID": ownerID, "userID": userID, "botID": botID,
					"name": name, "value": value, "filename": filename,"state":AimlConfig.dialog_state,
					"2idx": self.nextidx, "datetime": datetime, "vaildTime": vaildTime}
		else:
			data = {"ownerID": ownerID, "userID": userID, "botID": botID,
				"name": name, "value": value,"filename":filename,
				"2idx": self.nextidx, "datetime": datetime, "vaildTime":vaildTime}
		result = _mongoDB.insert(collection, data)
		if self._verbose:
			print(result)

	def setDialogState(self, ownerID ,userID, botID,query,response,filename, state,collection = AimlConfig.stateColl):
		if query == "LOAD ALICE":
			return
		if self._verbose:
			try:
				query = query.encode("utf-8")
				response = response.encode("utf-8")
				ownerID = ownerID.encode("utf-8")
				userID = userID.encode("utf-8")
				botID = botID.encode("utf-8")
			except:
				pass
			try:
				print("Set {0}: {1} in session ({2} :({3} : {4}))".format(query, response, ownerID, userID, botID))
			except:
				pass
		datetime = time.getCurrentTime()
		data = {"ownerID": ownerID, "userID": userID, "botID": botID,
				"query": query, "response": response,
				"state":state , "filename":filename,"datetime": datetime}
		result = _mongoDB.insert(collection, data)
		if self._verbose:
			print(result)


	def deleteSession(self, sessionID, collection=AimlConfig.historyColl):
		""" deprecated  """


	def getSessionData(self,sessionID="DEFAULT_ID"):
		""" deprecated  """
