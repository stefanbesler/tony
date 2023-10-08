#!/usr/bin/env bash

echo "export TONY_USERNAME=\"$TONY_USERNAME\"" >> /env.sh
echo "export TONY_PASSWORD=\"$TONY_PASSWORD\"" >> /env.sh
echo "export TONY_PLAYLIST=\"$TONY_PLAYLIST\"" >> /env.sh

touch /var/log/cron.log
/tony.sh

cron
tail -f /var/log/cron.log

