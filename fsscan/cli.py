import argparse
import sys

from .core import run as run_scan
from .__version__ import __version__


def run():

    parser = argparse.ArgumentParser(
        description="Quickly scan a directory and yield matching entries,"
                    " based on patterns and/or entry type.",
        prog="fsscan",
    )

    pyversion = ".".join(str(v) for v in sys.version_info[:3])
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {} (python {})".format(__version__, pyversion),
    )

    parser.add_argument(
        "-d",
        help="Directory to scan",
        default=".",
        metavar="directory",
    )
    parser.add_argument(
        "-i",
        help="Ignore case",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-r",
        help="Recursive scan",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-t",
        help="Type of entry to return",
        default="BOTH",
        choices=["f", "d", "b", "FILE", "DIR", "BOTH"],
    )
    parser.add_argument(
        "-f",
        help="Follow symlinks of directories",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "p",
        help="Patterns to look for in entries names",
        default=None,
        metavar="patterns",
        nargs="*",
    )

    args = parser.parse_args()

    entries = run_scan(
        directory=args.d,
        patterns=args.p,
        ignore_case=args.i,
        wanted_type=args.t,
        recursive=args.r,
        on_error=None,
        follow_links=args.f,
        callback=None,
    )

    fse = sys.getfilesystemencoding()
    for entry in entries:
        try:
            print(entry)
        except UnicodeEncodeError:
            entry = entry.encode(fse, errors="replace").decode(fse)
            print(entry)
