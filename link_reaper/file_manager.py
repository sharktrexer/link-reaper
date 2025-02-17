"""Contains functions relating to file manipulation."""

import os

get_directory = lambda: os.getcwd() + "\\"

get_filename = lambda file: os.path.splitext(file)[0]

overwrite_file = lambda src, dst: os.replace(src, dst)