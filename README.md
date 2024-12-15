<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=BDBDC8&amp;height=150&amp;section=header">

# monitoring_process_resource

> python 과 shell script를 사용하여 특정 프로세스의 시스템 자원 사용량 (CPU, 메모리, 네트워크)를 실시간으로 모니터링 하는 프로그램.

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/rusharp1/monitoring_resource&count_bg=%233B3B3B&title_bg=%23B178BE&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

## 1. monitoring_resource

### 1\. 프로젝트 목록
#### 1. 프로젝트 개요 (Introduction)
   - 이 프로젝트는 Python 과 Shell script 를 사용하여 특정 프로세스의 시스템 자원 사용량(CPU, 메모리, 네트워크)을 실시간으로 모니터링하는 PyQt5 기반 GUI 애플리케이션입니다.

#### 2. 파일 구조 및 기능 설명
1. 파일 구조
   ```
    Read_process_usage_withQt/  
    ├── Read_process_usage_withQt.py    # PyQt5 기반의 GUI 메인 코드  
    └── status_process.sh               # 프로세스 사용량 데이터 수집을 위한 Bash 스크립트  
   ```

2. Read_process_usage_withQt.py
   - PyQt를 기반으로 작성된 GUI애플리케이션
   - 사용자로부터 특정 프로세스 이름을 입력받고 해당 프로세스의 CPU, 메모리, 네트워크 사용량을 실시간으로 모니터링.
   - 그래프와 텍스트 출력 기능을 통해 데이터를 시각적으로 확인 가능하며 Excel파일로 내보내는 기능도 포함.
   - PyQt의 Qthread 를 활용해 UI의 응답성 유지

3. control_server.sh
   -  Bash 스크립트로 작성되어 프로세스 이름을 기반으로 CPU, 메모리, 네트워크 사용량 데이터를 수집.
   -  top, ps, ifconfig 등의 시스템 명령어를 활용해 실시간으로 프로세스와 관련된 시스템 자원 정보를 추출.
   -  수집된 데이터를 Python 스크립트에서 처리할 수 있도록 표준 출력 형태로 반환.

### 3\. 사전 요구사항 \(Prerequisites\)
#### 1. 필수 환경
* Macos, Linux (권장)
* Python 3.8 이상
#### 2. 필수 패키지  
* PyQt5 설치
* matplotlib 설치
* pandas 설치
* openpyxl 설치

### 4\. 설치 방법 \(Installation\)
1. PyQt5 를 설치합니다.
    ```
    pip install pyqt5
    ```
2. matplotlib를 설치합니다.
    ```
    pip install matplotlib
    ```
3. pandas를 설치합니다.
    ```
    pip install pandas
    ```
4. openpyxl을 설치합니다.
    ```
    pip install openpyxl
    ```
5. 프로젝트를 로컬에 클론합니다.
    ```
    git clone -b master https://github.com/rusharp1/monitoring_resource.git
    ```
    ↳ 이 때, monitoring_process_resource.py 와 status_process.sh가 같은 디렉토리에 위치해야 합니다.
3. 해당 프로젝트 위치로 이동합니다.
    ```
    cd ./monitoring_resource/monitoring_process_resource
    ```
5. python 파일을 실행합니다.

    ```
    monitoring_process_resource.py
    ```
 
### 5\. 사용 방법 \(Directions\)

1. 프로세스 정보 입력
  1. 측정 횟수 : 데이터를 몇 번 측정할지 입력합니다. 이때, 0을 입력하면 중지 버튼을 누를 때까지 무한으로 측정합니다.
  2. 측정 간격(s) : 프로세스 측정 간격을 초 단위로 설정합니다.
  3. 프로세스 명: 모니터링할 프로세스 이름 또는 PID를 입력합니다 (python 등).
2. 모니터링 시작
  1. "시작" 버튼을 클릭하면 모니터링이 시작됩니다.
  2. 프로세스 데이터가 실시간으로 화면에 표시됩니다.
3. 모니터링 중지
  1. "중지" 버튼을 클릭하면 모니터링이 종료됩니다.
  2. 측정 횟수가 0 이상의 정수일 경우, 중지 버튼을 누르지 않아도 횟수가 만료되면 모니터링이 중지됩니다.
4. 데이터 저장 및 시각화
  1. 모니터링이 완료되면 결과 데이터가 Excel파일로 저장됩니다.
  2. matplotlib를 사용하여 그래프로 시각화 됩니다.
ex) 아래는 python 프로그램의 데이터를 2초 간격으로 30번 측정하는 방법입니다. 
      - 측정 횟수: 30
      - 측정 간격(s) : 2
      - 프로세스 명 : python
      - 시작 버튼 클릭

### 6\. 주의 사항 (caution)

1. 이 프로그램은 기본적으로 Macos 및 Linux/Unix 기반 서버에서 동작하도록 설계되었습니다. 다른 운영 체제에서는 정상적으로 동작하지 않을 수 있습니다.
2. Windows에서도 작동할 수 있지만, `status_process.sh` 스크립트가 Bash 환경에 의존하므로 WSL 또는 다른 Bash 환경이 필요합니다.
3. GUI 애플리케이션을 장시간 실행 시, 그래프를 그리거나 엑셀 파일을 저장하는 데 시스템 리소스를 많이 사용할 수 있습니다.

## 2. LICENSE

이 프로젝트는 [MIT License](LICENSE) 에 따라 라이선스가 부여됩니다.

<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=BDBDC8&amp;height=150&amp;section=footer">
