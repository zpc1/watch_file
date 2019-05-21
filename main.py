#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/5/14 14:54
# @Author   : pczhang
# @Email    : 853252226@qq.com
# @File     : test.py
# @Software : PyCharm
from PyQt5.Qt import *
import sys

# 创建一个应用程序对象
app = QApplication(sys.argv)

# 控件操作

window = QWidget()
window.setWindowTitle("dicom客户端")
window.resize(800, 800)

label = QLabel(window)
label.setText("文件类型")
browser = QTextBrowser(window)
browser.app





window.show()


# 应用程序执行，进入消息循环
sys.exit(app.exec_())
