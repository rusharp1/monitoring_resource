import sys
import subprocess
import re
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, QFormLayout

class ServiceController:
    def __init__(self):
        self.server_ip = ""
        self.action = ""
        self.password = ""
        self.service_name = ""
        self.user_name = ""
        self.bash_script = ""
        self.action_value = {"1": "start", "2": "stop", "3": "restart"}

    # IP 유효성 검사
    def get_valid_ip(self, ip_input):
        if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip_input):
            octets = ip_input.split(".")
            if all(0 <= int(octet) <= 255 for octet in octets):
                self.server_ip = ip_input
                return True
            else:
                return False
        else:
            return False

    # 액션 유효성 검사
    def get_valid_action(self, action_input):
        if action_input in self.action_value:
            self.action = self.action_value[action_input]
            return True
        else:
            return False
        
    def is_valid_name(self, user_name):
        return bool(re.match(r"^[a-zA-Z0-9_\-\.]+$", user_name))

    # Bash 스크립트 실행
    def run_bash(self):
        # 현재 파일의 디렉토리 경로
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.bash_script = current_dir + "/control_server.sh"
        print(f"Running script: {self.bash_script}")
        
        try:
            result = subprocess.run(
                ["bash", self.bash_script, self.server_ip, self.action, self.password, self.service_name, self.user_name],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 출력 결과
            return result.stdout, result.stderr
        except FileNotFoundError:
            return None, f"{self.bash_script} not found or not executable."

class ServiceControllerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.controller = ServiceController()
        
        self.setWindowTitle("Service Controller")
        self.setGeometry(100, 100, 400, 300)
        
        # 레이아웃 설정
        layout = QVBoxLayout()
        
        self.ip_label = QLabel("Enter the server IP address (ex. 192.168.0.1):")
        self.ip_input = QLineEdit(self)
        
        self.action_label = QLabel("Select action:")
        self.action_combobox = QComboBox(self)
        self.action_combobox.addItem("Start", "1")
        self.action_combobox.addItem("Stop", "2")
        self.action_combobox.addItem("Restart", "3")
        
        self.password_label = QLabel("Enter the sudo password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # 비밀번호는 입력 시 보이지 않도록 설정
        
        self.sn_label = QLabel("Enter the service name:")
        self.sn_input = QLineEdit(self)
        
        self.un_label = QLabel("Enter the Linux user name:")
        self.un_input = QLineEdit(self)

        self.result_label = QLabel("")
        
        # 실행 버튼
        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run_script)
        
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.action_label)
        layout.addWidget(self.action_combobox)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.sn_label)
        layout.addWidget(self.sn_input)
        layout.addWidget(self.un_label)
        layout.addWidget(self.un_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)

    def run_script(self):
        # 사용자 입력 값
        ip_input = self.ip_input.text().strip()
        action_input = self.action_combobox.currentData()
        password_input = self.password_input.text().strip()
        service_name_input = self.sn_input.text().strip()
        user_name_input = self.un_input.text().strip()
        
        # IP 주소와 액션 유효성 검사
        if not self.controller.get_valid_ip(ip_input):
            self.result_label.setText("Invalid IP address format.")
            return
        
        if not self.controller.get_valid_action(action_input):
            self.result_label.setText("Invalid action selected.")
            return
        
        if not self.controller.is_valid_name(service_name_input):
            self.result_label.setText("Invalid service name format.")
            return

        if not self.controller.is_valid_name(user_name_input):
            self.result_label.setText("Invalid user name format.")
            return

        
        # 비밀번호를 설정하고 bash 스크립트를 실행
        self.controller.password = password_input
        self.controller.service_name = service_name_input
        self.controller.user_name = user_name_input
        output, error = self.controller.run_bash()
        
        if output:
            self.result_label.setText(f"Output:\n{':'.join(output.split(':')[1:]).strip()}")
        else:
            self.result_label.setText(f"Error:\n{error}")

# PyQt5 애플리케이션 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServiceControllerApp()
    window.show()
    sys.exit(app.exec_())