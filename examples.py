import os
import pathlib

import tempfile

import fsscan


def make_temp_dir():
    """Create directory tree structure used for the tests

    <temp_dir>
    |-- dir1/
    |   |-- logs/
    |   |   |-- file11.log
    |   |-- file11.py
    |-- dir2/
    |   |-- logs/
    |   |   |-- file21.log
    |   |   |-- file22.log
    |   |-- file21.py
    |   |-- file22.py
    |-- file1.py
    """

    files_list = [
        "dir1/logs/file11.log",
        "dir1/file11.py",
        "dir2/logs/file21.log",
        "dir2/logs/file22.log",
        "dir2/file21.py",
        "dir2/file22.py",
        "file1.py",
    ]
    temp_dir_ = str(tempfile.mkdtemp())
    for file_path in files_list:
        p = pathlib.Path(temp_dir_) / file_path
        if not p.parent.exists():
            os.makedirs(str(p.parent), exist_ok=True)
        p.touch()
    return temp_dir_


def run_without_parameters(temp_dir):
    print("# ===== fsscan.run without parameters =====")
    for entry in fsscan.run(temp_dir):
        print(entry)


def run_with_parameters(temp_dir):
    print("# ===== fsscan.run with parameters =====")
    parameters = {
        "patterns": "*LOG*",
        "ignore_case": True,
        "wanted_type": fsscan.DIR_TYPE,
        "recursive": True,
    }
    for entry in fsscan.run(temp_dir, **parameters):
        print(entry)


def main():
    temp_dir = make_temp_dir()
    run_without_parameters(temp_dir)
    run_with_parameters(temp_dir)


if __name__ == '__main__':
    main()
