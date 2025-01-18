#!/data/data/com.termux/files/usr/bin/bash

while true; do
	# pianobar status
	pbq | termux-notification --title "Now Playing" --ongoing --id "pbs"
#	sleep 3
done
