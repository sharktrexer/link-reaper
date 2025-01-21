# Dockerfil for link-reaper
FROM python:3.13.1

# Where the markdown file is located. Default is current location of this file
WORKDIR ./

RUN pip install the-link-reaper

# Command to run link-reaper on your file without overwriting or file creation
# Customize as you desire
RUN link-reaper reap yourfile.md -is -m -dl

# Now you can use the following commands to run:
# docker build -t link-reaper .
# docker run link-reaper
