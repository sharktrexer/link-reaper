# link-reaper

Verifies AND automatically reaps links to keep your lists updated and clean of "zombies".

Unlike other link verifiers, this one will make direct changes to your markdown files instead of just preventing push/pull requests.

# Installation

## For personal usage

Here are a couple options for those who simply want to use the project.

### As an installed Package:

TBD - for downloaded the package folder

### Using Pip Install:

TBD - for downlaoding from PyPI

## For Developers

### Instructions
0. Have [Python](https://www.python.org/downloads/) installed.
1. Fork this repo (if you want to contribute. If not, skip this step)
2. Find/create your directory of choice
3. Open a terminal in that directory and use `git clone https://github.com/sharktrexer/<your fork name here>.git` but if you are not using a fork, just use `https://github.com/sharktrexer/link-reaper.git`
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

#Optional for bonus points
pylint link-reaper
```
If you don't use the ruff commands, the workflow of this project will fail and it will take longer to merge your potentially beautiful changes!

# Usage

Here are the many ways you can utilize this python package.

## Terminal
```
Usage: python -m link_reaper.reaper reap [OPTIONS] [FILES]...

  Command that reaps links from markdown files based on your options

Options:
  -s, --show_afterlife         Create an afterlife-filename.md for each
                               checked file that only contains the reaped
                               links.
  -m, --merciful               Instead of overwriting files, create a reaped-
                               filename.md for each checked file that contains
                               applied changes.
  -ig, --ignore_ghosts         Ignore redirect links.
  -id, --ignore_doppelgangers  Ignore duplicate links.
  -is, --ignore_ssl            Ignore links that result in SSL errors. Not
                               very secure so use with caution.
  -iu, --ignore_urls TEXT      Ignores specific links you want to whitelist.
                               Enter each url comma separated.
  -rs, --reap_status TEXT      Status codes you want to be reaped (404, 500,
                               521 and 300s are default).Enter each code comma
                               separated.
  -p, --patience INTEGER       Max # of seconds to wait for url to to send
                               data.
  --help                       Show this message and exit.
```

## Examples

TODO 

## GitHub Actions

GitHub Action functionality currently in production.

## Docker

Docker functionality in progress.
