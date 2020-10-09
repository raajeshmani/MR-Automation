import datetime, pickle, os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
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
            creds = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/calendar']).run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    # Driver Program Code
    # cerner_2^5_2020
    print('Whose birthday do u want to remember: ')
    summary = input()
    print('Date format YYYY-MM-DD    eg: 2019-07-29 ')
    print('When is the birthday: ')
    date = input()
    event = { 'summary': summary, 'description': 'Call them at 12 and do your thing', 'start': { 'date': date, 'timeZone': 'Asia/Calcutta', }, 'end': { 'date': date, 'timeZone': 'Asia/Calcutta', }, 'recurrence': [ 'RRULE:FREQ=YEARLY' ], 'reminders': { 'useDefault': False, 'overrides': [ {'method': 'popup', 'minutes': 5}, ], }, 'colorId': 11, }
    print(summary +  ' on ' + date)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
if __name__ == '__main__':
    main()