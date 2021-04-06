from __future__ import print_function
import base64
import pickle
import os.path

from apiclient import errors
from django.conf import settings
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


class GmailAPI:
    def send_email(self, message):
        service = self.get_service()
        try:
            message = service.users().messages().send(userId='me', body=message).execute()
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as e:
            print('An error occurred: {}'.format(e))

    @staticmethod
    def create_email(to_addr, from_addr, subject, content):
        message_raw = MIMEText(content)
        message_raw['to'] = to_addr
        message_raw['from'] = from_addr
        message_raw['subject'] = subject
        encoded = base64.urlsafe_b64encode(message_raw.as_bytes())
        return {'raw': encoded.decode()}

    @staticmethod
    def get_service():
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        pickle_path = os.path.join(settings.BASE_DIR.parent, 'accounts/api/gmail/token.pickle')
        if os.path.exists(pickle_path):
            with open(pickle_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(settings.BASE_DIR.parent, 'accounts/api/gmail/credentials.json'),
                    SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(pickle_path, 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)
        return service
