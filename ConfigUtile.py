#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/5/17 9:54
# @Author   : pczhang
# @Email    : 853252226@qq.com
# @File     : ConfigUtile.py
# @Software : PyCharm

from configparser import ConfigParser
'''
SafeConfigParser()  是配置文件解析器类，该类的方法有
read(configfile):读取配置文件
get(node,options),找出node节点的options选项的值（[mysqld]是节点,socket是选项）
sections():获取配置文件的节点，返回一个列表
options(node):获取节点里面的选项，返回一个列表
items(node):把节点名里面选项和值，以字典的方式返回，即选项=值

值的类型
get(node,options)：会返回一个字符串
getint():返回一个整数
getfloat():返回一个浮点型
getboolean():返回布尔值，真值:1,yes,on,True 假值：0,no,off,false

测试节点或者选项是否存在
has_section(node):如果节点存在就返回True，不存在就返回False
has_option(node,option):如果节点里面的选项存在就返回True，不存在就返回False


add_section(node):增加一个节点
set(node,options,value):修改或者添加选项,注意值只接受字符串
remove_section(node):移除一个节点，注意节点移除后，这个节点里面的选项也会自动跟着移除
remove_option(node,option):移除一个选项
'''

class ConfigUtile:
    def __init__(self):
        self.conf = ConfigParser()

    def readConfig(self, name):
        self.configname = name
        self.conf.read(name)
        self.sections = self.conf.sections()
        return self.sections

    def getSections(self):
        return self.conf.sections()

    def getItemsBySection(self, section):
        return self.conf.items(section)

    def getAllItems(self):
        items = {}
        for nodename in self.getSections():
            item = self.conf.items(nodename)
            items[nodename] = item
        return items

    def toDict(self, name):
        conf = ConfigParser()
        conf.read(name, encoding='utf-8')
        items = {}
        for nodename in conf.sections():
            print(nodename)
            opt = {}
            for son in conf.items(nodename):
                # print(son[0])
                opt.update({son[0]:son[1]})
            items[nodename] = opt
        return items

    def updateValue(self, name ,section, key, value):
        conf = ConfigParser()
        conf.read(name, encoding='utf-8')
        conf.set(section, key, value)
        with open(name, "w+") as f:
            conf.write(f)

    def saveConfig(self, configname):
        with open(configname, "w+") as f:
            self.conf.write(f)
        # print(self.getAllItems())

    def getPath(self):
        return self.conf.get(self.sections[0], "panopath")

    # 新建config
    # def writeConfig(self):
    #     self.conf.add_section("test")
    #     self.conf.set("test", "count", str(1))
    #
    #     with open("config/test.conf", "w+") as f:
    #         self.conf.write(f)
    #     print(self.getAllItems())

if __name__ == '__main__':
    configname = "D:/Users/deepcare/PycharmProjects/watch_file/config/watch.conf"
    conf = ConfigUtile()
    # conf.readConfig(configname)
    # # conf.readConfig("config/test.ini")
    # sections = conf.getSections()
    # print(sections)
    # print(conf.getItemsBySection(sections[0]))
    # conf.getPath()
    #
    # conf.writeConfig()
    conf.updateValue(configname,"client", "aetitle", "111")
    dict = conf.toDict(configname)
    print(dict)