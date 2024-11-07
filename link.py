class Link:
    def __init__(self, 
            file_line,
            link_name, 
            link_url,
            status,
            note,
            ):

        self.file_line = file_line
        self.link_name = link_name
        self.link_url = link_url
        self.status = status
        self.note = note

    def __str__(self):
        return (f"Line {self.file_line}, Status {self.status} | " 
               f"[{self.link_name}] ({self.link_url}) | " 
               f"{self.note}")
