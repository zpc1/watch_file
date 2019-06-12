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
import xmltodict
import traceback
import queue
from threading import Event
import threading
from threading import Thread


class FileThread(Thread):
    def __init__(self,queue, event, filename, signal):
        Thread.__init__(self)
        self.queue = queue
        self.mevent = event
        self.filename = filename
        self.isloop = True
        self.signal = signal
        self.starttime = time.time()

    def run(self):
        print(threading.currentThread())
        print(threading.active_count())
        while self.isloop:
            try:
                # raise RuntimeError('testerror')
                with open(self.filename, 'r') as file:
                    print('发送文件消息'+str(time.time()-self.starttime)+'s')
                    self.isloop = False
                    self.mevent.set()
            except Exception:
                if 'PermissionError' in traceback.format_exc():
                    print('文件没写完')
                    time.sleep(0.5)
                else:
                    self.isloop = False
                    self.signal.emit(traceback.format_exc())
                    self.mevent.set()

        print("线程死亡:")


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        self.file_recent = ''
        self.t_recent = 0

    def setConfig(self, config, signal):
        self.signal = signal
        # print('config:',config)
        self.type = config.get('panotype')
        self.parsexml = config.get('parsexml')
        self.aetitle = config.get('aetitle')
        self.name_institution = config.get('name_institution')
        self.sonpath = config.get('sonpath')


    def on_created(self, event):
        try:
            # print('---------------')
            if not event.is_directory:
                file_path = event.src_path
                # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                #       " - file created:{0}".format(file_path))
                t_now = time.time()

                if self.type in file_path and self.sonpath in file_path:
                    if self.file_recent != file_path or (t_now - self.t_recent) > 5:
                        q = queue.Queue()
                        mevent = Event()
                        thread = FileThread(q, mevent, file_path, self.signal)
                        thread.start()
                        mevent.wait()
                        # print(threading.current_thread())
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                              " - file created:{0}".format(file_path))

                        self.signal.emit(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                              " - file created:{0}".format(file_path))
                        if self.parsexml=='no':
                            print("正在上传")
                            self.signal.emit("正在上传")
                            with open(file_path, 'rb') as file:
                                multiple_files = [('multipartFiles', open(file_path, 'rb'))]
                                body = {"aetitle": self.aetitle}
                                # response = requests.post("http://139.219.103.195:4000/deepcare/api/dicom/saveFile", files=multiple_files, data=body)
                                # print(response.text)
                                # self.signal.emit(response.text)
                                # print(response.status_code)
                        else:
                            print("解析xml")
                            self.signal.emit("解析xml")
                            xml_path = file_path.replace(self.type, 'xml')
                            with open(xml_path, encoding='utf-8') as f:
                                xml_dict = xmltodict.parse(f.read())

                            type_img = xml_dict['IMAGEDESCRIPTION']['IMAGE']['@programbasename']
                            print(type_img)
                            if type_img == 'P1':
                                name_last = xml_dict['IMAGEDESCRIPTION']['PATIENT']['@lastname']
                                name_first = xml_dict['IMAGEDESCRIPTION']['PATIENT']['@firstname']
                                date_birth = xml_dict['IMAGEDESCRIPTION']['PATIENT']['@birthdate']
                                date_img = xml_dict['IMAGEDESCRIPTION']['IMAGE']['@takedate']
                                time_img = xml_dict['IMAGEDESCRIPTION']['IMAGE']['@taketime']
                                n_col = xml_dict['IMAGEDESCRIPTION']['IMAGE']['@noofcolums']
                                n_row = xml_dict['IMAGEDESCRIPTION']['IMAGE']['@noofrows']
                                if name_last == name_first and len(name_last) > 1:
                                    name_patient = name_last
                                else:
                                    name_patient = name_last + name_first
                                date_birth = date_birth.replace('-', '')
                                id_patient = name_patient + date_birth
                                output = {
                                    'PatientID': id_patient,
                                    'PatientName': name_patient,
                                    'PatientBirthDate': date_birth,
                                    'InstitutionName': self.name_institution,
                                    'StudyDate': date_img,
                                    'Rows': n_row,
                                    'Columns': n_col,
                                }
                                img_path = file_path
                                print("img_path",img_path)

                                with open(img_path, 'rb') as file:
                                    multiple_files = [('multipartFile',file )]
                                    body = {
                                        'id': id_patient,
                                        'name': name_patient,
                                        'aetitle': self.aetitle,
                                        'json': str(output),
                                    }
                                    # response = requests.post("http://139.219.103.195:4000/deepcare/api/tiff/upload", files=multiple_files, data=body)
                                    # print(response.text)
                                    # self.signal.emit(response.text)
                                    # print(response.status_code)
                        self.file_recent = file_path
                        self.t_recent = t_now
        except Exception:
            print('error')
            self.signal.emit(traceback.format_exc())

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