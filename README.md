[![image](https://img.shields.io/pypi/v/the-link-reaper.svg)](https://pypi.python.org/pypi/the-link-reaper)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) 
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# link-reaper

Verifies AND automatically reaps links to keep your lists updated and clean of "zombies".

Unlike other link verifiers, this one will make direct changes to your markdown files instead of just preventing push/pull requests (but it can do that too).

# Installation

This project is utilized as a Python package, and requires [Python](https://www.python.org/downloads/) to be installed if utlized directly on your computer.

## For personal usage

Here are a couple options for those who want to use the project.

### Using Pip Install:

0. Have Python installed and the latest version of Pip
1. Use `pip install the-link-reaper`
2. See [Usage](#Terminal) for what you can do with this package.

### Docker

The project includes a Dockerfile you can edit and build for your images. See [here](##Examples) for an example. A downloadable premade image TBD.

### Github Workflow

You can install link-reaper as a python package to use in workflows. See [here](##Examples) for an example.

## For Developers

### Instructions
1. Fork this repo (if you want to contribute. If not, skip this step)
2. Find/create your directory of choice
3. Open a terminal in that directory and use `git clone https://github.com/<your name>/<your fork name here>.git` but if you are not using a fork, just use `https://github.com/sharktrexer/link-reaper.git`
4. Create a virtual environment `python -m venv .venv` 
5. Install requried dependencies `pip install -r requirements.txt` or if you intend to contribute, `pip install -r requirements_dev.txt`
6. Use `python link-reaper reap yourfile.md -m` utilizing the many options [here](#Terminal) to test or play around with the project. The provided example will NOT overwrite your file data.
7. If you're contributing, follow the steps below

### Contributing

Feel free to create Issues or Pull Requests at your leisure. If you are unsure if the PR is a good idea, create an Issue first and I will respond as best as I can.

Before creating a pull request, be sure to use the following commands after implementing your changes (and make sure you installed dependencies from dev_requirements.txt):
```
# Lint code
ruff check link-reaper

# Apply lint fixes (you may have to do some manually)
ruff check --fix

# Format changes
ruff format link-reaper

# Optional for bonus points
pylint link-reaper
```
If you don't use the ruff commands, the workflow of this project will fail and it will take longer to merge your potentially beautiful changes!

# Usage

Here are the many ways you can utilize this python package.

## Terminal
```
Package Usage: python -m link_reaper.reaper [OPTIONS] COMMAND [ARGS]...
Usage: link-reaper [OPTIONS] COMMAND [ARGS]...

  Groups CLI commands under 'link reaper' and prints optional flavor ascii art

Options:
  -na, --no_art  Disable printed ascii art.
  --help         Show this message and exit.

Commands:
  reap  Command that reaps links from markdown files based on your options

Options:
  -s, --show_afterlife         Create an afterlife-filename.md for each
                               checked file that only contains the reaped
                               links.
  -m, --merciful               Instead of overwriting files, create a reaped-
                               filename.md for each checked file that contains
                               applied changes.
  -ig, --ignore_ghosts         Prevents updating redirecting links.
  -id, --ignore_doppelgangers  Ignore duplicate links.
  -is, --ignore_ssl            Disable SSL errors. Not very secure so use with
                               caution.
  -it, --ignore_timeouts       Ignore links that time out.
  -iu, --ignore_urls TEXT      Ignores specific links or general domains you 
                               want to whitelist. Comma separate each entry.
  -rs, --reap_status TEXT      Status codes you want to be reaped (By default
                               404, 500, 521 are reaped and 300s are updated).
                               Enter each code comma separated.
  -p, --patience INTEGER       Max # of seconds to wait for url to send data
                               until it times out.
  -dl, --disable_logging       Prevents creation of any log type files (does
                               not overwrite -show-afterlife)
  -v, --verbose                Provide more information on the reaping
                               process.
  --help                       Show this message and exit.
```

## Examples

Utilizing pip, you can install this package to use not only on your direct computer for any project, but also gives the flexibility of use in containers or workflows.

### General Use

In your Python project, you can use `pip install the-link-reaper` for access to CLI commands. For example, if you want to automatically clean a markdown list in your project, 
like a README.md, while understanding what exactly was changed without overwriting data, try:

```
python link-reaper reap example.md -is -m -s
```

This will keep the integrity of your document and create new files like 

1. reaped-example.md | Showcases the changes the program would make to the inputted file if overwritten
2. log-example.md | Lists any links that the program couldn't determine were reapable or not
3. afterlife-example.md | Lists all the reaped links by themselves

If you like the changes Link Reaper made, rename reaped-example.md to example.md to overwrite the original document with a cleaner link list. Feel free to delete the afterlife & log files.

### GitHub Workflow

Link Reaper can be used to verify pushes and pull requests using workflows, without changing any aspect of a document. See below for an example that verifies links without any extra fluff or potential to overwrite changes.

```
name: Link-Reaper

on:
  push:
    branches: [ '*' ]
  pull_request:
    branches: [ '*' ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.13.1' 
    - name: Install & run link-reaper
      run: |
        pip install the-link-reaper
        link-reaper -na reap README.md -is -m -dl
```

### Dockerfile

Provided in this project is an example Dockerfile that you can use to create a container that verifies a markdown list. For easy copy/paste:

```
# Dockerfile for link-reaper
FROM python:3.13.1

RUN pip install the-link-reaper

# Command to run link-reaper on your file without overwriting
# Customize as you desire
CMD ["link-reaper", "reap", "yourfile.md", "-is", -m"]

# Now you can use the following commands in your terminal to run:
# docker build -t link-reaper .
# docker run link-reaper
```

## In Progress Features

If you would like to see what is currently in production/what features are planned, visit [my trello page here!](https://trello.com/invite/b/6751e6dee83464d169568c4f/ATTI8034309813ff46026b4d29289c87a874D3DDC4E9/link-reaper)
