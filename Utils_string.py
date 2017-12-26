# -*- coding:utf-8 -*-
import re


def ignoreWS(str):
	"""将str左右的空白字符去掉"""
	result = re.match(r'^[ \t\n\r]*(.*?)[ \t\n\r]*$', str)
	retV = result.group(1) if result else ""
	return retV


def list2str(ls, ls_type="conditions"):
	string = ""
	if not isinstance(ls, list):
		return str(ls)
	if ls_type == "conditions":
		for idx, ele in enumerate(ls):
			ls[idx] = list2str(ele, ls_type)
		string = "[" + ",".join(ls) + "]"
	return string


def str2list(string="", content_type="tree"):
	"""
	将str形式的list转成list。

	:param string: str 形式的list
	:param content_type: list内容，现有 tree, int,conditions
	:return: list
	"""

	string = string.decode("utf-8") if isinstance(string, str) else string

	if string[0] != "[" or string[-1] != "]":
		return string
	if len(string) == 2:
		return []
	if content_type == "tree":
		ls = []
		start_idx = 0
		cur_idx = 0
		count = 0
		str_len = len(string) - 1
		while True:
			l_bracket_idx = string.find("(", cur_idx)
			r_bracket_idx = string.find(")", cur_idx)
			if l_bracket_idx == -1:
				# 从cur_idx 到最后都是一个tree
				ls.append(string[start_idx+1: -1])
				break
			elif l_bracket_idx < r_bracket_idx:
				count += 1
				cur_idx = l_bracket_idx+1
			elif r_bracket_idx == -1:
				raise IndexError
			else:
				count -= 1
				cur_idx = r_bracket_idx + 1
				if count == 0:
					ls.append(string[start_idx + 1: r_bracket_idx+1])
					start_idx = cur_idx = r_bracket_idx + 1
					if start_idx >= str_len:
						break
	else:
		# 格式化list中各项
		if content_type == "int":
			ls = string[1:-1].split(",")
			for idx, ele in enumerate(ls):
				ls[idx] = int(ele)
		elif content_type == "conditions":
			# string like:'[[TRUE,TRUE,TRUE],[IS_GT,age,12]]'
			ls = string[:-1].split("]")
			# ls like: ['[TRUE,TRUE,TRUE','[IS_GT,age,12']
			for idx, ele in enumerate(ls):
				if ele != "":
					ls[idx] = ele[2:].split(",")
				else:
					ls.pop(idx)
	return ls
