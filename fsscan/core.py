from collections import Sequence
from fnmatch import fnmatchcase
from os.path import sep

try:
    from os import scandir  # PY>=3.5, noqa
except ImportError as exc:
    from scandir import scandir  # PY<3.5, noqa


__all__ = [
    "BOTH_TYPES",
    "DIR_TYPE",
    "FILE_TYPE",
    "run",
]


FILE_TYPE = 1
DIR_TYPE = 2
BOTH_TYPES = 3


def run(directory='.',
        patterns=None, ignore_case=True, wanted_type=BOTH_TYPES,
        recursive=False, on_error=None, follow_links=False, callback=None):
    """Directory scanner

    Quickly scan a directory and yield matching entries,
    based on patterns and/or entry type.

    Parameters
    ----------
    directory : (str or Path)
        Directory to scan
    patterns : (str or sequence of str)
        Patterns to look for in entries names
    ignore_case : bool
        Ignore case
    wanted_type : int
        Type of entry to return (file, directory or both)
    recursive : bool
        Recursive scan
    on_error : (None or callable)
        Callable to use when an error occured in scandir
    follow_links : bool
        Follow symlinks of directories
    callback : (None or callable)
        Callable to use after the scan (e.g. entries cast)

    Returns
    -------
    Generator
        Entries paths as string or callback result
    """

    directory = _prepare_directory(directory)
    patterns = _prepare_patterns(patterns, ignore_case)
    wanted_type = _prepare_wanted_type(wanted_type)

    entries = _scan(
        directory, patterns, ignore_case, wanted_type,
        recursive, on_error, follow_links
    )

    return callback(entries) if callable(callback) else entries


def _scan(directory,
          patterns, ignore_case, wanted_type,
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
            entry_name = entry.name.lower() if ignore_case else entry.name

            # Return the entry or apply a filter from patterns
            if not patterns or _match_pattern(entry_name, patterns):
                yield entry.path

        # Apply the previous lines to sub directories if needed
        if recursive and entry_is_dir:
            yield from _scan(
                entry.path, patterns, ignore_case, wanted_type,
                recursive, on_error, follow_links
            )


def _prepare_directory(directory):
    # Normalize directory path to be compatible with PY<3.6 (PEP 519)
    # and ensure consistancy with OS handling of directories separator
    return str(directory).replace("\\", sep).replace("/", sep)


def _prepare_patterns(patterns, ignore_case):
    # Ensure that 'patterns' is a sequence of one or more items
    if isinstance(patterns, str) or not isinstance(patterns, Sequence):
        patterns = (patterns,)

    # Remove duplicates and only keep non-empty strings
    patterns = (p for p in set(patterns) if p and isinstance(p, str))

    # If needed, disable the case-sensitivity at patterns level
    if ignore_case:
        patterns = (pattern.lower() for pattern in patterns)

    return tuple(patterns)


def _prepare_wanted_type(wanted_type):
    return {
        1: FILE_TYPE,
        "f": FILE_TYPE,
        "FILE": FILE_TYPE,

        2: DIR_TYPE,
        "d": DIR_TYPE,
        "DIR": DIR_TYPE,

        3: BOTH_TYPES,
        "b": BOTH_TYPES,
        "BOTH": BOTH_TYPES,
    }.get(wanted_type, BOTH_TYPES)


def _match_type(wanted_type, entry_is_dir):
    # Conditions are ordered by easiness of check
    return (
        (wanted_type == BOTH_TYPES)
        or (wanted_type == DIR_TYPE and entry_is_dir)
        or (wanted_type == FILE_TYPE and not entry_is_dir)
    )


def _match_pattern(entry_name, patterns):
    # Check if at least one pattern matches the entry name
    return any(fnmatchcase(entry_name, pattern) for pattern in patterns)
