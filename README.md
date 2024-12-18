[![image](https://img.shields.io/pypi/v/the-link-reaper.svg)](https://pypi.python.org/pypi/the-link-reaper)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) 
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# link-reaper

Verifies AND automatically reaps links to keep your lists updated and clean of "zombies".

Unlike other link verifiers, this one will make direct changes to your markdown files instead of just preventing push/pull requests (but it can do that too).

# Installation

## For personal usage

Here are a couple options for those who simply want to use the project.

### As an installed Package:

TBD - for directly downloading the package folder

### Using Pip Install:

0. Have Python installed and the latest version of Pip
1. Use `pip install the-link-reaper`
2. See [here](#Terminal) for what you can do with this package.

### Docker

The project includes a Dockerfile you can edit and build for your images. See [here](##Examples) for an example. A downloadable premade image TBD.

### Github Workflow

You can install link-reaper as a python package to use in workflows. See [here](##Examples)  for an example.

## For Developers

### Instructions
0. Have [Python](https://www.python.org/downloads/) installed.
1. Fork this repo (if you want to contribute. If not, skip this step)
2. Find/create your directory of choice
3. Open a terminal in that directory and use `git clone https://github.com/<your name>/<your fork name here>.git` but if you are not using a fork, just use `https://github.com/sharktrexer/link-reaper.git`
4. Create a virtual environment `python3 -m venv venv` 
5. Install requried dependencies `pip install -r requirements.txt` or if you intend to contribute, `pip install -r requirements_dev.txt`
6. Use `python -m link_reaper.reaper reap yourfile.md` utilizing the many options [here](#Terminal) to test or play around with the project.
7. If your contributing, follow the steps below

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
Package Usage: python -m link_reaper.reaper reap [OPTIONS] [FILES]...
Regular Usage: link-reaper reap [OPTIONS] [FILES]...

  Command that reaps links from markdown files based on your options

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
  -iu, --ignore_urls TEXT      Ignores specific links you want to whitelist.
                               Enter each url comma separated.
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

TODO - show using it from github clone, python and pip install in terminal, github workflow, and docker

## In Progress Features

If you would like to see what is currently in production/what features are planned, visit [my trello page here!](https://trello.com/invite/b/6751e6dee83464d169568c4f/ATTI8034309813ff46026b4d29289c87a874D3DDC4E9/link-reaper)
