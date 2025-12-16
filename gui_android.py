import sys
import os
import subprocess
import threading
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QCheckBox,
                             QMessageBox, QScrollArea, QFormLayout, QGroupBox, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings, QStandardPaths
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor

class LogThread(QThread):
    """日志输出线程"""
    log_signal = pyqtSignal(str)
    
    def __init__(self, process):
        super().__init__()
        self.process = process
        self.running = True
        
    def run(self):
        """读取进程输出"""
        while self.running and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if line:
                    self.log_signal.emit(line.decode('utf-8').strip())
                else:
                    time.sleep(0.1)
            except Exception as e:
                self.log_signal.emit(f"[错误] 日志读取失败: {str(e)}")
                break

class ECHWorkersGUI(QMainWindow):
    """ECH Workers Android客户端"""
    
    def __init__(self):
        super().__init__()
        self.process = None
        self.log_thread = None
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("ECH Workers 客户端")
        self.setMinimumSize(800, 600)
        
        # 设置样式
        self.set_style()
        
        # 主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 服务器配置区域
        config_group = QGroupBox("服务器配置")
        config_layout = QFormLayout(config_group)
        config_layout.setSpacing(10)
        
        # 服务地址
        self.server_edit = QLineEdit()
        self.server_edit.setPlaceholderText("your-worker.workers.dev:443")
        config_layout.addRow("服务地址:", self.server_edit)
        
        # 监听地址
        self.listen_edit = QLineEdit()
        self.listen_edit.setPlaceholderText("127.0.0.1:30000")
        config_layout.addRow("监听地址:", self.listen_edit)
        
        # 身份令牌
        self.token_edit = QLineEdit()
        self.token_edit.setEchoMode(QLineEdit.Password)
        config_layout.addRow("身份令牌:", self.token_edit)
        
        # 分流模式
        self.routing_combo = QComboBox()
        self.routing_combo.addItems(["global", "bypass_cn", "none"])
        self.routing_combo.setCurrentText("global")
        config_layout.addRow("分流模式:", self.routing_combo)
        
        main_layout.addWidget(config_group)
        
        # 控制按钮区域
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        
        self.start_btn = QPushButton("启动代理")
        self.start_btn.clicked.connect(self.start_proxy)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        
        self.stop_btn = QPushButton("停止代理")
        self.stop_btn.clicked.connect(self.stop_proxy)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white;")
        
        self.save_btn = QPushButton("保存配置")
        self.save_btn.clicked.connect(self.save_settings)
        self.save_btn.setStyleSheet("background-color: #2196F3; color: white;")
        
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(control_layout)
        
        # 日志区域
        log_group = QGroupBox("运行日志")
        log_layout = QVBoxLayout(log_group)
        
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setStyleSheet("background-color: #f5f5f5;")
        
        log_layout.addWidget(self.log_edit)
        main_layout.addWidget(log_group)
        
        # 状态标签
        self.status_label = QLabel("状态: 已停止")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
        main_layout.addWidget(self.status_label)
        
        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)
        
    def set_style(self):
        """设置界面样式"""
        # 设置全局字体
        font = QFont("SansSerif", 10)
        QApplication.setFont(font)
        
        # 设置样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)
        
    def load_settings(self):
        """加载配置"""
        settings = QSettings("ECHWorkers", "Client")
        self.server_edit.setText(settings.value("server", ""))
        self.listen_edit.setText(settings.value("listen", "127.0.0.1:30000"))
        self.token_edit.setText(settings.value("token", ""))
        self.routing_combo.setCurrentText(settings.value("routing", "global"))
        
    def save_settings(self):
        """保存配置"""
        settings = QSettings("ECHWorkers", "Client")
        settings.setValue("server", self.server_edit.text())
        settings.setValue("listen", self.listen_edit.text())
        settings.setValue("token", self.token_edit.text())
        settings.setValue("routing", self.routing_combo.currentText())
        
        QMessageBox.information(self, "保存成功", "配置已保存")
        
    def start_proxy(self):
        """启动代理服务"""
        server = self.server_edit.text().strip()
        listen = self.listen_edit.text().strip()
        token = self.token_edit.text().strip()
        routing = self.routing_combo.currentText()
        
        if not server:
            QMessageBox.warning(self, "配置错误", "请输入服务地址")
            return
            
        if not listen:
            listen = "127.0.0.1:30000"
            
        # 构建命令
        cmd = ["./ech-workers", "-f", server, "-l", listen, "-routing", routing]
        
        if token:
            cmd.extend(["-token", token])
            
        self.log(f"启动命令: {' '.join(cmd)}")
        
        try:
            # 检查文件是否存在
            if not os.path.exists("./ech-workers"):
                self.log("错误: 未找到ech-workers可执行文件")
                QMessageBox.critical(self, "启动失败", "未找到ech-workers可执行文件")
                return
                
            # 设置可执行权限
            os.chmod("./ech-workers", 0o755)
            
            # 启动进程
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=False,
                cwd=os.getcwd()
            )
            
            # 启动日志线程
            self.log_thread = LogThread(self.process)
            self.log_thread.log_signal.connect(self.log)
            self.log_thread.start()
            
            # 更新界面状态
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.status_label.setText("状态: 运行中")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.log("代理服务已启动")
            
        except Exception as e:
            self.log(f"启动失败: {str(e)}")
            QMessageBox.critical(self, "启动失败", f"无法启动代理服务: {str(e)}")
            
    def stop_proxy(self):
        """停止代理服务"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                self.process = None
                
                if self.log_thread:
                    self.log_thread.running = False
                    self.log_thread.wait()
                    self.log_thread = None
                    
                self.start_btn.setEnabled(True)
                self.stop_btn.setEnabled(False)
                self.status_label.setText("状态: 已停止")
                self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
                self.log("代理服务已停止")
                
            except Exception as e:
                self.log(f"停止失败: {str(e)}")
                
    def log(self, message):
        """记录日志"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_edit.append(f"[{timestamp}] {message}")
        # 滚动到最后
        self.log_edit.verticalScrollBar().setValue(self.log_edit.verticalScrollBar().maximum())
        
    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.process:
            reply = QMessageBox.question(
                self, "确认退出", "代理服务正在运行，确定要退出吗？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.stop_proxy()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    """主函数"""
    try:
        app = QApplication(sys.argv)
        
        # 设置应用图标
        if os.path.exists("app_icon.png"):
            app.setWindowIcon(QIcon("app_icon.png"))
            
        window = ECHWorkersGUI()
        window.show()
        
        # 处理Android返回键
        def handle_android_back():
            if window.isVisible():
                window.close()
                return True
            return False
            
        # 为Android平台设置返回键处理
        if hasattr(app, 'installEventFilter'):
            from PyQt5.QtCore import QEvent
            class BackButtonFilter(QObject):
                def eventFilter(self, obj, event):
                    if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Back:
                        return handle_android_back()
                    return super().eventFilter(obj, event)
                    
            filter_obj = BackButtonFilter()
            app.installEventFilter(filter_obj)
            
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"应用启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
