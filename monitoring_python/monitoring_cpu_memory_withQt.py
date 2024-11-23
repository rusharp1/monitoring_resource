import psutil
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox


class ResourceMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resource Monitor")
        self.root.geometry("300x200")

        self.process_name_label = tk.Label(root, text="모니터링할 프로세스명:")
        self.process_name_label.pack(pady=10)

        self.process_name_entry = tk.Entry(root)
        self.process_name_entry.pack(pady=5)

        self.duration_label = tk.Label(root, text="측정 시간 (초 단위):")
        self.duration_label.pack(pady=10)

        self.duration_entry = tk.Entry(root)
        self.duration_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="시작", command=self.start_monitoring)
        self.start_button.pack(pady=20)

    def start_monitoring(self):
        process_name = self.process_name_entry.get()
        try:
            monitoring_duration = int(self.duration_entry.get())
            if monitoring_duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("입력 오류", "0 이상의 숫자를 입력해 주세요.")
            return

        data = self.monitoring_resource_usage(process_name, monitoring_duration)
        if data:
            df = pd.DataFrame(data, columns=['Time', 'CPU Usage (%)', 'Memory Usage (MB)'])
            df = df.iloc[1:]  # 첫 번째 측정값(0초)을 제외함

            self.display_results(df)
            self.plot_resource_usage(df)
        else:
            messagebox.showerror("오류", "해당 프로세스를 찾을 수 없습니다.")

    def monitoring_resource_usage(self, process_name, monitoring_duration):
        data = []
        cores = psutil.cpu_count(logical=True)
        
        for _ in range(monitoring_duration + 1):
            cpu_usage = 0
            memory_usage = 0
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            processes = [
                proc for proc in psutil.process_iter(['name', 'pid'])
                if process_name.lower() in proc.info['name'].lower()
            ]

            if processes:
                for proc in processes:
                    cpu_usage += proc.cpu_percent(interval=0) / cores
                    memory_usage += proc.memory_info().rss / (1024 * 1024)

                data.append([timestamp, cpu_usage, memory_usage])
            time.sleep(1)
        return data

    def display_results(self, df):
        results_window = tk.Toplevel(self.root)
        results_window.title("Monitoring Results")
        
        text = tk.Text(results_window)
        text.insert(tk.END, df.to_string(index=False))
        text.pack()

    def plot_resource_usage(self, df):
        plt.figure(figsize=(12, 6))

        plt.subplot(2, 1, 1)
        plt.plot(df['Time'], df['CPU Usage (%)'], label='CPU Usage (%)', color='blue', marker='o')
        plt.xlabel('Time')
        plt.ylabel('CPU Usage (%)')
        plt.title('CPU Usage Over Time')
        plt.xticks(rotation=45)
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(df['Time'], df['Memory Usage (MB)'], label='Memory Usage (MB)', color='red', marker='o')
        plt.xlabel('Time')
        plt.ylabel('Memory Usage (MB)')
        plt.title('Memory Usage Over Time')
        plt.xticks(rotation=45)
        plt.legend()

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceMonitorApp(root)
    root.mainloop()
