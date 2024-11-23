max_cpu=0
max_mem=0

# top 명령을 사용하여 CPU와 메모리 사용량 추출
output=$(top -l 60 -s 1 | grep "프로세스명")

# 각 라인에 대해 처리
while read -r line; do
    # CPU와 메모리 값 추출
    cpu=$(echo "$line" | awk '{print $4}')
    mem=$(echo "$line" | awk '{print $9}')

    # 최대값 갱신
    (( $(echo "$cpu > $max_cpu" | bc -l) )) && max_cpu=$cpu
    (( $(echo "$mem > $max_mem" | bc -l) )) && max_mem=$mem
    
    printf "CPU: %-5s%%, Memory: %-5s\n" "$cpu" "$mem"
done <<< "$output"
Echo "-----최대 CPU, Memory 값-----"
printf "CPU: %-5s%%, Memory: %-5s\n" "$max_cpu" "$max_mem"
