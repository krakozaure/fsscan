from collections import Sequence
from enum        import IntEnum
from fnmatch     import fnmatchcase
from functools   import partial
from pathlib     import Path

try:
    from os import scandir, DirEntry  # PY>=3.5  noqa
except ImportError as exc:
    from scandir import scandir, DirEntry  # PY<3.5  noqa



class EntryType(IntEnum):
    FILE = 1
    DIR  = 2
    BOTH = 3


DEFAULT_CALLBACK = None
FOLLOW_LINKS     = False


# ##### Search functions ###


def run(directory='.', patterns=None, wanted_type=EntryType.BOTH,
        recursive=False, onerror=None, callback=None):
    """Scan a directory and return the mathing entries

    Parameters
    ----------
    directory : (str or Path), optional
        Directory to scan
    patterns : (str or sequence of str), optional
        Patterns to look for in the entry name
    wanted_type : (EntryType or int), optional
        Type of entry to return (file, dir or both)
    recursive : bool, optional
        Scan directory recursively or not
    onerror : (None or callable), optional
        Callable to use when an error occured (OSError, PermissionError)
    callback : (None or callable), optional
        Callable to use after the scan (e.g. entries cast)

    Returns
    -------
    Generator
        Entries returned by the scandir function
    """

    directory = str(Path(directory))

    if isinstance(patterns, str) or not isinstance(patterns, Sequence):
        patterns = (patterns, )
    patterns = tuple(p for p in set(patterns) if p and isinstance(p, str))

    results  = _scan(directory, patterns, wanted_type, recursive, onerror)
    callback = callback if callable(callback) else DEFAULT_CALLBACK
    return callback(results) if callable(callback) else results


def _scan(directory, patterns, wanted_type, recursive, onerror):

    try:
        entries = scandir(directory)
    except Exception as error:
        if callable(onerror):
            onerror(error)
        return

    for entry in entries:

        entry_is_dir = entry.is_dir(follow_symlinks=FOLLOW_LINKS)

        if _match_type(wanted_type, entry_is_dir):
            if not patterns or _match_pattern(entry.name, patterns):
                yield entry

        if recursive and entry_is_dir:
            yield from _scan(entry.path, patterns, wanted_type, recursive, onerror)


def _match_type(wanted_type, entry_is_dir):
    return (wanted_type == 3) \
        or (wanted_type == 2 and entry_is_dir) \
        or (wanted_type == 1 and not entry_is_dir)


def _match_pattern(entry, patterns):
    # fnmatchcase(a.lower(), b.lower()) 1.5-4x faster than fnmatch(a, b)
    return any(
        fnmatchcase(entry.lower(), pattern.lower())
        for pattern in patterns
    )


# ##### Callback functions ###


def convert_entries(entries, modifier):
    entries = (e.path if isinstance(e, DirEntry) else e for e in entries)
    return (modifier(entry) for entry in entries)


def as_Path_str(item):
    return str(Path(item))


cast_to_str      = partial(convert_entries, modifier=str)
cast_to_Path     = partial(convert_entries, modifier=Path)
cast_to_Path_str = partial(convert_entries, modifier=as_Path_str)
