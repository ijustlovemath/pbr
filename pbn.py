from dataclasses import dataclass, field
import typing
import re
from collections import defaultdict
import sys
import shutil
from pathlib import Path
from urllib.request import urlretrieve as httpget
from pprint import pformat as pp

root = Path(__file__).parents[0]

@dataclass
class Url:
    url: str

    def __bool__(self):
        return bool(self.url)

    def save(self, path: Path):
        if not self.url:
            print(f"No URL was found for the asset `{path}`\n{pp(dd)}", file=sys.stderr)
            return
        assert path is not None, "your Paths getter isnt implemented correctly, make sure to return"
        httpget(self.url, path)


class MetadataFactory:
    save_paths = {}
    sigfiles = {}
    def save_to(self, *, path: typing.Callable, enabled=True):
        def decorator(prop: property):
            # prop is.just a getter function, so its callable
            self.save_paths[prop] = path
            return prop
        return decorator

    def sigfile(self, *, path: typing.Callable, enabled=True):
        def decorator(prop: property):
            # prop is.just a getter function, so its callable
            self.sigfiles[prop] = path
            return prop
        return decorator

    def items(self):
        yield from self.save_paths.items()

mdf = MetadataFactory()

class Paths:
    @classmethod
    def backup(cls, sigfile: Path, history: int = 10):
        backups = root / "history"
        print = lambda *args, **kwargs: None
        if not data:
            # failed to parse, leave history intact
            return

        for i in range(history):
            tree = backups / f"{i}"
            tree.mkdir(parents=True, exist_ok=True)

        todel = history - 1

        fname = sigfile.parts[-1]

        candidate = backups / f"{todel}" / fname
        if candidate.exists():
            print(f"deleting {todel}/{fname}")
            candidate.unlink()


        # gotta go in reverse order, otherwise it just moves the same data
        for i in range(todel, 0, -1):
            candidate = backups / f"{i-1}" / fname
            print(f"moving {i}, {fname}, {candidate.exists()}")
            if candidate.exists():
                shutil.move(candidate, backups / f"{i}" / fname)

        print(f"saving initial to 0/{fname}")
        # must happen after the shuffle, to start
        shutil.copy(sigfile, backups / "0" / fname)

    @classmethod
    def sigfile(cls, content: str, sigfile: Path):
        """communicate where to find current assets to control-pianobar"""
        #print = lambda *args, **kwargs: None
        with open(sigfile, "r") as current:
            # this is expensive but realistically only a few ms
            if content in current.read():
                print("duplicate call detected, backups will not rotate")
            else:  
                cls.backup(sigfile)
        with open(sigfile, "w") as f:
            f.write(content)

    @classmethod
    def dl_dest(cls, content: str, bn):
        cls.sigfile(content, root / "downloaddir")

    @classmethod
    def dl_name(cls, content: str, bn):
        cls.sigfile(content, root / "downloadname")

    @classmethod
    def nowplaying(cls, content: str, bn):
        cls.sigfile(content, root / "nowplaying")

    @classmethod
    def coverart(cls, bn):
        path = root / "albumart" / f"{bn.artist}-{bn.album}.jpg".replace("/", "_")
        cls.sigfile(str(path), root / "artname")
        return path

@dataclass(kw_only=True, slots=True)
class BarNotif:
    stationName: str
    songStationName: str
    pRet: int
    pRetStr: str
    wRet: int
    wRetStr: str
    songPlayed: int
    artist: str
    title: str
    album: str
    coverArt: Url
    rating: int
    detailUrl: Url
    songDuration: int
    # These are sometimes missing so give them safe defaults
    # 'artistNext', 'titleNext', 'albumNext', 'coverArtNext', 'ratingNext', 'detailUrlNext', and 'songDurationNext'
    artistNext: list[str] = field(default_factory=lambda: [""])
    titleNext: list[str] = field(default_factory=lambda: [""])

    albumNext: list[str] = field(default_factory=lambda: [""])

    coverArtNext: list[Url] = field(default_factory=lambda: [""])

    ratingNext: list[int] = field(default_factory=lambda: ["0"])

    detailUrlNext: list[Url] = field(default_factory=lambda: [""])

    songDurationNext: list[int] = field(default_factory=lambda: ["0"])

    stationCount: int
    station: list[str]

    def save_metadata(self):
        # getter retrieves the url
        # formatter formats a path to save to, given the base object
        for getter, formatter in mdf.items():
            path = formatter(self)
            url = getter(self)
            url.save(path)

        # nothing to download, these are just special files to communicate state to cpbr
        for getter, sigfiler in mdf.sigfiles.items():
            content = getter(self)
            assert content is not None, f"{getter} much return a string"
            sigfiler(content.replace("/", "_"), self)


    @property
    def songname(self):
        return f"{self.artist} - {self.title}"

    
    @mdf.sigfile(path=Paths.nowplaying)
    def nowplaying(self):
        return f'"{self.title}" by {self.artist}'

    @property
    def songfile(self): # equivalent to filename()
        return self.songname

    @mdf.sigfile(path=Paths.dl_name)
    def dlname(self):
        return self.songfile


    @mdf.sigfile(path=Paths.dl_dest)
    def dldest(self):
        return self.songStationName or self.stationName

    @mdf.save_to(path=Paths.coverart)
    def coverart(self):
        # sometimes coverArt is empty in which case coverArtNext is correct
        return self.coverArt or self.coverArtNext[0]

    def __post_init__(self):
        for name, dtype in self.__annotations__.items():
            current = getattr(self, name)
            assert current
            if len(current) == 1:
                setattr(self, name, dtype(current[0]))
            else:
                (inner,) = typing.get_args(dtype)
                coerced = list(map(inner, current))
                setattr(self, name, coerced)

            

lines = sys.stdin.readlines()
dd = defaultdict(list)
for line in lines:
    line = line.rstrip()
    pattern = r"([A-Za-z]+)(\d*)"
    a = line.split("=", 1)
    key, data = a
    match = re.match(pattern, key)
    if not match:
        raise ValueError(line)
    key = match.group(1)
#    print(key, match.group(2)
    dd[key].append(data)

data = None
try:
    data = BarNotif(**dd)
except TypeError as e:
    print(f"Had a problem with parsing incoming data: {pp(dd)}\n{e}", file=sys.stderr)
    quit()

data.save_metadata()
