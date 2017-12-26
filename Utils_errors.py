# -*- coding:utf-8 -*-


class PyMongoError(Exception):
	def __init__(self, msg=None):
		self._msg = msg

	def __str__(self):
		if self._msg:
			return self._msg
		else:
			return "MongoDB Error"


class PyMongoTimeOutError(PyMongoError):
	def __init__(self, msg=None):
		self._msg = msg
		Exception.__init__(self, msg)

	def __str__(self):
		if self._msg:
			return self._msg
		else:
			return "MongoDB Connect Time Out.."
class NoAnswer(Exception):
	def __init__(self, msg = None):
		self._msg = msg
