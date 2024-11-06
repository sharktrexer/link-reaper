# checks links in markdown files and prints results
# results are temp stored so the user can decide to implement them or not
import re, os, requests, urllib.parse

from link import Link
''' TODO: add ability to accept automatic links inbetween <>
    perhaps enable ability to just check any links in entire file, not just markdown
'''

# grabs content between [ and )
# obtaining: [name](https://test.com)
LINK_RE = re.compile(r'\[(.*?)\)') 
# [name]
LINK_NAME_RE = re.compile(r'\[(.*?)\]') 
# (url)
LINK_URL_RE = re.compile(r'\((.*?)\)') 

# grab github readme links as a list of tuple strings 
# (line_num, name, url, status_code, reason)
def collect_links(
    files, directory: str = "",
    ignored_codes: list = [], ignored_links: list = [], guides: list = [],
    do_ignore_copies = False, do_ignore_ghosts = False, do_show_afterlife = False, overwrite = True,
    do_reap_timeouts = False, max_timeout = 1
    ):

    # Loop thru all inputted files, and create a reaped copy
    for file in files:
        
        #file paths
        reap_file_path = directory + "reaped-" + file
        afterlife_file_path = directory + "afterlife-" + file
        file = directory + file
        
        file_urls = []
        undead_links = []
        
        with (open(file, "r", encoding='utf-8') as cur_file, 
              open(reap_file_path, "w", encoding='utf-8') as reap_file):
            
            file_line = -1
            print("\n")
            
            for line in cur_file:

                # line count
                file_line += 1
                # Url's reason for being a zombie/getting deleted or modified
                zombie_reason = ""
                
                # Trying to search for a markdown link
                link_line = LINK_RE.search(line)
                if not link_line:
                    reap_file.write(line)
                    continue
                
                # Found a markdown link
                link_line = link_line.group()
                
                link_name = LINK_NAME_RE.search(link_line)
                link_url = LINK_URL_RE.search(link_line)
                
                # only grab regex matches, otherwise ignore
                if(link_name == None or link_url == None):
                    reap_file.write(line)
                    continue;
                
                # grab text between parentheses
                link_name = link_name.group()[1:-1]
                raw_url = link_url.group()[1:-1]
                
                #validate that the captured "link" is actually a link
                try:
                    parsed_url = urllib.parse.urlparse(raw_url)
                    if not parsed_url.scheme:
                        reap_file.write(line)
                        continue
                except ValueError:
                    reap_file.write(line)
                    continue
                
                # ignore specified links
                if raw_url in ignored_links:
                    reap_file.write(line)
                    continue
                
                # deal with duplicate links
                is_dupe = False  
                if not do_ignore_copies:
                    for grabbed_link in file_urls:
                        if raw_url == grabbed_link.link_url:
                            zombie_reason = ("Duplicate Link of " + 
                                            grabbed_link.link_name + ", Line " +
                                            str(grabbed_link.file_line))
                            is_dupe = True
                            break       
                
                file_urls.append(Link(file_line, link_name, raw_url, 200, ""))
                
                # Handle copies
                if is_dupe:
                    undead_links.append(Link(file_line, link_name, raw_url, 200, zombie_reason))
                    continue
                
                # only grab links that respond with 404 or 300s
                # TODO: grab links that timeout as zombies, perhaps a new option for that?
                req = None
                try:
                    req = requests.head(raw_url, 
                                        timeout=max_timeout, 
                                        headers={'User-Agent': 'link-reaper'}
                                        )
                except Exception as e:
                    #print("Error Resolving Url: ", e)
                    reap_file.write(line)
                    continue
                
                #get link info
                status = req.status_code
                url_after_redirect = ""
                if not do_ignore_ghosts and 'location' in req.headers:
                    #print("New url: ", req.headers['location'])
                    url_after_redirect = req.headers['location'] 
                    
                
                if (status >= 100 and status < 300) or status in ignored_codes:
                    reap_file.write(line)
                    continue
                elif status >= 300 and status < 400: 
                    # if redirected and not ignored, write new url
                    if url_after_redirect != "":
                        new_line = line.replace(raw_url, url_after_redirect)
                        #print("Old line: ", line, "New line: ", new_line)
                        reap_file.write(new_line)
                        zombie_reason += " Ghost Link (Redirect)"
                    else:
                        reap_file.write(line)
                        zombie_reason += "Link redirects, not reaped despite its ghostly nature"
                elif status == 404:
                    zombie_reason += " Connection couldn't be established"
                elif status >= 400 and status < 500:
                    zombie_reason += " Unauthorized, not reaped"
                    reap_file.write(line)
                elif status >= 500 and status < 600:
                    zombie_reason += " Server Error, not reaped"
                    reap_file.write(line)
                
                # (file line num, name, url, status, reason)
                link_info = Link(
                    file_line,
                    link_name, 
                    raw_url,
                    status,
                    zombie_reason
                    )
                #print(link_info, "\n")
                undead_links.append(link_info)
        
        # Write undead_links to afterlife-filename.md
        if do_show_afterlife:   
            with open(afterlife_file_path, 'w', encoding='utf-8') as afterlife_file:
                for link in undead_links:
                    afterlife_file.write(link.__str__() + "\n")
            
        # Replace 
        if overwrite: 
            os.replace(reap_file_path, file)
            
        #TODO: print using click.echo()    
        # Print results
        print("Found links in: ", file)
        for url in file_urls:
            print("Line:", url.file_line, " | ", url.link_name, url.link_url)
            
        print("\nProblematic links in: ", file, '\nAssume they are reaped unless specified\n')
        for url in undead_links:
            print(url)
        
    return undead_links 

