__doc__ = "pianobar query -- curently just song status"
import sys
from pathlib import Path
import shutil
import string
root = Path(__file__).parents[0]
cache = root / "cache"
cache.mkdir(parents=True, exist_ok=True)

lines = open(root / "log", "r", encoding="utf-8").readlines()

def status(s, **kwargs):
    s = s.replace("[2K", "")
    print(''.join(c for c in s if c in string.printable), **kwargs)

def parse(durline):
    try:
        _, duration = durline.split("/")
        start, end = duration.split(":")
    except ValueError as e:
        print(durline, e, file=sys.stderr)
        raise e
    duration = ":".join([start, end[:2]])
    return duration, cache / duration

def save_song(details, durline):
#    shutil.rmtree(cache)
    duration, fname = parse(durline)
    with open(fname, "w") as f:
        f.write(details)

def recall_song(durline):
    duration, fname = parse(durline)
    if fname.exists():
        return open(cache / duration, "r").read()
    return "no song name cached for current duration"


songs = [line for line in lines if "|>" in line]
durations = [line for line in lines if "#" in line]


if songs:
    status(songs[-1], end="")
    save_song(songs[-1], durations[-1])
else:
    status(recall_song(durations[-1]), end="")

status(durations[-1], end="")
