#!/bin/bash
set -eu
pbr="env /data/data/com.termux/files/home/.config/pianobar/pianobar.sh"
termux-notification --type media --media-next "$pbr next || termux-toast next failed" --media-pause "$pbr p || termux-toast pause failed" --media-play "$pbr play || termux-toast play failed" --media-previous "termux-toast cant go previous" --title pianobar --id pianobar --content "foo"

