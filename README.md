# link-reaper

Verifies AND automatically reaps links to keep your lists updated and clean of "zombies".

# Installation

TBD

# Usage

## Terminal
```
Usage: reaper.py reap [OPTIONS] [FILES]...

Options:
  -s, --show_afterlife         Create an afterlife-filename.md for each
                               checked file that only contains the reaped
                               links.
  -m, --merciful               Instead of overwriting files, create a reaped-
                               filename.md for each checked file that contains
                               applied changes.
  -ig, --ignore_ghosts         Ignore redirect links.
  -id, --ignore_doppelgangers  Ignore duplicate links.
  -rt, --reap_timeouts         Reap links that time out.
  -iu, --ignore_urls TEXT      Ignores specific links you want to whitelist.
                               Use this option for each url.
  -rs, --reap_status INTEGER   Status codes you want to be reaped (404 and
                               300s are default). Use this option per each
                               code.
  -p, --patience INTEGER       Max # of seconds to wait for url to to send
                               data.
  -g, --guides PATH
  --help                       Show this message and exit.
```

## Examples


## GitHub Actions
