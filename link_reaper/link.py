# Stores useful information about a link
class Link:
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
        else:
            return (
                f"Line {self.file_line}, Status {self.status} | "
                f"{self.url} | "
                f"{self.note}"
            )
