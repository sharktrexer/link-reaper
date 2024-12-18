# Dockerfil for link-reaper
FROM python:3.9.6

RUN pip install the-link-reaper

# Command to run link-reaper on your file without overwriting
# Customize as you desire
CMD ["link-reaper", "reap", "yourfile.md", "-m"]

# Now you can use the following commands to run:
# docker build -t link-reaper .
# docker run link-reaper