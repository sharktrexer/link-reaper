#shell commands
import click
import link_collector

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
    
@link_reaper.command(context_settings={"ignore_unknown_options": True})
@click.option('-s', '--show_afterlife', is_flag=True)
@click.option('-m', '--merciful', is_flag=True)
@click.option('-ig', '--ignore-ghosts', is_flag=True)
@click.option('-is','--ignore-shapeshifters', is_flag=True, help="Ignore duplicate links")
@click.option('-iu','--ignore-urls', multiple=True)
@click.option('-i', '--ignore', multiple=True, help="Ignored status codes")
@click.option('-p', '--patience', default=3, help="Max # of seconds to wait for url to respond before reaping")
@click.option('-g', '--guides', multiple=True, type=click.Path(exists=True))
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def reap(files, guides, 
         show_afterlife, merciful, 
         ignore_ghosts, ignore_shapeshifters, 
         ignore_urls, ignore, patience
         ):
    if guides and len(guides) > 1 and len(files) != len(guides):
        raise click.BadParameter('Number of guides must match the number of files,' 
                                 'or only one guide should be provided')
    
    link_collector.collect_links(files, guides=guides, overwrite=merciful, 
                                 do_ignore_copies=ignore_shapeshifters, 
                                 do_ignore_ghosts=ignore_ghosts, 
                                 do_show_afterlife=show_afterlife, 
                                 ignored_links=ignore_urls, 
                                 ignored_codes=ignore, max_timeout=patience)
    

if __name__ == '__main__':
    link_reaper()