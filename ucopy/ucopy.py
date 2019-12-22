#! /usr/bin/env python3

"""
 Union copier:
    copy files from src_dir directory to dest_dir directory with union mode;
    if file with same name present in dest_dir directory than file will be renamed with unique suffix
    Note:
       - recursive mode not supported
       - symlinks are ignored
"""

import os
import glob
from random import choice
from string import ascii_lowercase
from shutil import copyfileobj
from sys import stdout, stderr


def _split_ext(filename: str) -> tuple:
    if '.' not in filename:
        return filename, ''
    if filename.startswith('.'):
        return '', filename
    parts = filename.split('.')
    return parts[0], '.' + '.'.join(parts[1:])


def _rand_suffix(size: int = 5) -> str:
    return ''.join(choice(ascii_lowercase) for i in range(size))


def _ensure_unique_filename(filename: str, fileext: str, path: str) -> str:
    if os.path.exists(os.path.join(path, filename + fileext)):
        filename = "%s_[%s]" % (filename, _rand_suffix())
        return _ensure_unique_filename(filename, fileext, path)
    return filename


def _progress(count: int, total: int, status: str = '') -> None:
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    stdout.flush()


def _copy(src_path: str, dest_path: str) -> None:
    with open(src_path, 'rb') as fsrc:
        with open(dest_path, 'wb') as fdst:
            copyfileobj(fsrc, fdst)


def copier(src_dir: str, dest_dir: str, extensions: list, exclude: list, verbose: bool = False) -> None:
    file_list = os.listdir(src_dir)
    total_files = len(file_list)
    if len(exclude):
        extensions = []
    for i, file in enumerate(file_list):
        name, ext = _split_ext(file)
        src_path = os.path.join(src_dir, file)
        if (len(extensions) and ext not in extensions) or (len(exclude) and ext in exclude):
            continue
        if not os.path.isfile(src_path) or os.path.islink(src_path):
            continue
        name = _ensure_unique_filename(name, ext, dest_dir)
        dest_path = os.path.join(dest_dir, name + ext)
        _copy(src_path, dest_path)
        if verbose:
            _progress(i + 1, total_files, file)


def run(sources: list, dest: str, ext: str = '*', xcl: str = '', verbose: bool = False) -> bool:
    dest = os.path.abspath(str(dest))
    if not os.path.isdir(dest):
        stderr.write("Destination path is not directory\n")
        return False
    exts = ['.' + x.strip() if not x.startswith('.') else x.strip() for x in ([] if ext == '*' else ext.split(','))]
    exclude = ['.' + x.strip() if not x.startswith('.') else x.strip() for x in ([] if not xcl else xcl.split(','))]
    if len(exclude):
        exts = []
    _skipped = True
    for source in sources:
        if '*' in source or '?' in source or '[' in source:
            source_dirs = [os.path.abspath(d) for d in glob.glob(source) if not os.path.islink(d) and os.path.isdir(d)]
            _skipped = not len(source_dirs)
            for source_dir in source_dirs:
                if verbose:
                    stdout.write("Work in %s \n" % source_dir)
                copier(source_dir, dest, exts, exclude, verbose)
        else:
            source_dir = os.path.abspath(source)
            if not os.path.isdir(source_dir) or os.path.islink(source_dir):
                continue
            _skipped = False
            if verbose:
                stdout.write("Work in %s \n" % source_dir)
            copier(source_dir, dest, exts, exclude, verbose)
    return not _skipped
