#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <PID>"
  exit 1
fi

PID="$1"
total_kb_prev=0
while true; do
  total_kb=$(awk '
    BEGIN { sum=0; anon=0 }
    /^[0-9a-f]+-[0-9a-f]+/ {
        anon = ($2 ~ /rw-p/ && $4 == "00:00")
        next
    }
    anon && /^Rss:/ {
        sum += $2
    }
    END { print sum }
  ' "/proc/$PID/smaps")
  if [ "$total_kb" -ne "$total_kb_prev" ]; then
      echo "$(date +"%H, %M, %S, ") PID $PID anonymous rw-p RSS, ${total_kb}, kB"
  fi
  total_kb_prev="$total_kb"
  sleep 1
done
