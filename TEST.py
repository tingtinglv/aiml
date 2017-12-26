# -*- coding:utf-8 -*-
import os
import RBCS as aiml
import re
from CustomDesigns import CustomDesign
import CustomConfig as cf

# cd = CustomDesign(verbose=True)

# 列举规则 测试

# cd.listRule(cf.custom_designColl, userID="alice")

# 添加规则 测试。
# cd.setRuleFromFile(cf.custom_designColl, "bot", "alice", "rule_file")
# cd.setSingleRule(cf.custom_designColl, "alice", "bob", "^.*你好呀$", "你好吗")
# ruleList = [("^.*你好    $", "你好"), ("^.*你好吗$","你好吗"), ("^.*你好\?$#","你好?"),("^.*你好china\?$", " 你好?")]
# cd.setRuleBatch(cf.custom_designColl, "alice", "bob", ruleList)
def chain():
    res = "我要出发"
    return res,""
if __name__ == "__main__":
    from TimeConvert import TimeConvert

    tn = TimeConvert(isPreferFuture=True)
    res = tn.parse(u'明天早晨')
    print res

