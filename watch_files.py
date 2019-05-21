#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2019/5/20 13:14
# @Author   : pczhang
# @Email    : 853252226@qq.com
# @File     : watch_files.py
# @Software : PyCharm
import os
import time
import sys
import requests
import json
import xmltodict
from watchdog.observers import Observer
from watchdog.events import *
from win32api import *
from win32con import *
import win32api
import win32con

# watch_folder = 'C:\\Users\\Hailong\\Desktop\\Test'
watch_folder = 'E:\\DB\\'
name_institution = 'one_clinic'
aetitle = 'd00000000000000'
device_type = 'Kodak_01'

url_dicom = 'http://139.219.103.195:4000/deepcare/api/dicom/saveFile'
url_tiff = 'http://139.219.103.195:4000/deepcare/api/tiff/upload'

## Write to Windows Registry
value_name = 'watch_files'
program_path = 'C:\\Program Files\\DeepCare\\watch_files.exe'
KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
try:
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
    info = RegQueryInfoKey(key)
    value_names = []
    for i in range(0, info[1]):
        ValueName = RegEnumValue(key, i)
        value_names.append(ValueName[0])
    if value_name not in value_names:
        win32api.RegSetValueEx(key, value_name, 0, win32con.REG_SZ, program_path)
    win32api.RegCloseKey(key)
except:
    print('Reg Error.')


class FileEventHandlerKodak(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        self.file_recent = ''
        self.t_recent = 0

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_path = file_path.replace('\\', '/')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                  " - file created:{0}".format(file_path))
            t_now = time.time()

            if '.pano' in file_path:
                if self.file_recent != file_path or (t_now - self.t_recent) > 5:
                    time.sleep(10)
                    multiple_files = [('multipartFiles', open(file_path, 'rb'))]
                    body = {"aetitle": aetitle}
                    response = requests.post(url_dicom, files=multiple_files, data=body)
                    print(response.text)
                    print(response.status_code)
                    self.file_recent = file_path
                    self.t_recent = t_now


class FileEventHandlerSirona(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        self.file_recent = ''
        self.t_recent = 0

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_path = file_path.replace('\\', '/')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                  " - file created:{0}".format(file_path))
            t_now = time.time()

            if '2D' in file_path and file_path.rsplit('.', 1)[-1] == 'img':
                if self.file_recent != file_path or (t_now - self.t_recent) > 5:
                    time.sleep(5)
                    xml_path = file_path.replace('.img', '.xml')
                    with open(xml_path, encoding='utf8') as f:
                        xml_dict = xmltodict.parse(f.read())

                    type_img = xml_dict['IMAGEDESCRIPTION']['IMAGE']['@programbasename']
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
                            'InstitutionName': name_institution,
                            'StudyDate': date_img,
                            'Rows': n_row,
                            'Columns': n_col,
                        }
                        img_path = file_path.replace('.img', '.tif')
                        multiple_files = [('multipartFile', open(img_path, 'rb'))]
                        body = {
                            'id': id_patient,
                            'name': name_patient,
                            'aetitle': aetitle,
                            'json': str(output),
                        }
                        response = requests.post(url_tiff, files=multiple_files, data=body)
                        print(response.text)
                        print(response.status_code)
                        self.file_recent = file_path
                        self.t_recent = t_now





if __name__ == "__main__":
    if device_type == 'Kodak_01':
        event_handler = FileEventHandlerKodak()
    elif device_type == 'Sirona_01':
        event_handler = FileEventHandlerSirona()

    path = watch_folder if len(watch_folder) > 1 else '.'

    observer = Observer()
    observer.schedule(event_handler, path, True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()