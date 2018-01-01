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
        # eventId = event.get('id')
        print(start, event['summary'])
        x += (month + '月'+ day + '日: ' + event['summary'] + "\n")
        print(x)
    
    return x

def delete(name):
    credentials = get_credentials_insert()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        if(name == event['summary']):
            eventId = event.get('id')
            d = service.events().delete(calendarId='primary', eventId='eventId').execute()
            if(d):
                return True

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def welcome(self, update):
        text = update.message.text
        # if (text == 'hi' or text == '/start' or text == '/help' or text == '嗨' or text == '?' or text == 'hihi'):
        return True


    def to_a(self, update):
        text = update.message.text
        return '加' in text or 'add' in text

    def to_b(self, update):
        text = update.message.text
        return '查' in text or 'check' in text

    def to_f(self, update):
        text = update.message.text
        return text == 'delete'

    def a_to_c(self, update):
        text = update.message.text
        global the_date
        the_date = text
        return True
        # datetime.strptime(the_date, "%Y-%m-%d")
        # else:
        #     update.message.reply_text("請按照以下格式：2018-01-01")

    def c_to_e(self, update):
        text = update.message.text
        global title
        title = text
        return True

    def b_to_d(self, update):
        text = update.message.text
        global num
        num = text
        return num.isdigit()
    
    def on_enter_state1(self, update):
        update.message.reply_text("什麼時候呢？(mm-dd)")
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
        global the_date
        update.message.reply_text(the_date + "你要幹嘛呢？")
        # update.message.reply_text(the_date)

    def on_enter_state5(self, update):
        global title
        # update.message.reply_text("state5 here")

        credentials = get_credentials_insert()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        # GMT_OFF = '08:00'
        EVENT = {
            'summary':title,
            'start': {
                'dateTime': '2018-' + the_date + 'T09:00:00+08:00'
            },
            'end': {
                'dateTime': '2018-' + the_date + 'T10:00:00+08:00'
            }
        }

        e = service.events().insert(calendarId='primary', body=EVENT).execute()

        if(e):
            update.message.reply_text("已加入!")


    def on_enter_state4(self, update):
        global num
        # update.message.reply_text("state D here")
        if (check(num)):
            update.message.reply_text(check(num))
        else:
            update.message.reply_text("sth wrong.")

    # def on_enter_state6(self, update):
    #     update.message.reply_text("state F here")
    #     delete('睡覺')

    def on_enter_state0(self, update):
        update.message.reply_text("你要「加行程」還是「查行程」？")