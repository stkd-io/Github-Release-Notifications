from curses import raw
from datetime import datetime, timedelta
import sys
import os
from os import environ
import pdpyras
from slack_sdk import WebClient
import time
from github import Github

##########################
#
#       Variables
#
##########################
#PAger Duty Variables
if environ.get('PD_API_KEY') is not None:
    #Service -> Custom Change Event Transformer key
    PD_API_KEY = os.environ['PD_API_KEY']
    #Setting Pager duty
    session = pdpyras.EventsAPISession(PD_API_KEY)



#Slack variables
if environ.get('SLACK_CHANNEL_NAME') is not None:
    SLACK_CHANNEL_NAME = os.environ['SLACK_CHANNEL_NAME']

if environ.get('SLACK_API') is not None:
    SLACK_API = os.environ['SLACK_API']

#Github variables
if environ.get('GITHUB_API') is not None:
    GITHUB_API = os.environ['GITHUB_API']    

if environ.get('GITHUB_REPO') is not None:
    GITHUB_REPO = os.environ['GITHUB_REPO'] 

if environ.get('CHECK_TIMER') is not None:
    CHECK_TIMER = os.environ['CHECK_TIMER']
else:
    CHECK_TIMER = 10

##########################
#
#       functions
#
##########################
def send_slack_message(api, channel_name, message):
    client = WebClient(api)
    response = client.chat_postMessage(
        channel=channel_name,
        text=message)

def sendAlert(message):
    sys.stdout.write(message)
    if environ.get('SLACK_API') is not None and environ.get('SLACK_CHANNEL_NAME') is not None:
        send_slack_message(SLACK_API, SLACK_CHANNEL_NAME, message)
    if environ.get('PD_API_KEY') is not None:
        session.trigger(message, "polkadot")
    time.sleep(3600)

##########################
#
#       Main
#
##########################
def main():
    G = Github(GITHUB_API) # Put your GitHub token here
    repo = G.get_repo(GITHUB_REPO) # 'paritytech/polkadot'
    releases = repo.get_releases()

    for release in releases:
        #Check if released in the last hour
        if (datetime.utcnow() - datetime.strptime(str(release.published_at), '%Y-%m-%d %H:%M:%S')) < timedelta(minutes=CHECK_TIMER):
            message = "[!] New Release: " + release.title 
            #sendAlert(message)
            quit()
        
    print("No New Release in the last " + str(CHECK_TIMER) + " minutes, lastest release was: " + releases[0].title)


if __name__ == "__main__":
    main()