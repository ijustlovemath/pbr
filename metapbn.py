import re
from pprint import pprint
from collections import defaultdict


with open("pbn.txt", "r") as f:
    lines = f.readlines()

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



def infer(elt):
    try:
        int(elt)
        return "int"
    except ValueError:
        pass
    if "http" in elt:
        return "Url"
    return "str"
print("from dataclasses import dataclass\n\n@dataclass\nclass BarNotif:")
for name, data in dd.items():
    dtype = infer(data[0])
    if len(data) == 1:
        print(f"\t{name}: {dtype}")
    else:
        print(f"\t{name}: list[{dtype}]")

#pprint(dd)
