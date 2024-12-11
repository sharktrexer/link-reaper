"""checks links in markdown files and prints results"""

import re
import os

from collections import namedtuple
from urllib.parse import urlparse, urlsplit, urlunsplit

import requests
import click.utils

from . import link_info
from requests.exceptions import Timeout, ConnectTimeout
from requests.packages import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# grabs content between [ and )
# obtaining: [name](https://test.com)
LINK_RE = re.compile(r"\[(.*?)\)")
# [name]
LINK_NAME_RE = re.compile(r"\[(.*?)\]")
# (url)
LINK_URL_RE = re.compile(r"\((.*?)\)")
# <url>
ALT_LINK_URL_RE = re.compile(r"\<(.*?)\>")

# Named Tuple to store name and url of md links
MarkdownLink = namedtuple("Markdown_Link", ["name", "url"])


def collect_links(
    files,
    directory: str = "",
    reap_codes: list = [],
    ignored_links: list = [],
    do_ignore_copies=False,
    do_ignore_redirect=False,
    do_ignore_ssl=True,
    do_show_afterlife=False,
    overwrite=True,
    ignore_timeouts=False,
    max_timeout=15,
):
    """Checks all links in markdown files and reaps them depending on options."""
    if not directory:
        directory = os.getcwd() + "\\"

    file_index = -1
    do_verify = not do_ignore_ssl

    # Loop thru all inputted files, and create a reaped copy
    for file in files:
        file_index += 1

        # file paths
        reap_file_path = directory + "reaped-" + file
        afterlife_file_path = directory + "afterlife-" + file
        log_file_path = directory + "log-" + file
        file = directory + file

        file_urls = []
        undead_links = []
        file_log = []

        with (
            open(file, "r", encoding="utf-8") as cur_file,
            open(reap_file_path, "w", encoding="utf-8") as reap_file,
        ):
            click.echo("Processing " + file + "...\n")

            for line_num, line in enumerate(cur_file, start=1):
                # Grabbing all md links in the file line [name](url) or <url>
                line_links = grab_md_links(line)

                # ignore lines without possible markdown links
                if not line_links:
                    reap_file.write(line)
                    continue

                processed_line_links = []  # Track links that have been checked

                for md_link in line_links:
                    link_name = md_link[0]
                    raw_url = md_link[1]

                    # validate that the captured "link" is actually a http url
                    if not check_url_validity(raw_url):
                        reap_file.write(line)
                        continue

                    click.echo("Found " + raw_url)

                    # ignore specified links
                    if raw_url in ignored_links:
                        reap_file.write(line)
                        click.echo("Ignored as specified")
                        continue

                    cur_link = link_info.Link(line_num, link_name, raw_url, history=[])

                    # deal with duplicate links
                    is_dupe = False
                    for grabbed_link in file_urls:
                        if (
                            raw_url == grabbed_link.url
                            or raw_url in grabbed_link.history
                        ):
                            cur_link.note = (
                                "Doppelganger of "
                                + grabbed_link.name
                                + ", Line "
                                + str(grabbed_link.file_line)
                            )
                            cur_link.status = grabbed_link.status
                            is_dupe = True
                            break

                    # keeps track of valid links seen
                    file_urls.append(cur_link)

                    # Handle copies
                    if is_dupe:
                        if do_ignore_copies:
                            # Log copies just so user knows what has been ignored
                            cur_link.result = "Logged"
                        else:
                            # otherwise dupes are known as undead
                            cur_link.result = "Reaped"

                        # dont need to evaluate duplicate urls
                        processed_line_links.append(cur_link)
                        continue

                    obtain_request(
                        cur_link,
                        do_verify,
                        ignore_timeouts,
                        max_timeout,
                        do_ignore_redirect,
                        reap_codes,
                    )

                    processed_line_links.append(cur_link)

                # Handle every md link in line
                new_line = ""
                reaped_links_num = 0
                do_delete_line = False
                for cur_link in processed_line_links:
                    if cur_link.result == "Reaped":
                        undead_links.append(cur_link)

                        # If only one link in line, then line can be deleted
                        if len(processed_line_links) == 1:
                            do_delete_line = True
                            continue

                        # If multiple links in a line, just remove the link
                        if len(processed_line_links) > 1:
                            reaped_links_num += 1
                            new_line = line.replace(cur_link.get_as_md_form(), "")

                            # If all links in line are reaped, then line can be deleted
                            if reaped_links_num == len(processed_line_links):
                                do_delete_line = True
                                new_line = ""

                        continue

                    if cur_link.result == "Logged":
                        file_log.append(cur_link)
                        continue

                    if cur_link.result == "All Good":
                        # If redirect occured, update the link, reap old one
                        if cur_link.history:
                            if new_line:
                                # Compound updates
                                new_line = new_line.replace(
                                    cur_link.history[0], cur_link.url
                                )
                            else:
                                new_line = line.replace(
                                    cur_link.history[0], cur_link.url
                                )

                            cur_link.status = (
                                cur_link.og_code
                            )  # Get code of original url
                            undead_links.append(cur_link)

                        continue

                # Modifying Line
                if new_line:
                    reap_file.write(new_line.strip() + "\n")
                    print("LINE MODIFIED")
                elif do_delete_line:
                    print("LINE DELETED")
                else:
                    reap_file.write(line)
                    print("LINE UNCHANGED")
                # End Of Line
            # EOF

        click.echo(
            "\nReaped/Updated "
            + str(len(undead_links))
            + "/"
            + str(len(file_urls))
            + " links in "
            + file
        )

        # Write undead_links to afterlife-filename.md
        if do_show_afterlife:
            with open(afterlife_file_path, "w", encoding="utf-8") as afterlife_file:
                for link in undead_links:
                    afterlife_file.write(str(link) + "\n")

        # Write log to log-filename.md
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            for link in file_log:
                log_file.write(str(link) + "\n\n")

        # Replace
        if overwrite:
            os.replace(reap_file_path, file)

        # Print results
        # print("Found links in: ", file)
        # for url in file_urls:
        #    click.echo("Line "+ str(url.file_line) + " | " + url.link_name +" " + url.link_url)

        print("\nProblematic links in: ", file)
        for url in undead_links:
            click.echo(url)

        print("Other link results in ", log_file_path, " for additional info")


