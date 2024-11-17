#shell commands
import click
from . import link_collector

PROMPT = "💀 "
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠃"""

@click.group(name="link_reaper")
def link_reaper():
    click.echo(INTRO)
    
# TODO: add verbose(?) mode that explains more about what is happening
# TODO: let user know what options they used? Like if merciful then print "not overwriting files"
@link_reaper.command(context_settings={"ignore_unknown_options": True})
@click.option('-s', '--show_afterlife', is_flag=True, help="Create an afterlife-filename.md for each checked file that only contains the reaped links.")
@click.option('-m', '--merciful', is_flag=True, help="Instead of overwriting files, create a reaped-filename.md for each checked file that contains applied changes.")
@click.option('-ig', '--ignore_ghosts', is_flag=True, help="Ignore redirect links.")
@click.option('-id','--ignore_doppelgangers', is_flag=True, help="Ignore duplicate links.")
@click.option('-is', '--ignore_ssl', is_flag=True, help="Ignore links that result in SSL errors. Not very secure so use with caution.")
@click.option('-rt', '--reap_timeouts', is_flag=True, help="Reap links that time out.")
@click.option('-iu','--ignore_urls', multiple=True, type=str, help="Ignores specific links you want to whitelist. Use this option for each url.")
@click.option('-rs', '--reap_status', multiple=True, type=int, help="Status codes you want to be reaped (404 and 300s are default). Use this option per each code.")
@click.option('-p', '--patience', default=10, help="Max # of seconds to wait for url to to send data.")
@click.option('-g', '--guides', type=click.Path(exists=True))
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def reap(files, guides, 
         show_afterlife, merciful, 
         ignore_ghosts, ignore_doppelgangers, 
         ignore_urls, reap_status, ignore_ssl,
         reap_timeouts, patience
         ):
    
    if not files:
        raise click.BadParameter('No files provided')
    
    if guides and len(guides) > 1 and len(files) != len(guides):
        raise click.BadParameter('Number of guides must match the number of files,' 
                                 'or only one guide should be provided')
    
    if ignore_ssl:
        click.echo('\nWarning: ignoring SSL errors. Use with caution.')
    
    link_collector.collect_links(files, guides=guides, overwrite= not merciful, 
                                 do_ignore_copies=ignore_doppelgangers, 
                                 do_ignore_redirect=ignore_ghosts, 
                                 do_show_afterlife=show_afterlife, 
                                 ignored_links=ignore_urls, 
                                 reap_codes=reap_status, do_ignore_ssl=ignore_ssl,
                                 do_reap_timeouts=reap_timeouts, max_timeout=patience)
    

if __name__ == '__main__':
    link_reaper()