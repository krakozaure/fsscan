import os
import pathlib

import pytest

import fsscan


@pytest.fixture
def temp_dir(tmpdir):
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
    temp_dir_ = str(tmpdir.mkdtemp())
    for file_path in files_list:
        p = pathlib.Path(temp_dir_) / file_path
        if not p.parent.exists():
            os.makedirs(str(p.parent), exist_ok=True)
        p.touch()
    return temp_dir_


def test_callback_cast_to_Path_to_str(temp_dir):
    parameters = {
        "patterns": "*.py",
        "recursive": True,
    }

    results = fsscan.run(temp_dir, **parameters)
    expected = [
        temp_dir + "/dir1/file11.py",
        temp_dir + "/dir2/file21.py",
        temp_dir + "/dir2/file22.py",
        temp_dir + "/file1.py",
    ]

    results = sorted(fsscan.cast_to_Path_str(results))
    expected = sorted(fsscan.cast_to_Path_str(expected))

    assert results == expected
