FROM python:3.4.8-alpine

LABEL Vikas Kumar "vikas@reachvikas.com"

# Let's start
RUN apk update && \
    apk upgrade

# Dependencies
ADD requirements.txt /tmp/
RUN apk update && \
    apk add --update --no-cache g++ gcc libxslt-dev && \
    pip install -r /tmp/requirements.txt

# Add Scripts
ADD scripts/gitlab_create_token.py /usr/sbin/gitlab_create_token.py

# Clean Up
RUN rm -rf /var/cache/apk/* /tmp/requirements.txt
