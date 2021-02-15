from rest_framework.exceptions import APIException


class DeletionException(APIException):
    status_code = 409

    def __init__(self, exception):
        self.detail = str(exception)
