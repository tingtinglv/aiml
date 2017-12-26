# -*- coding:utf-8 -*-
from pymongo import MongoClient


class mongoDB(object):
	def __init__(self, url="127.0.0.1", port=2222, database_name="test", verbose=True):
		connect = MongoClient(url, port)
		self._database = connect[database_name]
		self._verbose = verbose

	def search(self, collection, filters, projections, sort, limit=1):
		try:
			_collection = self._database[collection]
			cursor = _collection.find(filters, projections).limit(limit).sort(sort)
			return cursor
		except:
			return None

	def insert(self, collection, data):
		try:
			_collection = self._database[collection]
			result= _collection.insert_one(data)
			return result
		except:
			return None

	def delete(self, collection, filters):
		try:
			_collection = self._database[collection]
			result = _collection.delete_many(filters)
			return result
		except:
			return None

_mongoDB = mongoDB()