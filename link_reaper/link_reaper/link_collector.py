# checks links in markdown files and prints results
# results are temp stored so the user can decide to implement them or not
import re, os, requests, urllib.parse, click.utils

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
    reap_codes: list = [], ignored_links: list = [], guides: list = [],
    do_ignore_copies = False, do_ignore_redirect = False,  do_ignore_ssl = True,
    do_show_afterlife = False, overwrite = True,
    do_reap_timeouts = False, max_timeout = 1,
    ):

    if not directory:
        directory = os.getcwd()

    file_index = -1
    do_verify = not do_ignore_ssl
    
    # Loop thru all inputted files, and create a reaped copy
    for file in files:
        
        file_index += 1
        
        #file paths
        reap_file_path = directory + "reaped-" + file
        afterlife_file_path = directory + "afterlife-" + file
        log_file_path = directory + "log-" + file
        file = directory + file
        
        file_urls = []
        undead_links = []
        file_log = []
        
        guide_urls = []
        
        #if guides:
            
        
        with (open(file, "r", encoding='utf-8') as cur_file, 
              open(reap_file_path, "w", encoding='utf-8') as reap_file):
            
            file_line = -1
            print("\n")
            
            for line in cur_file:

                # line count
                file_line += 1
                # Url's reason for being a zombie/getting deleted or modified
                note = ""
                
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
                dupe_status = 200
                for grabbed_link in file_urls:
                    if raw_url == grabbed_link.link_url:
                        note = ("Doppelganger of " + 
                                        grabbed_link.link_name + ", Line " +
                                        str(grabbed_link.file_line))
                        dupe_status = grabbed_link.status
                        is_dupe = True
                        break       
                
                # Status doesn't matter here, this is only to track grabbed links found in md
                basic_link = Link(file_line, link_name, raw_url, -1, "")
                file_urls.append(basic_link)
                
                dupe_link = Link(file_line, link_name, raw_url, dupe_status, note)
                
                # Handle copies
                if is_dupe:
                    if do_ignore_copies:
                        # Log copies just so user knows what has been ignored
                        file_log.append(dupe_link)
                    else:
                        # otherwise dupes are known as undead
                        undead_links.append(dupe_link)
                        continue
                
                # Grabbing links in respect to cli options
                req = None
                status = -1
                try:
                    req = requests.head(raw_url, 
                                        timeout=max_timeout, 
                                        headers={'User-Agent': 'link-reaper'},
                                        verify=do_verify
                                        )
                # Handle reaping timeouts if desired
                except requests.exceptions.Timeout as e:
                    if do_reap_timeouts:
                        basic_link.note = str(e)
                        undead_links.append(basic_link)
                        continue
                    else:
                        reap_file.write(line)
                        
                        basic_link.note = "Url Timed Out: " + str(e)
                        file_log.append(basic_link)
                        continue
                except Exception as e:
                    basic_link.write(line)
                    
                    link_info.note = "Error Resolving Url: " + str(e)
                    file_log.append(basic_link)
                    continue
                
                #get link info
                status = req.status_code
                file_urls[-1].status = status
                
                # Link and its info
                link_info = Link(
                    file_line,
                    link_name, 
                    raw_url,
                    status,
                    ""
                    )
                
                # url has a redirect
                if 'location' in req.headers:
                    url_after_redirect = req.headers['location'] 
                    
                    if do_ignore_redirect:
                        # log ignored redirects
                        link_info.note = "This link is a ghost of " + url_after_redirect
                        file_log.append(link_info)
                    else:
                        # write new url to reap file
                        new_line = line.replace(raw_url, url_after_redirect)
                        reap_file.write(new_line)
                        note = "Discovered as Ghost (Redirect)"
                
                # Handle status codes that user wants reaped
                if status in reap_codes:
                        link_info.note += " This link responded with a status code that you want ignored"
                # Handling other codes
                elif (status >= 100 and status < 300) or status in reap_codes:
                    reap_file.write(line)
                    # Log ignored status codes
                elif status == 404:
                    link_info.note = "Responded 404"
                elif status >= 400 and status < 500:
                    link_info.note = "Unauthorized Access"
                    file_log.append(link_info)
                    reap_file.write(line)
                    continue
                elif status >= 500 and status < 600:
                    link_info.note = "Server Error"
                    file_log.append(link_info)
                    reap_file.write(line)
                    continue
                
                undead_links.append(link_info)
        
        # Write undead_links to afterlife-filename.md
        if do_show_afterlife:   
            with open(afterlife_file_path, 'w', encoding='utf-8') as afterlife_file:
                for link in undead_links:
                    afterlife_file.write(link.__str__() + "\n")
                    
        # Write log to log-filename.md
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            for link in file_log:
                log_file.write(link.__str__() + "\n")
            
        # Replace 
        if overwrite: 
            os.replace(reap_file_path, file)
            
        # Print results
        print("Found links in: ", file)
        for url in file_urls:
            click.echo("Line:"+ str(url.file_line) + " | " + url.link_name + url.link_url)
            
        print("\nProblematic links in: ", file)
        for url in undead_links:
            click.echo(url)
            
        print("Other link results in ", log_file_path, " for additional info")
        

