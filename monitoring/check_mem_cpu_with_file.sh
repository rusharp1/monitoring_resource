max_cpu=0
max_mem=0
temp_file=$(mktemp) #임시파일 생성, 변수에 경로 저장.

# 프로세스 이름을 변수로 받기.
process_name = ""
# 스페이스 개수만큼 카운트
space_count = $(echo "$process_name" | grep -o " " | wc -l)
cpu_field = $((3 + space_count))
mem_field = $((8 + space_count))

# top 명령을 사용하여 CPU와 메모리 사용량 추출
# 내용이 너무 길 때, 부적절한 메시자가 나오는 것을 파일로 만들어 방지.
top -l 60 -s 1 | grep "$process_name" > "$temp_file"

# 각 라인에 대해 처리
while read -r line; do
    # CPU와 메모리 값 추출
    cpu=$(echo "$line" | awk -v field="$cpu_field" '{print $field}')
    mem=$(echo "$line" | awk -v field="$mem_field" '{print $field}')

    # 최대값 갱신
    (( $(echo "$cpu > $max_cpu" | bc -l) )) && max_cpu=$cpu
    (( $(echo "$mem > $max_mem" | bc -l) )) && max_mem=$mem
    
    printf "CPU: %-5s%%, Memory: %-5s\n" "$cpu" "$mem"
done < "$temp_file"  # 파일에서 읽어오기

# 최댓값 출력
echo "-----최대 CPU, Memory 값-----"
printf "CPU: %-5s%%, Memory: %-5s\n" "$max_cpu" "$max_mem"

#임시 파일 삭제
rm "$temp_file"
