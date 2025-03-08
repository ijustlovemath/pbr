import urllib.parse as parse
from pathlib import Path
from os import system

root = Path(__file__).parents[0]
with open(root / "downloadname") as f:
    raw = f.readline().rstrip()
    artist_song = raw.split(" - ")
    if len(artist_song) < 2:
        artist = ""
        song = artist_song[0]
    elif len(artist_song) > 2:
        artist = ""
        song = raw
    else:
        artist, song = artist_song
    
query = f'''{artist} {song}'''


system(f"env termux-open-url spotify:search:{parse.quote_plus(query)}")
