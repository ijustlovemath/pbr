from dataclasses import dataclass
import typing
import re
from collections import defaultdict
import sys
from pathlib import Path
from urllib.request import urlretrieve as httpget

root = Path(__file__).parents[0]

@dataclass
class Url:
    url: str

    def save(self, path: Path):
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
    def sigfile(cls, path: Path, sigfile: Path):
        """communicate where to find current assets to control-pianobar"""
        with open(sigfile, "w") as f:
            f.write(str(path))

    @classmethod
    def dl_dest(cls, bn):
        cls.sigfile(bn.dldest(), root / "downloaddir")

    @classmethod
    def dl_name(cls, bn):
        cls.sigfile(bn.dlname(), root / "downloadname")

    @classmethod
    def coverart(cls, bn):
        path = root / "albumart" / f"{bn.artist}-{bn.album}.jpg".replace("/", "_")
        cls.sigfile(path, root / "artname")
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
    artistNext: list[str]
    titleNext: list[str]
    albumNext: list[str]
    coverArtNext: list[Url]
    ratingNext: list[int]
    detailUrlNext: list[Url]
    songDurationNext: list[int]
    stationCount: int
    station: list[str]

    def save_metadata(self):
        # getter retrieves the url
        # formatter formats a path to save to, given the base object
        for getter, formatter in mdf.items():
            path = formatter(self)
            url = getter(self)
            url.save(path)

        for sigfiler in mdf.sigfiles.values():
            sigfiler(self)


    @property
    def songname(self):
        return f"{self.artist} - {self.title}"

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
        return self.coverArt

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

try:
    data = BarNotif(**dd)
except TypeError:
    quit()

data.save_metadata()
