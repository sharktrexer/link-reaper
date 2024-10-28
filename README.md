# link-reaper

Verifies AND automatically reaps links to keep your lists updated and clean of zombies.

# Installation

TBD

# Usage

## Terminal
```
// Checks all links and tracks what links should be modified/deleted
link-reaper collect [file(s)] [options]
  -f, -files                       Name of files to check, separated by commas
  -i, -ignore [codes]              Status codes to ignore, separated by commas
      -ignore-copy                 Ignore duplicate links
      -ignore-messenger            Ignore redirect links
      -ignore-specific [urls]      Ignore links that match inputted link, separated by commas
           
// Applies all changes from the 'collect' command
link-reaper reap [options]
  default:                         Applies all changes from 'collect' command to the checked file(s) 
                                   by overwriting them
  -show-afterlife                  Creates an afterlife-filename.md for each checked file that only contains 
                                   the zombie links
  override default:
  -merciful                        Creates a purgatory-filename.md for each checked file that contains 
                                   applied changes, if you want to manually compare to the original file(s)
```

## Examples


## GitHub Actions
