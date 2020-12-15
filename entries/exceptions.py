from rest_framework.exceptions import APIException


class FieldRequiredException(APIException):
    status_code = 409

    def __init__(self, field):
        self.detail = '{} are required to continue'.format(field)


class NullRequiredException(APIException):
    status_code = 409

    def __init__(self, field):
        self.detail = '{} must be null to continue'.format(field)


class ProjectRequiredException(APIException):
    status_code = 409

    def __init__(self):
        self.detail = 'Project is required to end entry!'
