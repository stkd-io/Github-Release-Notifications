from curses import raw
from datetime import datetime, timedelta
import sys
import os
from os import environ
import pdpyras
from slack_sdk import WebClient
import time
from github import Github
import ssl
import certifi

##########################
#
#       Variables
#
##########################
#Pager Duty Variables
if environ.get('PD_API_KEY') is not None:
    #Service -> Custom Change Event Transformer key
    PD_API_KEY = os.environ['PD_API_KEY']
else:
    sys.stdout.write("[!] No Pager Duty API Key detected\n")


if environ.get('PD_SERVICE_NAME') is not None:
    PD_SERVICE_NAME = os.environ['PD_SERVICE_NAME']
else:
    sys.stdout.write("[!] No Pager Duty Service Name detected\n")

#Slack variables
if environ.get('SLACK_CHANNEL_NAME') is not None:
    SLACK_CHANNEL_NAME = os.environ['SLACK_CHANNEL_NAME']
else:
    sys.stdout.write("[!] No Slack channel name set\n")

if environ.get('SLACK_API') is not None:
    SLACK_API = os.environ['SLACK_API']
else:
    sys.stdout.write("[!] No Slack API Key detected\n")

#Github variables
if environ.get('GITHUB_API') is not None:
    GITHUB_API = os.environ['GITHUB_API']    
else:
    sys.stdout.write("[!] No GitHub API Key detected\n")

if environ.get('GITHUB_REPO') is not None:
    GITHUB_REPO = os.environ['GITHUB_REPO'] 
else:
    sys.stdout.write("[!] No GitHub Repo detected\n")

if environ.get('CHECK_TIMER') is not None:
    CHECK_TIMER = os.environ['CHECK_TIMER']
else:
    sys.stdout.write("[!] No CHECK_TIMER set defaulting to 10 minutes\n")
    CHECK_TIMER = 10

##########################
#
#       functions
#
##########################
def send_slack_message(api, channel_name, message):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    client = WebClient(api, ssl=ssl_context)
    response = client.chat_postMessage(
        channel=channel_name,
        text=message)

def sendAlert(message):
    sys.stdout.write(message)
    if environ.get('SLACK_API') is not None and environ.get('SLACK_CHANNEL_NAME') is not None:
        send_slack_message(SLACK_API, SLACK_CHANNEL_NAME, message)
    if environ.get('PD_API_KEY') is not None and environ.get('PD_SERVICE_NAME') is not None:
        #Setting Pager duty
        session = pdpyras.EventsAPISession(PD_API_KEY)
        session.trigger(message, PD_SERVICE_NAME)

##########################
#
#       Main
#
##########################
def main():
    sentPage = False

    G = Github(GITHUB_API)
    repo = G.get_repo(GITHUB_REPO)
    releases = repo.get_releases()

    for release in releases:
        #Check if released in the last CHECK_TIMER minutes
        if (datetime.utcnow() - datetime.strptime(str(release.published_at), '%Y-%m-%d %H:%M:%S')) < timedelta(minutes=int(CHECK_TIMER)):
            message = "[!] New Release for " + str(GITHUB_REPO) + ": " + str(release.title) + "\n" 
            sendAlert(message)
            sentPage = True

    if sentPage == False:
        print("No New Release for " + GITHUB_REPO + " in the last " + str(CHECK_TIMER) + " minutes, lastest release was: " + releases[0].title)


if __name__ == "__main__":
    main()