# -*- coding:utf-8 -*-
from pymongo import MongoClient
import Config
from pymongo.errors import *
from Utils_errors import *
import time
class mongoDB(object):
	def __init__(self, url=Config.mongodbURL, port=Config.mongodbPort, database_name=Config.database, verbose=True):
		connect = MongoClient(url, port)
		self._database = connect[database_name]
		self._verbose = verbose


	def search(self, collection, filters, projections, sort, limit=1, skip=0):
		try:
			_collection = self._database[collection]
			cursor = _collection.find(filters, projections).limit(limit).sort(sort).skip(skip)
			proj = [key for key in projections]
			proj.remove("_id")
			retV = []
			for ele in cursor:
				retV.append(ele)
			return retV
		except ServerSelectionTimeoutError:
			raise PyMongoTimeOutError()

	def insert(self, collection, data):
		try:
			_collection = self._database[collection]
			result = _collection.insert_one(data)
			return result
		except ServerSelectionTimeoutError:
			raise PyMongoTimeOutError()
		except Exception as e:
			print(e)
			return None

	def update(self, collection, filters, data, is_inc=False):
		try:
			_collection = self._database[collection]
			update = {"$set": data} if not is_inc else {"$inc": data}
			result = _collection.update_one(filters, update)
			return result
		except ServerSelectionTimeoutError:
			raise PyMongoTimeOutError()
		except Exception as e:
			print(e)
			return None

	def count(self, collection, filters):
		try:
			_collection = self._database[collection]
			result = _collection.count(filters)
			return result
		except ServerSelectionTimeoutError:
			raise PyMongoTimeOutError()
		except Exception as e:
			print(e)
			return None

	def delete(self, collection, filters):
		try:
			_collection = self._database[collection]
			result = _collection.delete_many(filters)
			return result
		except ServerSelectionTimeoutError:
			raise PyMongoTimeOutError()
		except Exception as e:
			print(e)
			return None
	def select(self, collection):
		try:
			_collection = self._database[collection]
			cursor = _collection.find()
			return cursor
		except ServerSelectionTimeoutError:
			raise PyMongoTimeOutError()
	def selectDialog(self, ownerId,userId,botId,type,collection):
		try:
			datetime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
			_collection = self._database[collection]
			cursor = _collection.find({"userId":userId, "ownerId":ownerId, "botId":botId, "type":type, "create_time":{'$gte':datetime}}).sort("create_time", 1)
			return cursor
		except ServerSelectionTimeoutError:
			raise PyMongoTimeOutError()
	def selectCustom(self, collection, ownerId, userId, botId):
		try:
			# datetime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
			_collection = self._database[collection]
			cursor = _collection.find(
				{"userID": userId, "ownerID": ownerId, "botID": botId}).sort(
				"datetime", -1)
			return cursor
		except ServerSelectionTimeoutError:
			raise PyMongoTimeOutError()
_mongoDB = mongoDB()

if __name__ == "__main__":
	list = _mongoDB.selectCustom(collection= "user_rule", ownerId= "ltt", userId="ltt", botId="ltt")
	for ele in list:
		print (ele)
