
# fsscan

Quickly scan a directory and yield matching entries, based on patterns and/or entry type.

### Status

This project is not maintained anymore !

### Requirements

* Python 3.4+ (Python 3.6+ is preferred)
* scandir (for Python 3.4)

The module is tested on Python 3.4 to 3.7 (included).

### Installation

From [PyPI](https://pypi.org/)

* Open a terminal
* Type `pip3 install fsscan` 
  <br>or `pip3 install --user fsscan` on Linux

From [GitHub](https://github.com)

* Download the archive from [GitHub](https://github.com/krakozaure/fsscan)
* Unzip the archive
* Open a terminal
* Move to the directory containing `setup.py`
* Type `pip3 install .`
  <br>or `pip3 install --user .` on Linux

### Usage

#### From command line

```sh
$ python3 -m fsscan
```

or

```sh
$ fsscan
```

```sh
usage: fsscan [-h] [-d directory] [-i] [-r] [-t {f,d,b,FILE,DIR,BOTH}] [-f]
              [patterns [patterns ...]]

Quickly scan a directory and yield matching entries.

positional arguments:
  patterns              Patterns to look for in entries names

optional arguments:
  -h, --help            show this help message and exit
  -d directory          Directory to scan
  -i                    Ignore case
  -r                    Recursive scan
  -t {f,d,b,FILE,DIR,BOTH}
                        Type of entry to return
  -f                    Follow symlinks of directories
```

#### From script

Using this directory tree sample
```
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
```

**Example 1 - without parameters**
```Python
for entry in fsscan.run(temp_dir):
    print(entry)
```
Output<exp>*</exp>:
```
<temp_dir>/dir1
<temp_dir>/dir2
<temp_dir>/file1.py
```

**Example 2 - with parameters**
```Python
parameters = {
    "patterns": "*LOG*",
    "ignore_case": True,
    "wanted_type": fsscan.DIR_TYPE,
    "recursive": True,
}
for entry in fsscan.run(<temp_dir>, **parameters):
    print(entry)
```
Output<exp>*</exp>:
```
<temp_dir>/dir1/logs
<temp_dir>/dir2/logs
```

<exp>*</exp> : The outputs may differ for you OS


### Documentation

```
run(directory='.',
    patterns=None, ignore_case=True, wanted_type=BOTH_TYPES,
    recursive=False, on_error=None, follow_links=False, callback=None):

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
```

For callbacks, see `fsscan/callbacks.py`.

### Thanks

I would say a big thank you to the people listed below :
* [Guido van Rossum (@gvanrossum)](https://github.com/gvanrossum) and other Python contributors for their great work on [Python](https://github.com/Python/Python).
* [Ben Hoyt (@benhoyt)](https://github.com/benhoyt) and other contributors for their great work on [scandir](https://github.com/benhoyt/scandir)
* People from the #python-fr channel on IRC for their advices and feedbacks
* My friends (ABR & AM) for their advices and feedbacks
