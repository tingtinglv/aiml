介绍
============
aiml人工智能语言,修改kernel核心代码，支持一下功能：
1.支持中文
2.对话过程中，set 变量值以及历史对话内容存入mongodb
3.添加ownerID(开发者id),userID(用户id),botID(机器人id)，用于区分多种对话过程。
4.topic对话状态记录
5.set变量有效期
6.支持时间抽取
使用方法
============
    Aiml_result.py 测试入口
    views.py 是flask 浏览器访问接口

使用方式：
===============
1.安装mongodb，然后在任意盘下面添加数据库目录，例如 c:\mdb (目录不允许有空格，例如 c:\file ashsh\mdb)
2.cmd 启动数据库连接，mongod -port 2222 --dbpath c:\mdb
4.安装相关类库，flask，以及https://gitlab.com/deepintellgp1/TimeAnalyzer  中时间类库，安装步骤见readme.txt
3.运行views.py 即可。
4.Aiml_result.py 是测试入口。
