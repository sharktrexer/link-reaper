# link-reaper

Verifies AND automatically reaps links to keep your lists updated and clean of "zombies".

Unlike other link verifiers, this one will make direct changes to your markdown files instead of just preventing push/pull requests.

# Installation

## For personal usage

Here are a couple options for those who simply want to use the project.

### As an installed Package:

TBD

### Clone Repo:

0. Have Python installed.
1. Find/create your directory of choice
2. Open a terminal in that directory and use `git clone https://github.com/sharktrexer/link-reaper.git`
3. Install requried dependencies (pip install requests & Click)
4. Use `python -m link_reaper.reaper reap yourfile.md` utilizing the many options [here](#Terminal)
5. Enjoy your markdown file free of dead links!

### Using Pip Install:

TBD

## For Developers

These options allow for those who want to contribute or mess around with the code.

TBD

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
