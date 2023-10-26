# Pulling ubuntu image with a specific tag from the docker hub.
FROM ubuntu:22.04

ENV TONY_USERNAME=
ENV TONY_PASSWORD=
ENV TONY_PLAYLIST=
ENV TONY_PUSHOVER_USERKEY=
ENV TONY_PUSHOVER_APPTOKEN=

# Adding maintainer name (Optional).
MAINTAINER beslst

# Updating the packages and installing cron and vim editor if you later want to edit your script from inside your container.
RUN apt-get update \  
    && apt-get install cron -y && apt-get install vim -y \
    && apt install python3 -y \
    && apt install python3-pip -y \
    && apt install ffmpeg -y

COPY ./requirements.txt /requirements.txt
COPY ./script.sh /script.sh
COPY ./tony.py /tony.py
COPY ./tony.sh /tony.sh

# Giving executable permission to script file.
RUN chmod +x /script.sh
RUN chmod +x /tony.sh
RUN mkdir /tony_cache
RUN pip3 install -r requirements.txt
RUN { cat; echo "0 * * * * /tony.sh > /proc/1/fd/1 2>/proc/1/fd/2"; } | crontab -


# Running commands for the startup of a container.
WORKDIR /
ENTRYPOINT ["/script.sh"]
