#!/bin/bash
while true
do
  batt=`pmset -g batt | grep -Eo "\d+%" | cut -d% -f1`
  if [ $batt -le 20 -o $batt -ge 80 ]; then
    date +"%R Battery too low or too high. Notifying..."
    cd /Users/yj048444/Documents/my_github/ButlerBot
    ./BatteryBot.py $batt
    sleep 600
  fi
done