def find_markdown_link(line):
    """Uses regex to find markdown link [name](url) or <url> DEPRECATED"""
    md_link = LINK_RE.search(line)

    # if [name](url) doesn't match, try <url>
    if not md_link:
        md_link = ALT_LINK_URL_RE.search(line)
        if not md_link:
            return None

        link_name = ""
        raw_url = md_link.group()[1:-1]

        return (link_name, raw_url)

    # separating [name] and (url)
    link_name = LINK_NAME_RE.search(md_link.group())
    link_url = LINK_URL_RE.search(md_link.group())

    # ensure regex match includes [name] and (url) and not something like [blah)
    if link_name is None or link_url is None:
        return None

    # exclude brackets
    link_name = link_name.group()[1:-1]
    raw_url = link_url.group()[1:-1]

    return (link_name, raw_url)


# if url has a scheme it is valid
def check_url_validity(url):
    """Uses urlparse to check for valid url string"""
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            return False
    except ValueError:
        return False

    return True


def obtain_request(
    link: link_info.Link,
    do_verify: bool,
    ignore_timeouts: bool,
    max_timeout: int,
    do_ignore_redirect: bool,
    reap_codes: list,
):
    """Tests links for responses in respect to cli options"""
    # Loop for as many times are there are redirects
    while True:
        # print("checking: ", link.url)
        # print("Current history: ", link.history)
        # print("Link: ", link)

        try:
            req = requests.head(
                link.url,
                timeout=max_timeout,
                headers={"User-Agent": "link-reaper"},
                verify=do_verify,
            )
        # Handle reaping timeouts based on timeout var if desired
        except Timeout as e:
            if ignore_timeouts:
                link.note = "Url Timed Out: " + str(e)
                link.result = "Logged"
                return

            link.note = str(e)
            link.result = "Reaped"
            return

        # Handling connection errors and connection timeouts
        except (ConnectionError, ConnectTimeout) as e:
            link.note = str(e)
            link.result = "Reaped"
            return

        # Other unknown errors aren't reaped, up to the user to take action
        except Exception as e:
            link.note = "Error Resolving Url: " + str(e)
            link.result = "Logged"
            return

        # get link info
        link.status = req.status_code

        # Store original code before redirects
        if not link.history:
            link.og_code = link.status

        does_redirect = "location" in req.headers
        # print(does_redirect)
        # url has a redirect
        if does_redirect:
            if do_ignore_redirect:
                # log ignored redirects
                link.note = "This link is a ghost"
                link.result = "Logged"
                return

            url_after_redirect = req.headers["location"]

            # if redirect is just a new path, replace the path in old url
            if url_after_redirect[0] == "/":
                split_url = list(urlsplit(link.url))
                # path replacement
                split_url[2] = url_after_redirect
                url_after_redirect = urlunsplit(split_url)

            # update link to new url, keeping track of redirects
            link.history.append(link.url)
            link.url = url_after_redirect
            link.note = "Updated to most current redirect"
            continue

        status = link.status
        # Handle status codes that user wants reaped
        if str(status) in reap_codes:
            link.note += " This link responded with a status code that you want reaped"
            link.result = "Reaped"

        # Handling other codes
        elif 100 <= status < 400 and not does_redirect:
            link.result = "All Good"

        elif status == 404:
            link.note = "Does not exist"
            link.result = "Reaped"

        elif 400 <= status < 500:
            link.note = "Unauthorized Access"
            link.result = "Logged"

        elif status in (500, 521):
            link.note = "Server Could Not Handle Request"
            link.result = "Reaped"

        elif 501 <= status < 600:
            link.note = "Unknown Server Error"
            link.result = "Logged"

        return


def grab_md_links(line: str) -> list:
    """
    Captures markdown links without use of regex
    Assumes url doesn't contain parenthesis, and is a markdown link [name](url) or <url>
    """

    md_links = []
    start_capture = 0
    capturing_chevrons = False
    starting_name = False
    found_name = False
    end_name = 0
    starting_url = False
    end_capture = 0

    for ind, c in enumerate(line):
        # For <url>
        if c == "<" and not starting_name:
            start_capture = ind
            capturing_chevrons = True
            starting_name = True
        elif c == ">" and capturing_chevrons:
            url = line[start_capture : ind + 1]
            # Ignore brackets
            md_links.append(MarkdownLink("", url[1:-1]))
            # Reset
            capturing_chevrons = False
            starting_name = False
        # For [name](url)
        elif c == "[" and not starting_name:
            start_capture = ind
            starting_name = True
        elif (  # Assume [name] if [name]( which assumes [name](url)
            c == "]" and starting_name and ind + 1 < len(line) and line[ind + 1] == "("
        ):
            found_name = True
            end_name = ind
        elif c == "(" and found_name:
            starting_url = True
        elif c == ")" and starting_url:
            end_capture = ind
            # Capture vars without brackets
            name = line[start_capture : end_name + 1]
            url = line[end_name + 1 : end_capture + 1]
            md_links.append(MarkdownLink(name[1:-1], url[1:-1]))
            # Reset
            starting_name = False
            starting_url = False
            found_name = False

    return md_links
