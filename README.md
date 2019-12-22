Union copier:
=============

[![PyPI version fury.io](https://badge.fury.io/py/ucopy.svg)](https://pypi.python.org/pypi/ucopy/)

Default copy behavior offer to skip or replace files which names already existed in the target directory
This script allowed to copy files from one or more directories at once to target directory with union mode;
if a file with same name present in the destination directory, then the file will be renamed with a unique suffix

Note:
   - symlinks are ignored

Installation
------------

`python3 -m pip install --user ucopy`

Usage
-----

Definition: ucopy sourcepath  destpath  [-e allowed_extensions] or [-x excluded_extensions] [-v|--verbose]

Example 1: copy only png files, show progress log

   `ucopy /src/path/ /dest/path/ -e png --verbose`

Example 2: copy files with extensions .png .jpg .txt

   `ucopy /src/path/ /dest/path/ -e .png,.jpg,.txt`

Example 3: copy all files, but exclude ones with .zip and .gz extensions

   `ucopy /src/path/ /dest/path/ -x zip,tar.gz`

Example 4: copy all files without restriction

   `ucopy /src/path/ /dest/path/ -e *`

Example 5: copy from multiple source directories matched by glob pattern

   `ucopy /src/path/*/some/*/ /dest/path/`

*Note: You can specify file extensions with or without dots*

