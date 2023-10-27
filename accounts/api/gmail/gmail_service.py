import os
import json
import base64
import logging
import tempfile

from django.conf import settings
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from accounts.api.gmail.exceptions import SendEmailException

# Define the Gmail API version and the OAuth2 scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Initialize the logger
logger = logging.getLogger(__name__)
# Configure logging
logging.basicConfig(level=logging.INFO)


class GmailAPI:
    def __init__(self):
        self.gmail_base_dir = os.path.join(
            os.environ.get('GMAIL_TOKEN_PATH', settings.BASE_DIR.parent), 'accounts/api/gmail')
        self.service = self.get_service()

    def get_service(self):
        creds = None
        token_path = os.path.join(self.gmail_base_dir, 'token.json')
        credentials_info = self.get_credentials()

        # Load existing credentials from JSON file
        if os.path.exists(token_path):
            with open(token_path, 'r') as token_file:
                creds = Credentials.from_authorized_user_info(json.load(token_file), SCOPES)

        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                with tempfile.NamedTemporaryFile('w+', delete=False) as temp:
                    json.dump(credentials_info, temp)
                    temp.seek(0)
                    flow = InstalledAppFlow.from_client_secrets_file(temp.name, SCOPES)
                os.unlink(temp.name)  # delete the temporary file
                creds = flow.run_local_server(port=0)

            # Save the credentials to a JSON file
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    @staticmethod
    def create_email(to_addr, from_addr, subject, content):
        message_raw = MIMEText(content)
        message_raw['to'] = to_addr
        message_raw['from'] = from_addr
        message_raw['subject'] = subject
        encoded = base64.urlsafe_b64encode(message_raw.as_bytes())
        return {'raw': encoded.decode()}

    def send_email(self, message):
        try:
            message = self.service.users().messages().send(userId='me', body=message).execute()
            logger.info(f"Message sent: ID {message['id']}")
            return message
        except HttpError as e:
            logger.error(f"A 'send_email' error occurred: {e}")
            raise SendEmailException(e)

    @staticmethod
    def get_credentials():
        return {
            "installed": {
                "client_id": settings.GMAIL_CLIENT_ID,
                "project_id": settings.GMAIL_PROJECT_ID,
                "auth_uri": settings.GMAIL_AUTH_URI,
                "token_uri": settings.GMAIL_TOKEN_URI,
                "auth_provider_x509_cert_url": settings.GMAIL_AUTH_PROVIDER,
                "client_secret": settings.GMAIL_CLIENT_SECRET,
                "redirect_uris": settings.GMAIL_REDIRECT_URIS,
            }
        }
