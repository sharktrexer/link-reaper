"""Contains Link related classes"""


class Link:
    """Stores useful information about a link"""

    def __init__(
        self,
        file_line: int,
        name: str,
        url: str,
        status: int = -1,
        note: str = "",  # extra info about the link response or how this program handled it
        history: list = [],  # history of redirects, with last item being most recent
        result: str = "",  # What should be done with the link
        og_code: int = -1,  # Original response code that started the redirection
    ):
        self.file_line = file_line
        self.name = name
        self.url = url
        self.status = status
        self.note = note
        self.history = history
        self.result = result
        self.og_code = og_code

    def __str__(self):
        if self.history:
            url_history = " > ".join(self.history)
            url_history += " > " + self.url

            return (
                f"Line {self.file_line}, Status {self.status} | "
                + f"{url_history} | "
                + f"{self.note}"
            )

        return f"Line {self.file_line}, Status {self.status} | {self.url} | {self.note}"

    def get_as_md_form(self):
        """Formats link back into markdown: [name](url)"""
        return "[" + self.name + "](" + self.url + ")"


class LinkHolder:
    """Stores processed Links and provides helper functions"""

    def __init__(
        self,
        reaped_links: list,
        logged_links: list,
        found_links: list,
    ):
        self.reaped_links = reaped_links
        self.logged_links = logged_links
        self.found_links = found_links

    def store_link(self, link: Link):
        """Stores link in appropriate list"""
        if link.result in ("Reaped", "Updated"):
            self.reaped_links.append(link)
        elif link.result == "Logged":
            self.logged_links.append(link)
        elif not link.result:
            self.found_links.append(link)

    def check_if_dupe(self, link: Link):
        """Checks if link has already been found and returns the copy"""
        for found_link in self.found_links:
            if link.url == found_link.url or link.url in found_link.history:
                return found_link
        return None
