FROM python:alpine3.15

ENV TZ=""
ENV PD_API_KEY=""
ENV PD_SERVICE_NAME=""
ENV SLACK_API=""
ENV SLACK_CHANNEL_NAME=""
ENV GITHUB_API=""
ENV GITHUB_REPO=""
ENV CHECK_TIMER=""
ENV PYTHONUNBUFFERED=true


LABEL Maintainer="@frazzled_dazzle"
LABEL Company="stkd.io"

#Setup env
RUN apk update;\
    apk add py-pip;\
    apk add --no-cache tzdata

RUN pip install feedparser;\
    pip install datetime;\
    pip install time;\
    pip install sys;\
    pip install pathlib;\
    pip install pdpyras;\
    pip install os;\
    pip install slack_sdk;\
    pip install requests;\
    pip install PyGithub;\
    pip install ssl;\
    pip install certifi

#Patch the image
RUN apk upgrade

RUN mkdir /data;

COPY ./app/main.py /data/github_alert.py

CMD [ "python", "/data/github_alert.py"]

