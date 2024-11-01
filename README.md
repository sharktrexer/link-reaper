# link-reaper

Verifies AND automatically reaps links to keep your lists updated and clean of zombies.

# Installation

TBD

# Usage

## Terminal
```
/* Checks all markdown links in files and deletes zombies, replaces ghosts, 
   and applies those changes to the files. */
link-reaper [file(s)] [options]
  -f, -files                       Name of files to check, separated by commas

  -i, -ignore [codes]              Status codes to ignore, separated by commas
      -ignore-copy                 Ignore duplicate links, otherwise subsequent dupes are removed
      -ignore-ghosts               Ignore redirect links, otherwise are replaced by the appropriate
                                   new url
      -ignore-specific [urls]      Ignore links that match inputted link, separated by commas

  -s, -show-afterlife              Creates an afterlife-filename.md for each checked file that only  
                                   contains the reaped links

  -p, patience [seconds]           Max # of seconds reaper waits for url to respond before reaping
  
  -m, -merciful                    Creates a reaped-filename.md for each checked file that contains
                                   applied changes, if you want to manually compare to the original
                                   file(s). Otherwise, changes are applied directly to the files.

  -g, -guide [list_file]           Instead of checking every link in the provided file, only the  
                                   markdown links provided in the list_file are reviewed for reaping.
                                   Above options will still apply. The purgatory-filename from
                                   'merciful' could be used as a guide for example. If multiple guides
                                   are provided, they must be comma separated, and will correspond to
                                   only one of the inputted -f files.

 -h, -help                         This info.
```

## Examples


## GitHub Actions
