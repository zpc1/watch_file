#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/5/20 17:13
# @Author   : pczhang
# @Email    : 853252226@qq.com
# @File     : FileEventHandler.py
# @Software : PyCharm
from watchdog.observers import Observer
from watchdog.events import *
import time
import requests


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        self.file_recent = ''
        self.t_recent = 0

    def setConfig(self, config):
        # print('config:',config)
        self.type = config.get('panotype')
        self.parsexml = config.get('parsexml')
        self.aetitle = config.get('aetitle')

    def on_created(self, event):
        # print('---------------')
        if not event.is_directory:
            file_path = event.src_path
            # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
            #       " - file created:{0}".format(file_path))
            t_now = time.time()

            if self.type in file_path:
                if self.file_recent != file_path or (t_now - self.t_recent) > 5:
                    time.sleep(10)
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                          " - file created:{0}".format(file_path))
                    if self.parsexml=='no':
                        print("文件上传")
                        with open(file_path, 'rb') as file:
                            multiple_files = [('multipartFiles', open(file_path, 'rb'))]
                            body = {"aetitle": self.aetitle}
                            response = requests.post("http://139.219.103.195:4000/deepcare/api/dicom/saveFile", files=multiple_files, data=body)
                            print(response.text)
                            print(response.status_code)
                    else:
                        print("解析xml")
                    self.file_recent = file_path
                    self.t_recent = t_now


if __name__ == '__main__':
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, "D:/DataContainer", True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()