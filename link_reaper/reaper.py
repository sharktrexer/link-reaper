"""CLI for link_reaper"""

import click
from . import link_collector

# pylint: disable=trailing-whitespace, line-too-long, anomalous-backslash-in-string
INTRO = """ 
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

@click.group(name="link_reaper")
def link_reaper():
    """Groups CLI commands under 'link_reaper' and prints intro text"""
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
@click.option("-ig", "--ignore_ghosts", is_flag=True, help="Ignore redirect links.")
# IGNORE DUPLICATES
@click.option(
    "-id", "--ignore_doppelgangers", is_flag=True, help="Ignore duplicate links."
)
# IGNORE SSL
@click.option(
    "-is",
    "--ignore_ssl",
    is_flag=True,
    help="Ignore links that result in SSL errors. Not very secure so use with caution.",
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
        "Ignores specific links you want to whitelist."
        "Enter each url comma separated."
    ),
)
# REAP LIST OF STATUS CODES
@click.option(
    "-rs",
    "--reap_status",
    type=str,
    default="",
    help=(
        "Status codes you want to be reaped (404, 500, 521 and 300s are default)."
        "Enter each code comma separated."
    ),
)
# TIMEOUT
@click.option(
    "-p",
    "--patience",
    default=15,
    help="Max # of seconds to wait for url to to send data.",
)
# FILE(S)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
# REAPER
def reap(
    files,
    show_afterlife,
    merciful,
    ignore_ghosts,
    ignore_doppelgangers,
    ignore_urls,
    reap_status,
    ignore_ssl,
    ignore_timeouts,
    patience,
):
    """Command that reaps links from markdown files based on your options"""
    if not files:
        raise click.BadParameter("No file(s) provided")

    if ignore_ssl:
        click.echo("\nWarning: ignoring SSL errors. Use with caution.")

    # Transform multiple options into lists
    ignore_urls = ignore_urls.replace(" ", "").split(",")
    reap_status = reap_status.replace(" ", "").split(",")

    link_collector.collect_links(
        files,
        overwrite=not merciful,
        do_ignore_copies=ignore_doppelgangers,
        do_ignore_redirect=ignore_ghosts,
        do_show_afterlife=show_afterlife,
        ignored_links=ignore_urls,
        reap_codes=reap_status,
        do_ignore_ssl=ignore_ssl,
        ignore_timeouts=ignore_timeouts,
        max_timeout=patience,
    )


if __name__ == "__main__":
    link_reaper()
