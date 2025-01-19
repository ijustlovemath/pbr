# pbr - a pianobar client for Termux

## Installing

1. Install prerequisites

```
pkg install git pianobar pulseaudio
```

2. Create a config file for libao

### ~/.libao
```
default_driver=pulse
```

3. Fill in your user credentials 

### ~/.config/pianobar/config

```
user = pandora.username@email.com
password = sup3rs4f3p4ssw0rd
event_command = /data/data/com.termux/files/home/.config/pianobar/pbn.sh
```

4. Make requisite directories

```
mkdir -p ~/.local/usr/bin
mkdir -p ~/.local/tmp
```

5. Clone this repo, and copy the contents into `~/.config/pianobar`

```
git clone https://github.com/ijustlovemath/pbr ~/.local/tmp/pbr
mv ~/.local/tmp/pbr/* ~/.config/pianobar/
```

6. Install the symlinks

```
pushd ~/.config/pianobar
ln -s $(readlink -f media-notif.sh) ~/.local/usr/bin/pbr
ln -s $(readlink -f pianobar.sh) ~/.local/usr/bin/cpbr
ln -s $(readlink -f pbq.sh) ~/.local/usr/bin/pbq
ln -s $(readlink -f pbs.sh) ~/.local/usr/bin/pbs
```

7. (optional) update your path to make the whole thing usable

in your bash/zshrc:

```
export PATH="$PATH:~/.local/usr/bin"
```

# Usage

## Spawn pulseaudio

`pulseaudio --daemon`

## Spawn a media notification

`pbr`

Press the play/pause button to make it play
Press next to skip to next song

## Download the current song

`cpbr d`

## Like/Dislike the current song

`cpbr +/-`

## Spawn a notification with current song info

/!\ warning! this may cause increased battery usage

This command will hang, refreshing the notification once per second

`pbs`
