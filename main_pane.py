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

class Window(QMainWindow, Ui_MainWindow):
    Logsignal = pyqtSignal(str)

    def __init__(self):
        try  :
            super().__init__()
            self.setWindowIcon(QIcon("vvv.png"))
            self.setupUi(self)
            self.init_config()
            self.setup_ui()
            self.init_watchdog()
            self.Logsignal.connect(self.logtopte)
        except Exception:
            self.logtopte(traceback.format_exc())

    def setup_ui(self):
        self.btn_start.adjustSize()
        self.pte_log.setAutoFillBackground(True)
        self.pte_log.setReadOnly(True)
        self.setWindowIcon(QIcon("vvv.png"))
        trayicon = TrayIcon(self)
        trayicon.show()

    # 配置文件
    def init_config(self):
        self.configname = "config/watch.conf"
        self.configUtile = ConfigUtile()
        config = self.configUtile.toDict(self.configname)
        self.clientconf = config.get('client')
        self.logname = time.strftime("%Y-%m-%d", time.localtime())
        print(self.logname)

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
        print(self.clientconf)
        self.observer = Observer()
        path = self.clientconf.get('watchpath')
        print('watch path', path)
        if not path:
            import psutil
            for disk in psutil.disk_partitions():
                print(disk.device)
                self.observer.schedule(self.event_handler, disk.device, True)

        else:
            self.observer.schedule(self.event_handler, path, True)
        self.logtopte('watch path:'+ path)


        self.observer.start()

    def stop_watchfile(self):
        print('stop watch')
        self.logtopte("stop watch")
        self.observer.stop()

    def my_exec(self):
        if 'observer'in dir(self):
            self.observer.stop()

        log = self.pte_log.toPlainText()
        if log == '':
            return
        print('---------')
        with open("log/"+self.logname, "a+", encoding='utf-8') as f:
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



if __name__ == '__main__':

    isrunning = False
    from utile.SysUtile import SysUtile
    sysUtile = SysUtile()
    name = sys.argv[0]
    print(name)
    isrunning = sysUtile.isrunning(name)

    app = QApplication(sys.argv)
    window = Window()
    window.show()

    if isrunning:
        print('已经运行')
        window.showWarmingDialog()

    atexit.register(window.my_exec)
    sys.exit(app.exec_())

