# Pulling ubuntu image with a specific tag from the docker hub.
FROM ubuntu:18.04

ENV TONY_USERNAME=unkonwn
ENV TONY_PASSWORD=unknown
ENV TONY_PLAYLIST=https://open.spotify.com/playlist/unknown

# Adding maintainer name (Optional).
MAINTAINER beslst

# Updating the packages and installing cron and vim editor if you later want to edit your script from inside your container.
RUN apt-get update \  
    && apt-get install cron -y && apt-get install vim -y
    && apt install python3 -y \
    && apt install python3-pip -y \
    && apt install python3-venv

# Crontab file copied to cron.d directory.
COPY ./cronjob /etc/cron.d/container_cronjob
COPY ./requirements.txt /requirements.txt
COPY ./script.sh /script.sh
COPY ./tony.py /tony.py
COPY ./tony.sh /tony.sh

RUN virtualenv venv
RUN source venv/bin/activate
RUN pip install -r requirements.txt

# Giving executable permission to script file.
RUN chmod +x /script.sh
RUN chmod +x /tony.sh

# Running commands for the startup of a container.
CMD [“/bin/bash”, “-c”, “/script.sh && chmod 644 /etc/cron.d/container_cronjob && cron && tail -f /var/log/cron.log”]
