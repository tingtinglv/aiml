#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import re


findall_utf8 = re.compile(u'[\u4e00-\u9fff][，。？！]?|[^\u4e00-\u9fff ]+').findall
sub_utf8 = re.compile(u' +').sub
LangSupport = type('LangSupport', (),
                   {'__init__': lambda self, encodings='utf-8': self.__setattr__('encodings', encodings),
                    '__call__': lambda self, s: self.input(s),
                    'input': lambda self, s: ' '.join(findall_utf8(s)),
                    'output': lambda self, s: s})

