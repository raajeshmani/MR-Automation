from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Driver Program Code
    print('Whose birthday do u want to remember: ')
    summary = input()
    print('Date format YYYY-MM-DD    eg: 2019-07-29 ')
    print('When is the birthday: ')
    date = input()

    event = {
      'summary': summary,
      'description': 'Grant a happy birthday wish by contacting at 12',
      'start': {
        'date': date,
        'timeZone': 'Asia/Calcutta',
      },
      'end': {
        'date': date,
        'timeZone': 'Asia/Calcutta',
      },
      'recurrence': [
        'RRULE:FREQ=YEARLY'
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'popup', 'minutes': 5},
        ],
      },
      'colorId': 11,
    }

    # print(service.calendarList().list().execute())
    
    print(summary +  ' on ' + date)

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    main()