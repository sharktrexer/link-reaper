"""CLI for link_reaper"""

import sys
import click
from . import link_collector

# pylint: disable=trailing-whitespace, line-too-long, anomalous-backslash-in-string
INTRO = r""" 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢿⣧⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣶⡀⠀⠀⢀⡴⠛⠁⠀⠘⣿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣷⣤⡴⠋⠀⠀⠀⠀⠀⢿⣇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢸⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠈⣿⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢏⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⡇                                      .-') _  .-. .-')          _  .-')      ('-.      ('-.        _ (`-.     ('-.    _  .-')   
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣷⣾⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢿⡇                                    ( OO ) ) \  ( OO )        ( \( OO )   _(  OO)    ( OO ).-.   ( (OO  )  _(  OO)  ( \( -O ) 
⠀⠀⠀⠀⠀⠀⠀⢀⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⢸⡇            ,--.        ,-.-')  ,--./ ,--,'  ,--. ,--.         ,------.  (,------.   / . --. /  _.`     \ (,------.  ,------.  
⠀⠀⠀⠀⠀⠀⢠⡞⠁⢹⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢸⠀            |  |.-')    |  |OO) |   \ |  |\  |  .'   /         |   /`. '  |  .---'   | \-.  \  (__...--''  |  .---'  |   /`. ' 
⠀⠀⠀⠀⠀⣠⠟⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⢸⠀            |  | OO )   |  |  \ |    \|  | ) |      /,         |  /  | |  |  |     .-'-'  |  |  |  /  | |  |  |      |  /  | | 
⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀            |  |`-' |   |  |(_/ |  .     |/  |     ' _)        |  |_.' | (|  '--.   \| |_.'  |  |  |_.' | (|  '--.   |  |_.' | 
⠀⠀⠀⣴⠋⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀           (|  '---.'  ,|  |_.' |  |\    |   |  .   \          |  .  '.'  |  .--'    |  .-.  |  |  .___.'  |  .--'   |  .  '.' 
⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀   ⠀         |      |  (_|  |    |  | \   |   |  |\   \         |  |\  \   |  `---.   |  | |  |  |  |       |  `---.  |  |\  \  
⢀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀  ⠀ ⠀⠀        `------'    `--'    `--'  `--'   `--' '--'         `--' '--'  `------'   `--' `--'  `--'       `------'  `--' '--' 
⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀    
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀ ⠀    
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀   ⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀   
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀   
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠃"""  # noqa: E501
# pylint: enable=trailing-whitespace, line-too-long, anomalous-backslash-in-string


# DISABLE PRINT OF INTRO
@click.option(
    "-na", "--no_art", is_flag=True, help="Disable printed ascii art.", default=False
)
@click.group(name="link_reaper")
def link_reaper(no_art):
    """Groups CLI commands under 'link_reaper' and prints intro text"""
    if not no_art:
        click.echo(INTRO)


@link_reaper.command(context_settings={"ignore_unknown_options": True})
# CREATE AFTERLIFE CONTAINING REAPED LINKS
@click.option(
    "-s",
    "--show_afterlife",
    is_flag=True,
    help="Create an afterlife-filename.md for each checked file that only contains the reaped links.",
)
# DONT OVERWRITE
@click.option(
    "-m",
    "--merciful",
    is_flag=True,
    help=(
        "Instead of overwriting files, create a reaped-filename.md for each checked file "
        "that contains applied changes."
    ),
)
# IGNORE REDIRECTION UPDATES
@click.option(
    "-ig", "--ignore_ghosts", is_flag=True, help="Prevents updating redirecting links."
)
# IGNORE DUPLICATES
@click.option(
    "-id", "--ignore_doppelgangers", is_flag=True, help="Ignore duplicate links."
)
# IGNORE SSL
@click.option(
    "-is",
    "--ignore_ssl",
    is_flag=True,
    help="Disable SSL errors. Not very secure so use with caution.",
)
# IGNORE TIMEOUTS
@click.option(
    "-it", "--ignore_timeouts", is_flag=True, help="Ignore links that time out."
)
# IGNORE LIST OF URLS
@click.option(
    "-iu",
    "--ignore_urls",
    type=str,
    default="",
    help=(
        "Ignores specific links or general domains you want to whitelist."
        " Comma separate each entry."
    ),
)
# REAP LIST OF STATUS CODES
@click.option(
    "-rs",
    "--reap_status",
    type=str,
    default="",
    help=(
        "Status codes you want to be reaped (By default 404, 500, 521 are reaped and 300s are updated)."
        " Enter each code comma separated."
    ),
)
# TIMEOUT
@click.option(
    "-p",
    "--patience",
    default=20,
    help="Max # of seconds to wait for url to send data until it times out.",
)
# TIMEOUT RETRY ATTEMPTS
@click.option(
    "-c",
    "--chances",
    default=1,
    help="Max # of connection retries before labeling a link as timed out.",
)
# STOP LOGGING INTO FILES
@click.option(
    "-dl",
    "--disable_logging",
    is_flag=True,
    help="Prevents creation of any log type files (does not overwrite -show-afterlife)",
)
# VERBOSE MODE
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Provide more information on the reaping process.",
)
# FILE(S)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
# REAPER
def reap(**kwargs):
    """Command that reaps links from markdown files based on your options"""
    if not kwargs["files"]:
        raise click.BadParameter("No file(s) provided")

    if kwargs["ignore_ssl"]:
        click.echo("\nWarning: ignoring SSL errors. Use with caution.")

    # Transform multiple options into lists
    kwargs["ignore_urls"] = kwargs["ignore_urls"].replace(" ", "").split(",")
    kwargs["reap_status"] = parse_status_codes(
        kwargs["reap_status"].replace(" ", "").split(",")
    )

    # print(kwargs)

    exit_code = link_collector.file_manip(kwargs)

    # Exit based on if there are reaped links
    sys.exit(exit_code)


def parse_status_codes(status_codes: list) -> list:
    """Checks for any special code formats, like 3*/3** & 30* and adds appropriate codes to reap list

    Example: 3* would add 300-399 and 34* would add 340-349
    """

    true_codes = []

    for code in status_codes:
        # check for "*"
        index = code.find("*")

        if index == -1:
            true_codes.append(code)
        elif index > 3 or index == 0:
            click.echo("Ignored invalid status code input: " + code)
        # get range of codes based on location of "*"
        else:
            multiplier = int(
                100 ** (1 / index)
            )  # Turn multipier into 100 for index 1 or 10 for index 2
            num = int(code[0:index])  # Capture the number(s) before *
            codes = range(
                num * multiplier, (num + 1) * multiplier
            )  # Get the approiate range
            true_codes.extend(codes)

    return true_codes


if __name__ == "__main__":
    link_reaper()
