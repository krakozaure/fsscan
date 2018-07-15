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


def test_run_without_parameters(temp_dir):
    results = fsscan.run(temp_dir)
    expected = [
        temp_dir + "/dir1",
        temp_dir + "/dir2",
        temp_dir + "/file1.py",
    ]

    results = sorted(results)
    expected = sorted(results)

    assert results == expected


def test_run_with_parameters(temp_dir):
    parameters = {
        "patterns": "*LOG*",
        "ignore_case": True,
        "wanted_type": fsscan.DIR_TYPE,
        "recursive": True,
    }

    results = fsscan.run(temp_dir, **parameters)
    expected = [
        temp_dir + "/dir1/logs",
        temp_dir + "/dir2/logs",
    ]

    results = sorted(results)
    expected = sorted(results)

    assert results == expected
