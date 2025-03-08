#!/data/data/com.termux/files/usr/bin/bash
set -eu
root="/data/data/com.termux/files/home/.config/pianobar"
pbr="env /data/data/com.termux/files/home/.config/pianobar/pianobar.sh"
pbos="env python /data/data/com.termux/files/home/.config/pianobar/open_in_spotify.py"
focus="env am start -n com.termux/com.termux.app.TermuxActivity 2>/dev/null 1>&2; bash $0"
termux-notification --type media --media-next "$pbr next || termux-toast next failed" --media-pause "$pbr p || termux-toast pause failed" --media-play "$pbr play || termux-toast play failed" --media-previous "termux-toast Opening in Spotify...; $pbos" --title pianobar --id pianobar --content "-"
termux-notification --button3 "<3" --button3-action "$pbr + | termux-toast" --button2 "\/" --button2-action "$pbr d | termux-toast" --button1 "</3" --button1-action "$pbr - | termux-toast" --title pianobar-tools --id pianobar_tools --content " "
# maybe add a notification to url encode and open a spotify search
# spotify:search:track%3A%22castle%20on%20the%20hill%22%20artist%3A%22ed%20sheeran%22
# use termux-open-url

# pipe stdin to 
# spawn pianobar if it's not already running
[[ ! -n "$(pidof pianobar)" ]] && cpbr p
