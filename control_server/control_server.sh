#!/bin/bash

# 파라미터 읽기
SERVER_IP=$1
ACTION=$2
PASSWORD=$3
SERVICE=$4
USER_NAME=$5

# 입력 검증
if [[ -z "$SERVER_IP" || -z "$ACTION" || -z "$PASSWORD" ]]; then
    echo "Usage: $0 <server_ip> <action> <password>"
    exit 1
fi

if [[ "$ACTION" != "start" && "$ACTION" != "stop" && "$ACTION" != "restart" ]]; then
    echo "Invalid action: $ACTION. Use start, stop, or restart."
    exit 1
fi

# SSH 접속 및 sudo 명령 실행
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USER_NAME@$SERVER_IP" "echo $PASSWORD | sudo -S systemctl $ACTION $SERVICE" 2>&1

# 실행 결과 출력
if [[ $? -eq 0 ]]; then
    echo "Service $SERVICE $ACTION on $SERVER_IP was successful."
else
    echo "Failed to $ACTION service $SERVICE on $SERVER_IP."
fi
