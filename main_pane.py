from PyQt5.Qt import *
from resource.main_ui import Ui_MainWindow
from watchdog.observers import Observer
# from watchdog.events import *
from FileEventHandler import *
import sys
import atexit
from PyQt5 import QtGui
from ConfigUtile import *
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init_config()

        self.btn_start.adjustSize()
        # self.btn_start.setEnabled(False)
        self.init_watchdog()

    # 配置文件
    def init_config(self):
        self.configname = "config/watch.conf"
        self.configUtile = ConfigUtile()
        config = self.configUtile.toDict(self.configname)
        self.clientconf = config.get('client')

    def closeEvent(self, a0: QtGui.QCloseEvent):
        # a0.ignore()
        pass

    def start_btn_clicked(self, isclicked):
        if isclicked:
            self.btn_start.setText("停止")
            self.start_watchfile()
        else:
            self.btn_start.setText("开始")
            self.stop_watchfile()

    def test_clicked(self):
        print(self.observer.is_alive())
        self.observer.stop()

    # 初始化配置文件，配置watchdog路径
    def init_watchdog(self):
        self.event_handler = FileEventHandler()
        self.event_handler.setConfig(self.clientconf)


    def start_watchfile(self):
        print('watching...')
        print(self.clientconf)
        self.observer = Observer()
        path = self.clientconf.get('watchpath')
        print('watch path', path)
        self.observer.schedule(self.event_handler, path, True)
        self.observer.start()

    def stop_watchfile(self):
        print('stop watch')
        self.observer.stop()

    def my_exec(self):
        self.observer.stop()

    def loadconfig(self):
        config = self.configUtile.toDict(self.configname)
        self.clientconf = config.get('client')
        print(self.clientconf)
        self.event_handler.setConfig(self.clientconf)


    def test_clicked(self):
        self.loadconfig()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = Window()

    window.show()
    atexit.register(window.my_exec)
    sys.exit(app.exec_())