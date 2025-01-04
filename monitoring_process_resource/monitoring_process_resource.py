import sys
import os 
import time
import subprocess
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QTextEdit, QLabel, QLineEdit, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
import statistics

class monitoring(QThread):
    update_signal = pyqtSignal(str, str, str, str)
    finished_signal = pyqtSignal(list)

    def __init__(self, total_time, interval, process_name):
        super().__init__()
        self.total_time = total_time
        self.interval = interval
        self.is_running = True
        self.time_list = []

        # 현재 디렉토리 경로 설정
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.script_path = self.current_dir + "/status_process.sh"
        self.process_name = process_name
        # self.process_name = 예: "python", 또는 특정 PID

        # CPU 사용량, 메모리 사용량, 네트워크 사용량

        self.current_time = "0"
        self.cpu_usage = "0 %"
        self.mem_usage = "0 MB"
        self.net_data = "0"
        self.received_bytes = "0 Mbps"

        self.times = []
        self.cpu_usages = []
        self.mem_usages = []
        self.sent_bytes_list = []
        self.received_bytes_list = []

    def run(self):
        self.time_list.clear()
        if self.total_time == 0:  # 무한 루프
            while self.is_running:
                self.monitoring()
                self.update_signal.emit(self.current_time,
                                            self.cpu_usage,
                                            self.mem_usage,
                                            self.received_bytes )
                time.sleep(self.interval)

        for _ in range(self.total_time):
            if not self.is_running:
                break
            self.monitoring()
            self.update_signal.emit(self.current_time,
                                    self.cpu_usage,
                                    self.mem_usage,
                                    self.received_bytes )
            time.sleep(self.interval)
        
        self.finished_signal.emit(self.time_list)

    def stop(self):
        self.is_running = False

    def monitoring(self):
        try:
            # 현재 시간 저장
            self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 쉘 명령어 실행 결과 가져오기
            self.result = subprocess.check_output(f"bash {self.script_path} '{self.process_name}'", shell=True, text=True)
            self.result = self.result.splitlines()

            # 결과가 1개 이상이면 CPU, 메모리, 네트워크 데이터 추출
            if len(self.result) > 1:
                self.cpu_usage = self.result[1].split()[0] + " %"
                self.mem_usage = self.result[1].split()[1]
                self.mem_usage = str(round(int(self.mem_usage) / 1024, 1)) + " MB"

                # 네트워크 데이터를 마지막 줄에서 추출
                net_data = self.result[-1].split(",")

                # 수신 바이트 처리
                self.received_bytes = net_data[4] if not (net_data[0] == '') else "0"
                self.received_bytes = "0" if self.received_bytes == '' else self.received_bytes
                self.received_bytes = str(round(int(self.received_bytes) / 125000, 1)) + " Mbps"

            # 각 데이터를 리스트에 추가
            self.times.append(self.current_time)
            self.cpu_usages.append(self.cpu_usage)
            self.mem_usages.append(self.mem_usage)
            self.received_bytes_list.append(self.received_bytes)

            # 로그 출력 (디버깅용)
            print(f"{self.current_time}\t\
                    {self.cpu_usage}\t\
                    {self.mem_usage}\t\
                    {self.received_bytes}")

        except Exception as e:
            print(f"{self.process_name} 를 찾을 수 없습니다. 다시한 번 확인해주세요. \n오류: {e}")
            self.cpu_usage = "0 %"
            self.mem_usage = "0 MB"
            self.received_bytes = "0 Mbps"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.times = []
        self.cpu_usages = []
        self.mem_usages = []
        self.sent_bytes_list = []
        self.received_bytes_list = []
    
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # 측정 시간 입력
        time_layout = QHBoxLayout()
        time_label = QLabel("측정 횟수 :")
        self.time_input = QLineEdit()
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_input)
        layout.addLayout(time_layout)

        # 측정 간격 입력
        interval_layout = QHBoxLayout()
        interval_label = QLabel("측정 간격(s):")
        self.interval_input = QLineEdit()
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_input)
        layout.addLayout(interval_layout)

        # 프로세스명 입력
        process_layout = QHBoxLayout()
        process_label = QLabel("프로세스 명:")
        self.process_input = QLineEdit()
        interval_layout.addWidget(process_label)
        interval_layout.addWidget(self.process_input)
        layout.addLayout(process_layout)

        self.button = QPushButton('시작', self)
        self.button.clicked.connect(self.toggleMonitoring)
        layout.addWidget(self.button)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.central_widget.setLayout(layout)

        self.worker = None

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Monitoring')
        self.show()

    def toggleMonitoring(self):
        # 입력값 검증

        try:
            total_time = int(self.time_input.text())
            interval = int(self.interval_input.text())
        except ValueError:
            self.text_edit.setText("올바른 숫자를 입력하세요.")
            return

        # 이미 실행 중인 워커가 있다면 중지
        if self.worker and self.worker.isRunning():
            self.button.setText('시작')
            self.worker.stop()
            return

        # 새 워커 생성 및 시작
        self.button.setText('중지')
        self.text_edit.clear()

        self.text_edit.append(f"{'Time':<34} | {'CPU Usage (%)':<15} | {'Memory Usage (KB)':<20} | {'received Bytes':<15}")
        self.text_edit.append("-" * 80)

        self.worker = monitoring(total_time, interval, self.process_input.text())
        self.worker.update_signal.connect(self.updateText)
        self.worker.finished_signal.connect(self.onMonitoringFinished)
        self.worker.start()

    def updateText(self, time, cpu, mem, RB ):
        # cpu = cpu + " %"
        # mem = mem + " MB"
        # RB = RB + " Mbps"
        formatted_text = f"{time:<20} |  {cpu:<24} |  {mem:<26} |  {RB:<15}"
        self.text_edit.append(formatted_text)
        if(cpu == '0 %' and mem == '0 MB'):
            self.text_edit.append(f"{self.process_input.text()} 를 찾을 수 없습니다. 다시한 번 확인해주세요. ")

        self.times.append(time)
        self.cpu_usages.append(cpu)
        self.mem_usages.append(mem)
        self.received_bytes_list.append(RB)
    def onMonitoringFinished(self, time_list):
        self.button.setText('시작')
        self.text_edit.append("\n측정 완료.")
        self.summary_values()

        ExcelExporte = ExcelExporter(self.times,
                                    self.cpu_usages,
                                    self.mem_usages,
                                    self.received_bytes_list)
        ExcelExporte.export_to_excel(f"monitoring_output_{self.times[0]}_{self.times[-1]}.xlsx")

        Graph = Graphing(self.times,
                         self.cpu_usages,
                         self.mem_usages,
                         self.received_bytes_list)
        Graph.plot_graph()

        self.times = []
        self.cpu_usages = []
        self.mem_usages = []
        self.sent_bytes_list = []
        self.received_bytes_list = []

    def print_max_values(self, label, data_list, key_value):
        max_value = max(data_list, key=key_value)
        max_index = data_list.index(max_value)

        self.text_edit.append("")
        self.text_edit.append(f"{label}")
        self.text_edit.append("-"*80)
        self.text_edit.append(f"{self.times[max_index]:<20} | {self.cpu_usages[max_index]:<24} | {self.mem_usages[max_index]:<26} | {self.received_bytes_list[max_index]:<15}")

    def print_average_values(self, label, data_list, unit_value):
        average_value = statistics.mean(float(item.split()[0]) for item in data_list)
        average_value = round(average_value, 1)
        self.text_edit.append(f"{label} : {average_value}{unit_value}")

    def summary_values(self):
        self.text_edit.append("")
        self.text_edit.append("평균 값")

        self.print_average_values('Average CPU Usage', self.cpu_usages, " %")
        self.print_average_values('Average Memory Usage', self.mem_usages, " MB")
        self.print_average_values('Average received Bytes', self.received_bytes_list, " Mbps")

        self.text_edit.append("")

        self.print_max_values('Max CPU Usage', self.cpu_usages, lambda x: float(x.split()[0]))
        self.print_max_values('Max Memory Usage', self.mem_usages, lambda x: float(x.split()[0]))
        self.print_max_values('Max received Bytes', self.received_bytes_list, lambda x: float(x.split()[0]))


