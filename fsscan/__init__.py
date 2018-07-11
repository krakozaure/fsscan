from collections import Sequence
from enum import IntEnum
from fnmatch import fnmatchcase
from functools import partial
from os.path import sep
from pathlib import Path

try:
    from os import scandir, DirEntry  # PY>=3.5  noqa
except ImportError as exc:
    from scandir import scandir, DirEntry  # PY<3.5  noqa


class EntryType(IntEnum):
    FILE = 1
    DIR = 2
    BOTH = 3


# ##### Core functions ###


def run(directory='.',
        patterns=None, case_sensitive=False, wanted_type=EntryType.BOTH,
        recursive=False, on_error=None, follow_links=False, callback=None):
    """Scan a directory and return the matching entries

    Parameters
    ----------
    directory : (str or Path)
        Directory to scan
    patterns : (str or sequence of str)
        Patterns to look for in the entry name
    case_sensitive : bool
        Use case-sensitivity on patterns testing
    wanted_type : (EntryType or int)
        Type of entry to return (file, dir or both)
    recursive : bool
        Scan directory recursively
    on_error : (None or callable)
        Callable to use when an error occured in scandir
    follow_links : bool
        Follow symlinks of directories
    callback : (None or callable)
        Callable to use after the scan (e.g. entries cast)

    Returns
    -------
    Generator
        Entries returned by the scandir function
    """

    directory = _prepare_directory(directory)
    patterns = _prepare_patterns(patterns, case_sensitive)

    entries = _scan(
        directory, patterns, case_sensitive, wanted_type,
        recursive, on_error, follow_links
    )

    return callback(entries) if callable(callback) else entries


def _prepare_directory(directory):
    # Normalize directory path to be compatible with PY<3.6 (PEP 519)
    # and ensure consistancy with OS handling of directories separator
    return str(directory).replace("\\", sep).replace("/", sep)


def _prepare_patterns(patterns, case_sensitive):
    # Ensure that 'patterns' is a sequence of one or more items
    if isinstance(patterns, str) or not isinstance(patterns, Sequence):
        patterns = (patterns,)

    # Remove duplicates and only keep non-empty strings
    patterns = (p for p in set(patterns) if p and isinstance(p, str))

    # If needed, disable the case-sensitivity at patterns level
    if not case_sensitive:
        patterns = (pattern.lower() for pattern in patterns)

    return tuple(patterns)


def _scan(directory,
          patterns, case_sensitive, wanted_type,
          recursive, on_error, follow_links):

    # Let user choose if the scan should continue after an error occured
    try:
        entries = scandir(directory)
    except (FileNotFoundError, PermissionError) as error:
        if callable(on_error):
            on_error(error)
        return

    for entry in entries:

        # is_dir will be used many times later, so better avoid costly calls
        entry_is_dir = entry.is_dir(follow_symlinks=follow_links)

        # Entry type is checked first because it is faster to apply
        # and can avoid unecessary patterns testing
        if _match_type(wanted_type, entry_is_dir):

            # If needed, disable the case-sensitivity at entry level
            entry_name = entry.name if case_sensitive else entry.name.lower()

            # Return the entry or apply a filter from patterns
            if not patterns or _match_pattern(entry_name, patterns):
                yield entry

        # Apply the previous lines to sub directories if needed
        if recursive and entry_is_dir:
            yield from _scan(
                entry.path, patterns, case_sensitive, wanted_type,
                recursive, on_error, follow_links
            )


def _match_type(wanted_type, entry_is_dir):
    # Conditions are ordered by easiness of check
    # Integer values are used to avoid getattr calls on EntryType
    return (
        (wanted_type == 3)
        or (wanted_type == 2 and entry_is_dir)
        or (wanted_type == 1 and not entry_is_dir)
    )


def _match_pattern(entry_name, patterns):
    # Check if at least one pattern matches the entry name
    return any(fnmatchcase(entry_name, pattern) for pattern in patterns)


# ##### Callback functions ###


def convert_entries(entries, modifier):
    # Extract path (str) before applying modifications
    # to avoid cast error with PY<3.6 (PEP 519)
    entries = (e.path if isinstance(e, DirEntry) else e for e in entries)
    return (modifier(entry) for entry in entries)


def as_Path_str(item):
    return str(Path(item))


# Predefined callbacks
cast_to_str = partial(convert_entries, modifier=str)
cast_to_Path = partial(convert_entries, modifier=Path)
cast_to_Path_str = partial(convert_entries, modifier=as_Path_str)
