# checks links in markdown files and prints results
# results are temp stored so the user can decide to implement them or not
import re, urllib.request

tests = [
    "[test](https://test.com)", 
    "[haha(https://fail.com)", 
    "[section](#test-head)", 
    "[relative](docs/README.md)",
    "[invalid](https//invalid.com)"
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
    ignored_codes, ignored_links,
    do_ignore_copies, do_ignore_messengers
    ):

    zombie_links = []
    file_line = 0
    print("\n")
    
    for line in file_content:
        
        # line info
        link_line = LINK_RE.search(line).group()
        print("link line: ", link_line)
        
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
        try:
            true_url = urllib.request.urlopen(link_url)
            print("true url: ", true_url)
        except Exception as e:
            print("url not valid. Reason: ", e)
            continue;
        
        #get link status code
        status = true_url.status_code
        zombie_reason = ""
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
        link_info = (
            file_line,
            link_name, 
            link_url,
            status,
            zombie_reason
            )
        print("info: ", link_info, "\n")
        zombie_links.append(link_info)
        
    return zombie_links 
    

# with open("test/README.md", "r", encoding='utf-8') as f:
#     content = f.read()

# print(content)