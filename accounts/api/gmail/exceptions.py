from rest_framework.exceptions import APIException


class SendEmailException(APIException):
    status_code = 500

    def __init__(self, err):
        self.detail = 'There was an error sending the email. Error: {}'.format(err)
