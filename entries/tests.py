import datetime
import pytz

from django.test import Client, TestCase

from freezegun import freeze_time

from accounts.models import User
from entries import constants as entry_constants
from entries.models import Entry


class EntryTests(TestCase):
    def setUp(self):
        # Create User
        self.user1 = User.objects.create(first_name='Tester',
                                         last_name='Testerson',
                                         email='testworkshard@gmail.com')
        self.start_time_endpoint = '/api/start-time/'
        self.end_time_endpoint = '/api/end-time/'
        self.start_pause_endpoint = '/api/start-pause/'
        self.end_pause_endpoint = '/api/end-pause/'
        self.c = Client()
        # TODO consider testing multiple users at the same time

    def test_entry_endpoints(self):
        """
        Test Entry endpoints
        """
        with freeze_time("2020-11-7 9:00:00"):
            request = self.time_request(self.user1, self.start_time_endpoint)
            exp_start_formatted, exp_start_raw = self.get_datetime()
            self.assertEqual(request.json()['start_time'], exp_start_formatted)

        with freeze_time("2020-11-7 12:00:00"):
            request = self.time_request(self.user1, self.start_pause_endpoint)
            exp_pause_formatted, exp_pause_raw = self.get_datetime()
            self.assertEqual(request.json()['pause_time'], exp_pause_formatted)
            pause_time = datetime.datetime.now(tz=pytz.UTC)

        with freeze_time("2020-11-7 13:00:00"):
            request = self.time_request(self.user1, self.end_pause_endpoint)
            expected_time_paused = datetime.datetime.now(tz=pytz.UTC) - pause_time
            actual_pause_time = self.format_timedelta(request.json()['time_paused'])
            self.assertEqual(expected_time_paused, actual_pause_time)

        with freeze_time("2020-11-7 17:00:00"):
            request = self.time_request(self.user1, self.end_time_endpoint)
            exp_end_formatted, exp_end_raw = self.get_datetime()
            self.assertEqual(request.json()['end_time'], exp_end_formatted)

            expected_time_worked = exp_end_raw - expected_time_paused - exp_start_raw
            actual_worked_time = self.format_timedelta(request.json()['time_worked'])
            self.assertEqual(actual_worked_time, expected_time_worked)

    def test_entry_edge(self):
        """
        Test entry edge cases
        """
        with freeze_time("2020-11-7 9:00:00"):
            start_time = datetime.datetime.now(tz=pytz.UTC)
            entry = Entry.objects.create(user=self.user1, start_time=start_time)
        with freeze_time("2020-11-7 12:00:00"):
            pause_time = datetime.datetime.now(tz=pytz.UTC)
            entry.pause_time = pause_time
        with freeze_time("2020-11-7 17:00:00"):
            end_time = datetime.datetime.now(tz=pytz.UTC)
            entry.end_time = end_time
            entry.save()

            entry.calculate_paused()
            entry.calculated_worked()

        expected_time_worked = pause_time - start_time
        self.assertEqual(entry.time_worked, expected_time_worked)

    def time_request(self, user, endpoint):
        self.c.force_login(user=user)
        data = {'user': user.pk}
        return self.c.post(endpoint, data=data)

    @staticmethod
    def format_timedelta(str_time):
        time = datetime.datetime.strptime(str_time, entry_constants.TIMEDELTA_DEFAULT_FORMAT)
        return datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

    @staticmethod
    def get_datetime():
        now = datetime.datetime.now(tz=pytz.UTC)
        return now.strftime(entry_constants.DEFAULT_DATETIME_FORMAT), now
