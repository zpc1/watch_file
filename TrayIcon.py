#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/5/23 11:32
# @Author   : pczhang
# @Email    : 853252226@qq.com
# @File     : TrayIcon.py
# @Software : PyCharm

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None, **kwargs):
        self.iconpath = kwargs.get('path')
        super(TrayIcon, self).__init__(parent)
        # print(self.iconpath)

        self.showMenu()
        self.other()

    def setIconPath(self, path):
        self.iconpath = path

    def showMenu(self):
        "设计托盘的菜单，这里我实现了一个二级菜单"
        self.menu = QMenu()
        self.menu1 = QMenu()
        self.showAction1 = QAction("显示消息1", self, triggered=self.showM)
        self.showAction2 = QAction("显示消息2", self,triggered=self.showM)
        self.quitAction = QAction("退出", self, triggered=self.quit)

        self.menu1.addAction(self.showAction1)
        self.menu1.addAction(self.showAction2)
        self.menu.addMenu(self.menu1, )

        self.menu.addAction(self.showAction1)
        self.menu.addAction(self.showAction2)
        self.menu.addAction(self.quitAction)
        self.menu1.setTitle("二级菜单")
        self.setContextMenu(self.menu)

    def other(self):
        self.activated.connect(self.iconClied)
        #把鼠标点击图标的信号和槽连接
        self.messageClicked.connect(self.mClied)
        #把鼠标点击弹出消息的信号和槽连接
        self.setIcon(QIcon(self.iconpath))
        # self.setIcon(QIcon("vvv.png"))
        self.icon = self.MessageIcon()
        #设置图标

    def iconClied(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            pw = self.parent()
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()
        # print(reason)

    def mClied(self):
        self.showMessage("提示", "你点了消息", self.icon)

    def showM(self):

        self.showMessage("测试", "我是消息", self.icon)

    def quit(self):
        "保险起见，为了完整的退出"
        self.setVisible(False)
        self.parent().close()
        qApp.quit()
        sys.exit(0)




class window(QWidget):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        ti = TrayIcon(self)
        ti.show()

    def closeEvent(self, a0: QCloseEvent):
        a0.ignore()
        self.hide()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = window()
    w.show()
    sys.exit(app.exec_())
