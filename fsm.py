from __future__ import print_function
from transitions.extensions import GraphMachine

import httplib2
import os
import sys
from googleapiclient.discovery import build

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

num = 3

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_credentials_insert():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-insert.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def check(num):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    # service = discovery.build('calendar', 'v3', http=credentials.authorize(Http()))

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    x = '接下來的' + num + '個活動：\n'

    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=num, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        # start = event['start'].get('dateTime', event['start'].get('date'))
        start = event['start'].get('dateTime')
        month = start[5:7]
        day = start[8:10]
        print(start, event['summary'])
        x += (month + '月'+ day + '日: ' + event['summary'] + "\n")
        print(x)
    
    return x

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def to_a(self, update):
        text = update.message.text
        return text == '加行程'

    def to_b(self, update):
        text = update.message.text
        return text == '查行程'

    def a_to_c(self, update):
        text = update.message.text
        return text == 'dinner'

    def b_to_d(self, update):
        text = update.message.text
        global num
        num = text
        return num.isdigit()
    
    def on_enter_state1(self, update):
        update.message.reply_text("state A here")
        update.message.reply_photo(open('test.gif', 'rb'))
        # self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("想查接下來幾個活動？")
        # update.message.reply_text(check())
        # check()
        # self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        update.message.reply_text("state C here")
        credentials = get_credentials_insert()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        # GMT_OFF = '08:00'
        EVENT = {
            'summary':'哭QQ',
            'start': {
                'date': '2018-01-03'
            },
            'end': {
                'date': '2018-01-03'
            },
            'attendees': [
                {'email': 'hoiian96@gmail.com'}
            ]
        }

        e = service.events().insert(calendarId='primary', body=EVENT).execute()

        if(e):
            update.message.reply_text("updated!")

    def on_enter_state4(self, update):
        global num
        update.message.reply_text("state D here")
        if (check(num)):
            update.message.reply_text(check(num))
        else:
            update.message.reply_text("sth wrong.")
        
        # update.message.reply_text(num)