max_cpu=0
max_mem=0

for ((i=0; i<60; i++)); do
    read cpu rss <<< $(ps aux | grep "프로세스명" | awk '{sum+=$3; rss+=$6} END {print sum, rss}')

    # MB로 변환
    mem_mb=$(echo "scale=2; $rss / 1024" | bc)

    (( $(echo "$cpu > $max_cpu" | bc -l) )) && max_cpu=$cpu
    (( $(echo "$mem_mb > $max_mem" | bc -l) )) && max_mem=$mem_mb
    echo "CPU: $cpu%, Memory : $mem_mb MB"
    sleep 1
done

echo "최대 CPU : $max_cpu%, 최대 Memory : $max_mem MB"
