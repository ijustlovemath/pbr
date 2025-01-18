install:
	mkdir -p ~/.local/usr/bin
	ln -s $(readlink -f media-notif.sh) ~/.local/usr/bin/pbr
	ln -s $(readlink -f pianobar.sh) ~/.local/usr/bin/cpbr
	ln -s $(readlink -f pbq.sh) ~/.local/usr/bin/pbq
	ln -s $(readlink -f pbs.sh) ~/.local/usr/bin/pbs
	$(ln -s $(readlink -f pbs.sh) ~/.local/usr/bin/pbs)


