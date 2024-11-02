class Link:
    def __init__(self, 
            file_line,
            link_name, 
            link_url,
            status,
            zombie_reason,
            alternate_url = None
            ):

        self.file_line = file_line
        self.link_name = link_name
        self.link_url = link_url
        self.status = status
        self.zombie_reason = zombie_reason

    def __str__(self):
        return (f"Line {self.file_line}, Status {self.status} | " 
               f"[{self.link_name}] ({self.link_url}) | " 
               f"{self.zombie_reason}")
