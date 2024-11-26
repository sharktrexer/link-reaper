# link-reaper

Verifies AND automatically reaps links to keep your lists updated and clean of "zombies".

Unlike other link verifiers, this one will make direct changes to your markdown files instead of just preventing push/pull requests.

# Installation

## Temporary instructions:

0. Have Python installed
1. Download the link_reaper folder
2. Open a terminal and change directory to inside that folder, where the .py files reside
3. Install requried dependencies (requests & Click)
4. In terminal, call reaper.py reap [OPTIONS] [FILES], with the different options shown below.
5. Enjoy your markdown file free of dead links!

## Future
Planning on packaging this project with SetupTools to be used without needing a venv or python installed.

# Usage

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
  -it, --ignore_timeouts       Ignore links that time out.
  -iu, --ignore_urls TEXT      Ignores specific links you want to whitelist.
                               Use this option for each url.
  -rs, --reap_status INTEGER   Status codes you want to be reaped (404 and
                               300s are default). Use this option per each
                               code.
  -p, --patience INTEGER       Max # of seconds to wait for url to to send
                               data.
  --help                       Show this message and exit.
```

## Examples

TODO

## GitHub Actions

GitHub Action functionality currently in production.