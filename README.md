<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=BDBDC8&amp;height=150&amp;section=header">

# CPU 및 메모리 사용량 모니터링 스크립트
> 이 프로젝트는 지정한 프로세스의 CPU 및 메모리 사용량을 모니터링하고 60초 동안의 최대 사용량을 출력하는 Bash 스크립트 입니다.

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/rusharp1/shell-programming&count_bg=%233B3B3B&title_bg=%23B178BE&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

## 1. monitoring
### 1. check_mem_cpu_with_file.sh
1. 프로젝트 개요
* 이 스크립트는 지정한 프로세스의 CPU 및 메모리 사용량을 60초 동안 측정한 뒤, 해당 시간 동안의 최고 사용량을 출력합니다.

2. 기능 설명
* 지정한 프로세스의 CPU 및 메모리 사용량을 측정합니다.
* 각 측정치의 최대값을 기록하여 최종적으로 출력합니다.
* 임시 파일을 사용하여 프로세스 정보를 저장합니다.


### 2. 참고사항
* 스크립트가 실행된 후 60초 동안 해당 프로세스의 사용량을 모니터링하며, 60초가 지나면 각 측정치와 함깨 최대값을 출력합니다.
* 스크립트 이름을 변경하거나 파일명을 잘못 입력하면 작동하지 않으니 주의해 주세요.

### 3. 설치 및 실행 방법
1. 터미널을 엽니다.
   * 우측 상단의 검색 아이콘을 클릭하고 'terminal'을 입력하여 터미널을 실행합니다.
3. 스크립트를 포함한 디렉토리로 이동합니다.
    ```
    cd ./monitoring
    ```
3. 스크립트 내 프로세스 이름을 정의합니다.
    ```
    process_name="프로세스명"
    ```
4. 스크립트를 실행합니다.
    ```
    ./파일명.sh
    ```


## 2. LICENSE

이 프로젝트는 [MIT License](LICENSE) 에 따라 라이선스가 부여됩니다.

<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=BDBDC8&amp;height=150&amp;section=footer">
