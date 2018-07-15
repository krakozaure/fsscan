from functools import partial
from pathlib import Path


__all__ = [
    "cast_to_Path",
    "cast_to_Path_str",
    "cast_to_str",
    "convert_entries",
]


def convert_entries(entries, modifier):
    return (modifier(entry) for entry in entries)


def as_Path_str(item):
    return str(Path(item))


# Predefined callbacks
cast_to_str = partial(convert_entries, modifier=str)
cast_to_Path = partial(convert_entries, modifier=Path)
cast_to_Path_str = partial(convert_entries, modifier=as_Path_str)
