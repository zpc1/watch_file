#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/6/12 9:44
# @Author   : pczhang
# @Email    : 853252226@qq.com
# @File     : SysUtile.py
# @Software : PyCharm
from win32com.client import Dispatch
import win32com
import os

class SysUtile:
    def isrunning(self, name):
        pidnum = 0
        wmi = win32com.client.GetObject('winmgmts:')
        for p in wmi.InstancesOf('win32_process'):
            if p.Name == 'main_pane.exe':
                pidnum += 1
                # return True
                # print(p.Name , p.Properties_('ProcessId'))
                # if p.Properties_('ProcessId') != os.getpid():
                #     return True
                # print(
                # p.Name, p.Properties_('ProcessId'), \
                # int(p.Properties_('UserModeTime').Value) + int(p.Properties_('KernelModeTime').Value))

                # children = wmi.ExecQuery(
                #     'Select * from win32_process where ParentProcessId=%s' % p.Properties_('ProcessId'))
                # for child in children:
                #     print(
                #     '\t', child.Name, child.Properties_('ProcessId'), \
                #     int(child.Properties_('UserModeTime').Value) + int(child.Properties_('KernelModeTime').Value))
        # print(wmi)
        # print(wmi.ExecQuery('select * from Win32_Process where name=\"%s\"' % (name.split('.')[0])))
        #     else:
        #         return False
        # return False
        if pidnum < 3:
            return False
        else:
            return True

if __name__ == '__main__':
    import psutil

    for disk in psutil.disk_partitions():
        print(disk)