class ExcelExporter:
    def __init__(self, times, cpu_usages, mem_usages, received_bytes):
        self.times = times
        self.cpu_usages = cpu_usages
        self.mem_usages = mem_usages
        self.received_bytes = received_bytes

    def export_to_excel(self, filename="monitoring_data.xlsx"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, filename)
        df = pd.DataFrame({
            'Time': self.times,
            'CPU Usage (%)': [cpu.split()[0] for cpu in self.cpu_usages],
            'Memory Usage (KB)': [mem.split()[0] for mem in self.mem_usages],
            'Received Bytes': self.received_bytes
        })
        df.to_excel(file_path, index=False)
        print(f"Data exported to {file_path}/{filename}")


class Graphing:
    def __init__(self, times, cpu_usages, mem_usages, received_bytes):
        self.times = times
        self.cpu_usages = cpu_usages
        self.mem_usages = mem_usages
        self.received_bytes = received_bytes

    def plot_graph(self):
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # CPU Usage 그래프
        ax1.set_xlabel('Time')
        ax1.set_ylabel('CPU Usage (%)', color='tab:red')
        ax1.plot(self.times, [float(cpu.split()[0]) for cpu in self.cpu_usages], color='tab:red', label='CPU Usage')
        ax1.tick_params(axis='y', labelcolor='tab:red')

        # Memory Usage 그래프
        ax2 = ax1.twinx()
        ax2.set_ylabel('Memory Usage (MB)', color='tab:blue')
        ax2.plot(self.times, [float(mem.split()[0]) for mem in self.mem_usages], color='tab:blue', label='Memory Usage')
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        # 네트워크 수신 바이트 그래프
        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('outward', 60))
        ax3.set_ylabel('Received Bytes', color='tab:green')
        ax3.plot(self.times, [float(byte.split()[0]) for byte in self.received_bytes], color='tab:green', label='Received Bytes')
        ax3.tick_params(axis='y', labelcolor='tab:green')

        ax1.set_xticklabels(self.times, rotation=45, ha='right')

        fig.tight_layout()
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())




# pyinstaller --onefile --windowed \
#   --hidden-import=matplotlib.backends.backend_qt5agg \
#   --hidden-import=openpyxl \
#   --hidden-import=openpyxl.cell._writer \
#   --add-data="/Users/kimsjin/coding/.venv/lib/python3.9/site-packages/matplotlib/mpl-data:matplotlib/mpl-data" \
#   --add-data="/Users/kimsjin/coding/monitoring_Qt/status_process.sh:./" \
#   Read_process_usage_withQt\ copy.py