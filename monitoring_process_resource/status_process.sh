#!/bin/bash

# 프로세스 이름 또는 PID를 첫 번째 인자로 받음
PROCESS=$1

# 프로세스가 존재하는지 확인
if [[ -z "$PROCESS" ]]; then
    echo "Usage: $0 <process_name_or_pid>"
    exit 1
fi

# 프로세스가 실행 중인지 확인
pid=$(pgrep -x "$PROCESS" || echo "")
if [[ -z "$pid" ]]; then
    echo "Process '$PROCESS' not found"
    exit 1
fi
# CPU와 메모리 사용량 가져오기
ps_output=$(ps -p $pid -o %cpu,rss,command)

# 네트워크 사용량 가져오기
net_output=$(nettop -P -L 1 | grep "$pid")

# 출력

echo "$ps_output"\
echo "$net_output"