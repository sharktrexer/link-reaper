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
5. Install requried dependencies `pip install -r requirements.txt` or if you intend to contribute, also do `pip install -r requirements_dev.txt`
6. Use `python -m link_reaper.reaper reap yourfile.md -is -m` utilizing the many options [here](#Terminal) to test or play around with the project. The provided example will NOT overwrite your file data.
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
Clone/Fork Usage: python -m link_reaper.reaper [OPTIONS] COMMAND [ARGS]...
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
  -c, --chances INTEGER        Max # of connection retries before labeling a
                               link as timed out.
  -dl, --disable_logging       Prevents creation of any log type files (does
                               not overwrite -show-afterlife)
  -v, --verbose                Provide more information on the reaping
                               process.
  --help                       Show the details of each option like above.
```

## Examples

Utilizing pip, you can install this package to use not only on your direct computer for any project, but also gives the flexibility of use in containers or workflows.

### General Use

In your Python project, you can use `pip install the-link-reaper` for access to CLI commands. For example, if you want to automatically clean a markdown list in your project, 
like a README.md, while understanding what exactly was changed without overwriting data, try:

```
link-reaper reap example.md -is -m -s
```

This will keep the integrity of your document and create new files like 

1. reaped-example.md | Showcases the changes the program would make to the inputted file if overwritten
2. log-example.md | Lists any links that the program couldn't determine were reapable or not
3. afterlife-example.md | Lists all the reaped links by themselves

If you like the changes Link Reaper made, rename reaped-example.md to example.md to overwrite the original document with a cleaner link list. Feel free to delete the afterlife & log files.

#### Whitelisting URLs

If there are certain urls or web domains you'd rather this program ignore, utilize the `--ignore_urls` option. For example, if you want to ignore a specific url, do:

`link-reaper reap example.md -iu https://github.com/sharktrexer/link-reaper`

But, lets say you want to ignore ALL github urls, then simply do:

`-iu github.com`

Or, if you wanted to ignore all of a certain path from github, you could do:

`-iu github.com/sharktrexer`

And finally, you can mix and match:

`-iu https://github.com/sharktrexer/link-reaper,google.com`

#### Blacklisting Status Codes

There may be some status codes some of your urls return that you would like reaped. In that case, use the `--reap-status` option. Similarly to above, to ignore one or multiple specific codes, you can do:

`link-reaper reap example.md -rs 401,402`

However, you may want to reap a similar group of status codes. In that case, Link Reaper provides an easy shorthand way to do so, using "\*". So if you want all 400 codes to be reaped, then inputting 4* or 4** would do such, as so:

`-rs 4*`

This also works with only specifying a range of 10, where if you input 30*, all codes from 300-309 would be caught and reaped, like such:

`-rs 30*`

Mixing and matching is totally fine as well:

`-rs 403,30*`

And don't worry about erroneous inputs, they'll be ignored.

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
# Dockerfil for link-reaper
FROM python:3.13.1

# Where the markdown file is located. Default is current location of this file
WORKDIR ./

RUN pip install the-link-reaper

# Command to run link-reaper on your file without overwriting or file creation
# Customize as you desire
RUN link-reaper reap yourfile.md -is -m -dl
```

Now you can use the following commands in your terminal to run:

`docker build -t link-reaper .`

`docker run link-reaper`

## In Progress Features

If you would like to see what is currently in production/what features are planned, visit [my trello page here!](https://trello.com/invite/b/6751e6dee83464d169568c4f/ATTI8034309813ff46026b4d29289c87a874D3DDC4E9/link-reaper)
