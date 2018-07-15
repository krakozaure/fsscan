import argparse

from .core import run as run_scan


def run():

    parser = argparse.ArgumentParser(
        description="Quickly scan a directory and yield matching entries.",
        prog="fsscan",
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
       patterns=args.p, ignore_case=args.i, wanted_type=args.t,
       recursive=args.r, on_error=None, follow_links=args.f, callback=None
    )
    for entry in entries:
        print(entry)
