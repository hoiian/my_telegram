
from __future__ import print_function
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
CLIENT_SECRET_FILE = 'client_secret_165964366033-k8fv1glia0lfsqn120k6h32u26cofcba.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


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

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    # service = discovery.build('calendar', 'v3', http=credentials.authorize(Http()))

    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # eventsResult = service.events().list(
    #     calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
    #     orderBy='startTime').execute()
    # events = eventsResult.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

    # print("hihihi")

    GMT_OFF = '08:00'
    EVENT = {
        'summary':'dinner with yy',
        'start' : {'dateTime': '2017-12-31T19:00:00%s' % GMT_OFF},
        'end' : {'dateTime': '2017-12-31T20:00:00%s' % GMT_OFF},
        'attendees': [
            {'email': 'hoiian96@gmail.com'}
        ]
    }

    e = service.events().insert(calendarId='primary', body=EVENT).execute()
    # print ('Event created: %s' % (e.get('htmlLink'))

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/google-apps/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    # e = {
    # 'summary': 'Google I/O 2015',
    # 'location': '800 Howard St., San Francisco, CA 94103',
    # 'description': 'A chance to hear more about Google\'s developer products.',
    # 'start': {
    #     'dateTime': '2017-12-31T09:00:00-07:00',
    #     'timeZone': 'America/Los_Angeles',
    # },
    # 'end': {
    #     'dateTime': '2018-01-01T17:00:00-07:00',
    #     'timeZone': 'America/Los_Angeles',
    # },
    # 'recurrence': [
    #     'RRULE:FREQ=DAILY;COUNT=2'
    # ],
    # 'attendees': [
    #     {'email': 'hoiian96@gmail.com'},
    #     # {'email': 'sbrin@example.com'},
    # ],
    # 'reminders': {
    #     'useDefault': False,
    #     'overrides': [
    #     {'method': 'email', 'minutes': 24 * 60},
    #     {'method': 'popup', 'minutes': 10},
    #     ],
    # },
    # }

    # ee = service.events().insert(calendarId='primary', body=e).execute()
    # # print 'Event created: %s' % (e.get('htmlLink'))
    # print("hihi")
if __name__ == '__main__':
    main()