# Stores useful information about a link
class Link:
    def __init__(self, 
            file_line: int,
            name: str, 
            url: str,
            status: int = -1,
            note: str = "",
            history: list = [],
            ):

        self.file_line = file_line
        self.name = name
        self.url = url
        self.status = status
        self.note = note
        self.history = history

    def __str__(self):
        if self.history:
            
            url_histroy = (" -> ".join(self.history)).join(" -> (" + self.url + ")")
            
            return (f"Line {self.file_line}, Status {self.status} | " +
               url_histroy + " | " +
               f"{self.note}")
        else:
            return (f"Line {self.file_line}, Status {self.status} | " 
                f"{self.url} | " 
                f"{self.note}")
