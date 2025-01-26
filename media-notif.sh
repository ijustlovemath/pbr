#!/bin/bash
set -eu
root="/data/data/com.termux/files/home/.config/pianobar"
pbr="env /data/data/com.termux/files/home/.config/pianobar/pianobar.sh"
termux-notification --type media --media-next "$pbr next || termux-toast next failed" --media-pause "$pbr p || termux-toast pause failed" --media-play "$pbr play || termux-toast play failed" --media-previous "termux-toast cant go previous" --title pianobar --id pianobar --content "foo"
termux-notification --button3 "<3" --button3-action "$pbr + | termux-toast" --button2 "\/" --button2-action "$pbr d | termux-toast" --button1 "</3" --button1-action "$pbr - | termux-toast" --title pianobar-tools --id pianobar_tools --content " "

# pipe stdin to 
# spawn pianobar if it's not already running
[[ ! -n "$(pidof pianobar)" ]] && cpbr p
