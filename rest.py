import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os
path = os.path.dirname(os.path.abspath(__file__))


class RestWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowTitle("休息模式")

        # 加载背景图片
        palette = QPalette()
        pixmap = QPixmap(path+os.sep+'Elysia.jpg')
        palette.setBrush(QPalette.Background, QBrush(pixmap.scaled(1920,1080)))  # load pictures
        self.setPalette(palette)

        # 显示当前时间的 QLabel
        self.current_time_label = QLabel(self)
        self.current_time_label.setStyleSheet("color: black; font-size: 100px;")
        self.timer=QTimer()
        self.timer.singleShot(1000,self.update_current_time)


        # 退出按钮
        exit_button = QPushButton("退出", self)
        exit_button.clicked.connect(self.close)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.current_time_label, alignment=Qt.AlignCenter)
        layout.addWidget(exit_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
    
    def update_current_time(self):
        # 获取当前时间
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss\n     正在休息")

        # 更新当前时间的 QLabel
        self.current_time_label.setText(current_time)
        self.timer.singleShot(1000, self.update_current_time)

    def keyPressEvent(self, event):
        # 按下ESC键关闭窗口
        if event.key() == Qt.Key_Escape:
            self.close()


class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowTitle("定时休息软件")

        # 创建组件
        self.time_edit = QLineEdit(self)
        self.time_edit.setPlaceholderText("请输入等待时间（分钟）")
        self.start_button = QPushButton("开始", self)
        self.start_button.clicked.connect(self.start_timer)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.time_edit)
        layout.addWidget(self.start_button)
        self.rest_widget = RestWidget()
        self.setLayout(layout)

    def start_timer(self):
        # 获取等待时间（分钟）
        wait_time = float(self.time_edit.text())

        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_rest_widget)
        self.timer.start(wait_time * 60000)  # 将分钟转换为毫秒

    def show_rest_widget(self):
        # 显示休息模式窗口
        print('start')
        
        self.rest_widget.showFullScreen()
        self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置全局样式
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)

    # 创建定时休息软件窗口
    timer_widget = TimerWidget()
    timer_widget.show()

    sys.exit(app.exec_())