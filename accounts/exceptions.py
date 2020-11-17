from rest_framework.exceptions import APIException


class InvalidDateRangeException(APIException):
    status_code = 409

    def __init__(self, start, end):
        self.detail = 'Start date cannot be later than end date'
