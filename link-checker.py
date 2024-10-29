# checks links in markdown files and prints results
# results are temp stored so the user can decide to implement them or not
import re, os, urllib.parse

tests = [
    "[test](https://test.com)", 
    "[haha(https://fail.com)", 
    "[section](#test-head)", 
    "[relative](docs/README.md)"
        ]

# grabs content between [ and )
# obtaining: [name](https://test.com)
LINK_RE = re.compile(r'\[(.*?)\)') 
# [name]
LINK_NAME_RE = re.compile(r'\[(.*?)\]') 
# (url)
LINK_URL_RE = re.compile(r'\((.*?)\)') 

# grab github readme links as a list of tuple strings (line_num, name, url)
def grab_links():

    grabbed_links = []
    file_line = 0
    print("\n")
    
    for line in tests:
        
        # line info
        link_line = LINK_RE.match(line)
        print("link line: ", link_line.group())
        
        link_name = LINK_NAME_RE.search(link_line.group())
        link_url = LINK_URL_RE.search(link_line.group())
        
        # only grab regex matches
        if(link_name == None or link_url == None):
            continue;
        
        # grab text between parentheses
        link_name = link_name.group()[1:-1]
        link_url = link_url.group()[1:-1]
        
        # only grab https links
        parsed_url = urllib.parse.urlparse(link_url)
        print("parsed url: ", parsed_url)
        if(parsed_url.scheme != 'https'):
            print("url not https: ", link_name, " - ", link_url)
            continue;
        
        # (file line num, name, url)
        link_info = (
            file_line,
            link_name, 
            link_url
            )
        print("info: ", link_info, "\n")
        grabbed_links.append(link_info)
    return grabbed_links 
    

# with open("test/README.md", "r", encoding='utf-8') as f:
#     content = f.read()

# print(content)