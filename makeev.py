#!/usr/bin/env python3

import os
#import requests
import httplib2
import argparse
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage
from datetime import datetime

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar test script'

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

def get_credentials():
    ''''''
    this_dir = os.path.dirname(os.path.abspath(__file__))
    credential_dir = os.path.join(this_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')
    
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """"""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    event = {
        'summary': 'test event',
        'description': 'made via API',
        'start': {
            'dateTime': '2018-03-12T12:10:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2018-03-12T12:40:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: {}'.format(event.get('htmlLink')))

if __name__ == '__main__':
    main()

