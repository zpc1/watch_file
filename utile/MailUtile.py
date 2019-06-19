#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/6/18 9:41
# @Author   : pczhang
# @Email    : 853252226@qq.com
# @File     : MailUtile.py
# @Software : PyCharm
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart

class MailUtile:
    def __init__(self):
        # 发送邮箱
        # sender = 'pzhang@huohuomei.com'
        self.sender = 'pczhang@deepcare.com'

        # 接收邮箱
        self.receiver = 'support@deepcare.com'

        # 发送邮件主题
        self.subject = 'clent error describe'

        # 发送邮箱账户名、密码
        # username = "pzhang@huohuomei.com"
        self.username = "pczhang@deepcare.com"
        # password = "Huomei123."
        self.password = "19900807Zpc!"

    def sendMail(self,context,aet):
        msg = MIMEMultipart()
        msg.attach(MIMEText(context+"<br>aet:"+aet, 'html', 'utf-8'))
        msg["From"] = formataddr(["RecSMTP", self.sender])
        msg["To"] = formataddr(["FromSMTPQQ", self.receiver])
        msg["Subject"] = "来自"+aet+"的日志邮件"  # 注意：主题不能使用MIMEMultipart，但可以使用Header


        smtp = smtplib.SMTP()
        smtp.connect('smtp.exmail.qq.com')
        smtp.login(self.username, self.password)
        result = smtp.sendmail(self.sender, self.receiver, msg.as_string())
        print(result)
        smtp.quit()

if __name__ == '__main__':
    mail = MailUtile()