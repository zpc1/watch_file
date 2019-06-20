from resource.main_ui import Ui_MainWindow
# from watchdog.events import *
from FileEventHandler import *
import atexit
from PyQt5 import QtGui
from ConfigUtile import *
import traceback
from TrayIcon import *
import psutil
import os
from win32com.client import Dispatch
import win32com
import threading
from win32api import *
from win32con import *
import win32api
import win32con
from utile.MailUtile import MailUtile

class Window(QMainWindow, Ui_MainWindow):
    Logsignal = pyqtSignal(str)

    def __init__(self, path):
        try  :
            super().__init__()
            print('---'+path)
            # self.workpath = "C:\\Program Files (x86)\\main_pane\\"
            # self.workpath = "C:\\Users\\deepcare\\Desktop\\watch_file\\"
            self.workpath = path
            self.iconpath = self.workpath+"vvv.png"
            self.configname = self.workpath + "config\\watch.conf"
            print("1111111111111")
            self.setWindowIcon(QIcon(self.iconpath))
            self.setupUi(self)
            self.init_config()
            self.setup_ui()
            self.init_watchdog()
            self.Logsignal.connect(self.logtopte)
            self.mail = MailUtile()
            if self.clientconf.get('auto_listen')=='yes':
                self.start_watchfile()
        except Exception:
            self.logtopte(traceback.format_exc())
            self.mail.sendMail("window error>>>"+traceback.format_exc(), self.clientconf.get("aetitle"))

    def setup_ui(self):
        self.btn_start.adjustSize()
        self.pte_log.setAutoFillBackground(True)
        self.pte_log.setReadOnly(True)
        # self.setWindowIcon(QIcon(self.iconpath))
        trayicon = TrayIcon(self,path=self.iconpath)
        # trayicon = TrayIcon(self)
        trayicon.show()


    # 配置文件
    def init_config(self):
        self.configUtile = ConfigUtile()
        print("config name:"+self.configname)
        config = self.configUtile.toDict(self.configname)
        self.clientconf = config.get('client')
        self.logname = time.strftime("%Y-%m-%d", time.localtime())

    def closeEvent(self, a0: QtGui.QCloseEvent):
        a0.ignore()
        # pass
        self.hide()

    def start_btn_clicked(self, isclicked):
        if isclicked:
            self.btn_start.setText("停止")
            self.start_watchfile()
        else:
            self.btn_start.setText("开始")
            self.stop_watchfile()

    # def test_clicked(self):
    #     print(self.observer.is_alive())
    #     self.logtopte(self.observer.is_alive())
    #     self.observer.stop()

    # 初始化配置文件，配置watchdog路径
    def init_watchdog(self):
        self.event_handler = FileEventHandler()
        self.event_handler.setConfig(self.clientconf, self.Logsignal)

    def start_watchfile(self):
        self.logtopte("watching..")
        self.btn_start.setText("停止")
        # print(self.clientconf)
        self.observer = Observer()
        path = self.clientconf.get('watchpath')
        print('watch path', path)

        # self.observer.schedule(self.event_handler,"C:\\", True)

        if not path:
            import psutil
            self.logtopte('watch path:')
            for disk in psutil.disk_partitions():
                # print(disk.device)
                if 'rw' in disk[3]:
                    self.observer.schedule(self.event_handler, disk.device, True)
                    self.logtopte(disk.device)

        else:
            self.observer.schedule(self.event_handler, path, True)
            self.logtopte('watch path:'+ path)
        self.observer.start()
        self.mail.sendMail("开始监听", self.clientconf.get("aetitle"))

    def stop_watchfile(self):
        print('stop watch')
        self.btn_start.setText("开始")
        self.logtopte("stop watch")
        self.observer.stop()


        self.mail.sendMail(self.pte_log.toPlainText(),self.clientconf.get("aetitle"))

    def my_exec(self):
        if 'observer'in dir(self):
            self.observer.stop()

        log = self.pte_log.toPlainText()
        if log == '':
            return
        self.mail.sendMail(self.pte_log.toPlainText(), self.clientconf.get("aetitle"))
        print('---------')
        with open(self.workpath+"log\\"+self.logname, "a+", encoding='utf-8') as f:
            f.write("\r\n"+log)


    def loadconfig(self):
        config = self.configUtile.toDict(self.configname)
        self.clientconf = config.get('client')
        # print(self.clientconf)
        self.logtopte(str(self.clientconf))
        self.event_handler.setConfig(self.clientconf, self.Logsignal)

    def init_para_clicked(self):
        self.loadconfig()
        # self.showMinimized()
        # print(self.isrunning())

    def logtopte(self, text):
        self.pte_log.appendPlainText(time.strftime("%H:%M:%S", time.localtime())+" :  "+text)
        # print("----"+text)

    def showWarmingDialog(self):
        mb = QMessageBox(self)
        mb.setModal(False)
        mb.setIcon(QMessageBox.Warning)
        mb.setText("系统检测到该程序正在后台运行")
        mb.setInformativeText("请点击确认取消本次任务")
        mb.setStandardButtons(QMessageBox.Yes)
        yes_btn = mb.button(QMessageBox.Yes)

        def clicked(btn):
            self.setVisible(False)
            self.close()
            qApp.quit()
            sys.exit(0)

        mb.buttonClicked.connect(clicked)
        mb.setDefaultButton(yes_btn)
        mb.exec()


def test():
    print("jklsdjfklslfksdfldskf")
if __name__ == '__main__':
    pypath = sys.argv[0]
    print("path = "+pypath)
    exepath = pypath.replace(".py", ".exe")
    # work_path = exepath[:(exepath.rindex("/")+1)]
    work_path = "C:\\Program Files (x86)\\main_pane\\"
    name = exepath.split("/")
    # print(name)

    # Write to Windows Registry
    value_name = name
    program_path = exepath
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
    except Exception:
        print(traceback.format_exc())
        # pass


    isrunning = False
    from utile.SysUtile import SysUtile
    sysUtile = SysUtile()

    # print(name)
    isrunning = sysUtile.isrunning(name)

    app = QApplication(sys.argv)
    window = Window(work_path)
    window.show()

    app.aboutToQuit.connect(test)
    if isrunning:
        print('已经运行')
        window.showWarmingDialog()

    atexit.register(window.my_exec)

    # exe = name.replace(".py", ".exe")
    # print(exe)
    # if os.path.exists(exe):
    #     print("shanchu")
    #     os.rename(exe, exe+'.bak')
    sys.exit(app.exec_())



