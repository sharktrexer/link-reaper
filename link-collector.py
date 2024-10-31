# checks links in markdown files and prints results
# results are temp stored so the user can decide to implement them or not
import re, urllib.request
from urllib.error import URLError

from link import Link

tests = [
    "[test](https://test.com)", 
    "[haha(https://fail.com)", 
    "[section](#test-head)", 
    "[relative](docs/README.md)",
    "[invalid](https://invalid.com)",
    "[github](https://github.com/sharktrexer)",
    "[404](https://www.example.com/nonexistentpage)",
        ]

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
    file_content, 
    ignored_codes = [], ignored_links = [],
    do_ignore_copies = False, do_ignore_messengers = False,
    max_timeout = 1
    ):

    zombie_links = []
    file_line = -1
    zombie_reason = None
    print("\n")
    
    for line in file_content:
        
        file_line += 1
        
        # line info
        link_line = LINK_RE.search(line).group()
        print("Checking ", link_line)
        
        link_name = LINK_NAME_RE.search(link_line)
        link_url = LINK_URL_RE.search(link_line)
        
        # only grab regex matches
        if(link_name == None or link_url == None):
            continue;
        
        # grab text between parentheses
        link_name = link_name.group()[1:-1]
        link_url = link_url.group()[1:-1]
        
        # ignore specified links
        if link_url in ignored_links:
            continue
        
        # deal with duplicate links 
        # TODO:
        
        # only grab valid links 
        # TODO: grab links that timeout as zombies
        try:
            true_url = urllib.request.urlopen(link_url, timeout=max_timeout)
            #print("true url: ", true_url)
        except ValueError as e:
            print("All Good. Reason: ", e)
            continue
        except Exception as e:
            zombie_reason = e
        
        #get link status code
        # TODO: try python requests lib instead? 
        # problem occurs when dealing with http responses
        status = 400 #true_url.status_code
        
        if not zombie_reason:
            if (status <= 100 and status < 300) or status in ignored_codes:
                print("URL is Valid")
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
        zombie_links.append(link_info)
        
        
    return zombie_links 
    

collect_links(tests)

# with open("test/README.md", "r", encoding='utf-8') as f:
#     content = f.read()

# print(content)