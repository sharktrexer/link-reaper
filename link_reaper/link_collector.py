"""checks links in markdown files and prints results"""

import re
import os

from collections import namedtuple
from urllib.parse import urlparse, urlsplit, urlunsplit

import requests
import click.utils

from requests.exceptions import Timeout, ConnectTimeout
from requests.packages import urllib3
from . import link_info


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


def file_manip(kwargs):
    """Searches and creates files related to link reaping"""

    directory = os.getcwd() + "\\"

    exit_code = 0

    file_index = -1

    files = kwargs["files"]
    overwrite = not kwargs["merciful"]
    dont_log = kwargs["disable_logging"]
    do_show_afterlife = kwargs["show_afterlife"]

    # Per file
    for file in files:
        file_index += 1

        link_storage = link_info.LinkHolder([], [], [])

        # file paths
        reap_file_path = ""
        afterlife_file_path = ""
        log_file_path = ""

        if do_show_afterlife:
            afterlife_file_path = directory + "afterlife-" + file

        if not dont_log:
            reap_file_path = directory + "reaped-" + file
            log_file_path = directory + "log-" + file

        click.echo("Processing " + file + "...\n")

        # Link validating
        if dont_log:
            # Don't make a reap file if not logging
            with open(file, "r", encoding="utf-8") as cur_file:
                for line_num, line in enumerate(cur_file, start=1):
                    collect_links(kwargs, line, line_num, link_storage)
        else:
            # Validate with reap file creation
            with (
                open(file, "r", encoding="utf-8") as cur_file,
                open(reap_file_path, "w", encoding="utf-8") as reap_file,
            ):
                for line_num, line in enumerate(cur_file, start=1):
                    reap_file.write(collect_links(kwargs, line, line_num, link_storage))

        reap_msg = "\nReaped/Updated "

        # Change wording if using a "check" mode
        if dont_log and not overwrite:
            reap_msg = "\nPotentially could reap/update "

        click.echo(
            reap_msg
            + str(len(link_storage.reaped_links))
            + "/"
            + str(len(link_storage.found_links))
            + " links in "
            + file
        )

        # Write undead_links to afterlife-filename.md
        if do_show_afterlife and link_storage.reaped_links:
            with open(afterlife_file_path, "w", encoding="utf-8") as afterlife_file:
                for link in link_storage.reaped_links:
                    afterlife_file.write(str(link) + "\n\n")

        # Write log to log-filename.md if there is anything to log
        if not dont_log and link_storage.logged_links:
            with open(log_file_path, "w", encoding="utf-8") as log_file:
                for link in link_storage.logged_links:
                    log_file.write(str(link) + "\n\n")

        # Replace
        if overwrite:
            os.replace(reap_file_path, file)

        if link_storage.reaped_links:
            click.echo("\nProblematic links in: " + file)
            for url in link_storage.reaped_links:
                click.echo(url)
        else:
            click.echo("\nNo problems found in " + file + "!")

        if not dont_log and link_storage.logged_links:
            click.echo(
                "Other link results in " + log_file_path + " for additional info"
            )

        if not link_storage.found_links:
            click.echo("No links found in " + file)

        # "Failure" exit code if reapable links are found
        if link_storage.reaped_links:
            exit_code = 1

    return exit_code


def collect_links(kwargs, line: str, line_num: int, link_storage: link_info.LinkHolder):
    """Checks all links in markdown files and reaps them depending on options."""

    # Unpacking
    reap_codes = kwargs["reap_status"]
    ignored_links = kwargs["ignore_urls"]
    do_ignore_copies = kwargs["ignore_doppelgangers"]
    do_ignore_redirect = kwargs["ignore_ghosts"]
    do_verify = not kwargs["ignore_ssl"]
    ignore_timeouts = kwargs["ignore_timeouts"]
    max_timeout = kwargs["patience"]
    verbose = kwargs["verbose"]

    # Grabbing all md links in the file line [name](url) or <url>
    line_links = grab_md_links(line)

    # ignore lines without possible markdown links
    if not line_links:
        return line

    for md_link in line_links:
        link_name = md_link[0]
        raw_url = md_link[1]

        # validate that the captured "link" is actually a http url
        if not check_url_validity(raw_url):
            if verbose:
                click.echo("Not a valid url in markdown link: " + raw_url)
            return line

        click.echo(f"(Line {line_num}) " + raw_url)

        # ignore specified links
        if raw_url in ignored_links:
            click.echo("Ignored as specified")
            return line

        cur_link = link_info.Link(line_num, link_name, raw_url, history=[])

        # Check if link has already been found in past loop iteration
        poss_dupe = link_storage.check_if_dupe(cur_link)

        # track found, valid links
        link_storage.store_link(cur_link)

        # handle duplicate links
        if poss_dupe:
            cur_link.note = (
                "Doppelganger of "
                + poss_dupe.name
                + ", Line "
                + str(poss_dupe.file_line)
            )
            cur_link.status = poss_dupe.status

            cur_link.result = "Logged" if do_ignore_copies else "Reaped"

        else:
            # Get requests of non dupe links
            obtain_request(
                cur_link,
                do_verify,
                ignore_timeouts,
                max_timeout,
                do_ignore_redirect,
                reap_codes,
            )

        # Handle the line based on link result
        if cur_link.history:
            # If redirect occured, update the link
            line = line.replace(cur_link.history[0], cur_link.url)

            # Get code of original url
            cur_link.status = cur_link.og_code
            cur_link.result = "Updated"

        # Store links into appropriate log/reap lists
        link_storage.store_link(cur_link)

        if cur_link.result == "Reaped":
            return ""

        return line


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
                link.note = (
                    "This link is a ghost (outdated and requires a redirect update)"
                )
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
            # print("Updated to most current redirect")
            continue

        status = link.status
        # Handle status codes that user wants reaped
        if str(status) in reap_codes:
            link.note += " Responded with a status code that you want reaped"
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

    # capture = []

    # for c in line:

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
