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
    Logsignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_config()
        self.setup_ui()

        # self.btn_start.setEnabled(False)
        self.init_watchdog()
        self.Logsignal.connect(self.logtopte)

    def setup_ui(self):
        self.btn_start.adjustSize()
        self.pte_log.setAutoFillBackground(True)
        self.pte_log.setReadOnly(True)

    # 配置文件
    def init_config(self):
        self.configname = "config/watch.conf"
        self.configUtile = ConfigUtile()
        config = self.configUtile.toDict(self.configname)
        self.clientconf = config.get('client')
        self.logname = time.strftime("%Y-%m-%d", time.localtime())
        print(self.logname)

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
        self.logtopte(self.observer.is_alive())
        self.observer.stop()

    # 初始化配置文件，配置watchdog路径
    def init_watchdog(self):
        self.event_handler = FileEventHandler()
        self.event_handler.setConfig(self.clientconf, self.Logsignal)

    def start_watchfile(self):
        print('watching...',self.pte_log)
        self.logtopte("watching..")
        print(self.clientconf)
        self.observer = Observer()
        path = self.clientconf.get('watchpath')
        print('watch path', path)
        self.logtopte('watch path:'+ path)
        self.observer.schedule(self.event_handler, path, True)
        self.observer.start()

    def stop_watchfile(self):
        print('stop watch')
        self.logtopte("stop watch")
        self.observer.stop()

    def my_exec(self):
        self.observer.stop()
        with open("log/"+self.logname, "a+", encoding='utf-8') as f:
            f.write("\r\n"+self.pte_log.toPlainText())

    def loadconfig(self):
        config = self.configUtile.toDict(self.configname)
        self.clientconf = config.get('client')
        print(self.clientconf)
        self.logtopte(str(self.clientconf))
        self.event_handler.setConfig(self.clientconf, self.Logsignal)

    def test_clicked(self):
        self.loadconfig()

    def logtopte(self, text):
        self.pte_log.appendPlainText(time.strftime("%H:%M:%S", time.localtime())+" :  "+text)
        # print("----"+text)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()

    window.show()
    atexit.register(window.my_exec)

    sys.exit(app.exec_())
