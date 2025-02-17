"""Contains functions relating to file manipulation."""

import os


def get_directory():
    return os.getcwd() + "\\"


def get_filename(file):
    return os.path.splitext(file)[0]


def overwrite_file(src, dst):
    os.replace(src, dst)
