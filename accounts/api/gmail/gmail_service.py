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

from accounts import constants as account_constants

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


class GmailAPI:
    def __init__(self, user, password, subject):
        self.user = user
        self.password = password
        self.subject = subject

    def send_pass_details(self):
        email_message = self.create_pass_message()
        service = self.get_service()
        try:
            message = service.users().messages().send(userId='me', body=email_message).execute()
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as e:
            print('An error occurred: {}'.format(e))

    def create_pass_message(self):
        message = MIMEText(account_constants.ACCOUNT_CREATION_MESSAGE.format(
            self.user.first_name, self.user.last_name, self.user.email, self.password))
        message['to'] = self.user.email
        # TODO will need to update message['from'] - possibly model attr?
        message['from'] = account_constants.FROM_ACCOUNT
        message['subject'] = self.subject
        # message['subject'] = account_constants.SUBJECT.format(self.user.first_name, self.user.last_name)
        encoded = base64.urlsafe_b64encode(message.as_bytes())
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
