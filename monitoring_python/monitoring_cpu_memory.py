import psutil
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt

"""주어진 리소스의 통계 정보를 출력하는 함수."""
def print_stats(df, resource_name):
    if df.empty:
        print(f"{resource_name} 데이터가 없습니다.")
        return
    
    # 원하는 통계 정보 추출
    min_val = df[resource_name].min()
    max_val = df[resource_name].max()
    avg_val = df[resource_name].mean()
    
    # 데이터 프레임으로 통계 데이터 정리
    stats_df = pd.DataFrame({
        'Metric': ['Min', 'Max', 'Avg'],
        resource_name: [min_val, max_val, avg_val]
    })
    
    # 가독성을 높이기 위해 소수점 포맷 지정
    stats_df[resource_name] = stats_df[resource_name].map('{:.2f}'.format)
    
    print(f"\n--- {resource_name} Summary Statistics ---")
    print(stats_df.to_string(index=False))  # 인덱스 숨김으로 출력

"""CPU 및 메모리 사용량을 그래프로 표시하는 함수."""
def plot_resource_usage(df):

    plt.figure(figsize=(12, 6))

    def plot_single_resource(y_data, title, ylabel, color):
        """단일 리소스의 그래프를 그리는 내부 함수."""
        plt.plot(df['Time'], y_data, label=ylabel, color=color, marker='o')
        plt.xlabel('Time')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=45)  # x축 시간 레이블 회전
        plt.legend()

    # CPU 사용량 그래프
    plt.subplot(2, 1, 1)
    plot_single_resource(df['CPU Usage (%)'], 'CPU Usage (%)', 'CPU Usage (%)', 'blue')

    # 메모리 사용량 그래프
    plt.subplot(2, 1, 2)
    plot_single_resource(df['Memory Usage (MB)'], 'Memory Usage (MB)', 'Memory Usage (MB)', 'red')

    plt.tight_layout()  # 그래프 레이아웃 최적화
    plt.show()

def monitoring_resource_usage(process_name, monitoring_duration):
    data = []
    
    cores = psutil.cpu_count(logical=True)
    # 모니터링 주기 및 측정 시간 설정 (초 단위)
    interval = 0.1  # 0.1초 대기 후 바로 측정.
    
    # 일정 시간동안 process 의 사용량을 측정하여 cpu, memory 측정량 저장.
    for _ in range(monitoring_duration + 1):
        cpu_usage = 0
        memory_usage = 0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = timestamp[2:]

        processes = [
            proc for proc in psutil.process_iter(['name', 'pid'])
            if process_name.lower() in proc.info['name'].lower()
            ]
        
        if processes:
            for proc in processes:
                cpu_usage += proc.cpu_percent(interval=0)/cores
                memory_usage += proc.memory_info().rss / (1024 * 1024)
        
            data.append([timestamp, cpu_usage, memory_usage])
        time.sleep(1)
    return data

def main():

    # 모니터링할 프로세스 이름
    process_name = input("모니터링할 프로세스명 : ")
    while True: 
        monitoring_duration = input("측정 시간 (초 단위) : ")
        try:
            # 정수로 변환 시도
            monitoring_duration = int(monitoring_duration)
            if monitoring_duration <= 0:
                print("0 이상의 숫자를 입력해 주세요.")
                continue
            break  # 올바른 값이 입력되면 루프 종료
        except ValueError:
            print("잘못된 입력입니다. 숫자만 입력해 주세요.")

    # 데이터 저장을 위한 리스트 초기화
    data = monitoring_resource_usage(process_name, monitoring_duration)

    if data:
        # 데이터 프레임 생성
        columns = ['Time', 'CPU Usage (%)', 'Memory Usage (MB)']
        df = pd.DataFrame(data, columns=columns)

        # 첫 번째 측정값(0초)을 제외하고 데이터 프레임에서 슬라이싱
        df = df.iloc[1:] if len(df) > 1 else df  # 첫 번째 행 제외

        # 결과 출력
        print("\n--- Monitoring Results ---")
        print(df)

        # CPU와 메모리 사용량 통계 출력
        print("\n--- Summary Statistics ---")
        print_stats(df, 'CPU Usage (%)')
        print_stats(df, 'Memory Usage (MB)')


        # CPU와 메모리 사용량 시각화
        plot_resource_usage(df)
    else:
        print("해당 프로세스를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()