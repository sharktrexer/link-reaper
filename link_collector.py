# checks links in markdown files and prints results
# results are temp stored so the user can decide to implement them or not
import re, urllib.request, os
from urllib.error import URLError

from link import Link

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
    files, directory = None,
    ignored_codes = [], ignored_links = [], guides = [],
    do_ignore_copies = False, do_ignore_ghosts = False, do_show_afterlife = False, overwrite = True,
    max_timeout = 1
    ):

    # Loop thru all inputted files, and create a reaped copy
    for file in files:
        
        #file paths
        reap_file_path = directory + "reaped-" + file
        afterlife_file_path = directory + "afterlife-" + file
        file = directory + file
        
        with (open(file, "r", encoding='utf-8') as cur_file, 
              open(reap_file_path, "w", encoding='utf-8') as reap_file):
            
            undead_links = []
            file_line = -1
            zombie_reason = None
            print("\n")
            
            for line in cur_file:

                # line count
                file_line += 1
                
                # Trying to search for a markdown link
                link_line = LINK_RE.search(line)
                if not link_line:
                    reap_file.write(line)
                    continue
                
                # Found a markdown link
                link_line = link_line.group()
                print("Checking ", link_line)
                
                link_name = LINK_NAME_RE.search(link_line)
                link_url = LINK_URL_RE.search(link_line)
                
                # only grab regex matches, otherwise ignore
                if(link_name == None or link_url == None):
                    reap_file.write(line)
                    continue;
                
                # grab text between parentheses
                link_name = link_name.group()[1:-1]
                link_url = link_url.group()[1:-1]
                
                # ignore specified links
                if link_url in ignored_links:
                    reap_file.write(line)
                    continue
                
                # deal with duplicate links 
                if not do_ignore_copies:
                    for grabbed_link in undead_links:
                        if link_url == grabbed_link.link_url:
                            zombie_reason = ("Duplicate Link of " + 
                                            grabbed_link.link_name + ", Line " +
                                            str(grabbed_link.file_line))
                            break       
                
                # only grab valid links 
                # TODO: grab links that timeout as zombies
                try:
                    true_url = urllib.request.urlopen(link_url, timeout=max_timeout)
                    #print("true url: ", true_url)
                except ValueError as e:
                    print("All Good. Reason: ", e)
                    reap_file.write(line)
                    continue
                except Exception as e:
                    zombie_reason = e
                
                #get link status code
                # TODO: try python requests lib instead? 
                # problem occurs when dealing with http responses
                try:
                    status = true_url.status_code
                except Exception as e:
                    status = 400
                    
                if not zombie_reason:
                    if (status <= 100 and status < 300) or status in ignored_codes:
                        print("URL is Valid")
                        reap_file.write(line)
                        continue
                    elif status <= 300 and status < 400: #TODO: take into account do_ignore_messengers
                        zombie_reason = "Redirect"
                    elif status <= 400 and status < 500:
                        zombie_reason = "Client Error"
                    elif status <= 500 and status < 600:
                        zombie_reason = "Server Error"
                
                # (file line num, name, url, status, reason)
                link_info = Link(
                    file_line,
                    link_name, 
                    link_url,
                    status,
                    zombie_reason
                    )
                print(link_info, "\n")
                undead_links.append(link_info)
        
        #Write undead_links to afterlife-filename.md
        if do_show_afterlife:   
            with open(afterlife_file_path, 'w', encoding='utf-8') as afterlife_file:
                for link in undead_links:
                    afterlife_file.write(link.__str__() + "\n")
            
        #Replace 
        if overwrite: 
            os.replace(reap_file_path, file)
        
    return undead_links 

