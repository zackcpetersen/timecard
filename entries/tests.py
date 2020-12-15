import datetime
import pytz

from django.test import Client, TestCase

from freezegun import freeze_time

from accounts.models import User
from entries import constants as entry_constants
from entries.models import Entry
from projects.models import Project


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
        self.csv_download_endpoint = '/api/entry-download/'
        self.c = Client()
        # TODO test multiple users at the same time

    def test_entry_endpoints(self):
        """
        Test Entry endpoints
        """
        with freeze_time("2020-11-7 9:00:00"):
            request = self.time_request(self.user1, self.start_time_endpoint)
            exp_start_formatted, exp_start_raw = self.get_test_datetime()
            self.assertEqual(request.json()['start_time'], exp_start_formatted)

        with freeze_time("2020-11-7 12:00:00"):
            request = self.time_request(self.user1, self.start_pause_endpoint)
            exp_pause_formatted, exp_pause_raw = self.get_test_datetime()
            self.assertEqual(request.json()['start_pause'], exp_pause_formatted)
            _, start_pause = self.get_test_datetime()

        with freeze_time("2020-11-7 13:00:00"):
            request = self.time_request(self.user1, self.end_pause_endpoint)
            expected_time_paused = datetime.datetime.now(tz=pytz.UTC) - start_pause
            expected_time_paused_secs = expected_time_paused.total_seconds()
            actual_pause_time = request.json()['time_paused']
            self.assertEqual(expected_time_paused_secs, actual_pause_time)

        with freeze_time("2020-11-7 17:00:00"):
            request = self.time_request(self.user1, self.end_time_endpoint)
            exp_end_formatted, exp_end_raw = self.get_test_datetime()
            self.assertEqual(request.json()['end_time'], exp_end_formatted)

            expected_time_worked = exp_end_raw - expected_time_paused - exp_start_raw
            expected_time_worked_secs = expected_time_worked.total_seconds()
            actual_worked_time_secs = request.json()['time_worked']
            self.assertEqual(actual_worked_time_secs, expected_time_worked_secs)

    def test_entry_edge(self):
        """
        Test entry edge cases
        """
        with freeze_time("2020-11-7 9:00:00"):
            _, start_time = self.get_test_datetime()
            entry = Entry.objects.create(user=self.user1, start_time=start_time)
        with freeze_time("2020-11-7 12:00:00"):
            _, start_pause = self.get_test_datetime()
            entry.start_pause = start_pause
        with freeze_time("2020-11-7 17:00:00"):
            _, end_time = self.get_test_datetime()
            entry.end_time = end_time
            entry.save()

        entry.calculate_worked()

        expected_time_worked = start_pause - start_time
        self.assertEqual(entry.time_worked, expected_time_worked)

    def test_entry_csv_download(self):
        project1 = Project.objects.create(name='Airport Job')
        entry_data = [
            {
                'start_time': '2020-11-10 12:00:00',
                'end_time': '2020-11-10 17:00:00',
                'start_pause': '2020-11-10 12:00:00',
                'end_pause': '2020-11-10 13:00:00',
                'project': project1
            },
            {
                'start_time': '2020-11-11 12:00:00',
                'end_time': '2020-11-11 17:00:00',
                'start_pause': '2020-11-11 12:00:00',
                'end_pause': '2020-11-11 13:00:00',
                'project': project1
            },{
                'start_time': '2020-11-12 12:00:00',
                'end_time': '2020-11-12 17:00:00',
                'start_pause': '2020-11-12 12:00:00',
                'end_pause': '2020-11-12 13:00:00',
                'project': project1
            },{
                'start_time': '2020-11-13 12:00:00',
                'end_time': '2020-11-13 17:00:00',
                'start_pause': '2020-11-13 12:00:00',
                'end_pause': '2020-11-13 13:00:00',
                'project': project1
            },{
                'start_time': '2020-11-15 12:00:00',
                'end_time': '2020-11-15 17:00:00',
                'start_pause': '2020-11-15 12:00:00',
                'end_pause': '2020-11-15 13:00:00',
                'project': project1
            },
        ]

        for entry in entry_data:
            Entry.objects.create(user=self.user1,
                                 start_time=self.add_tz(entry['start_time']),
                                 end_time=self.add_tz(entry['end_time']),
                                 start_pause=self.add_tz(entry['start_pause']),
                                 end_pause=self.add_tz(entry['end_pause']),
                                 project=entry['project'])

        data = {
            'users': [self.user1.pk],
            'start-date': '2020-11-10',
            'end-date': '2020-11-15'
        }

        request = self.c.post(self.csv_download_endpoint, data=data)
        print(request)

    def time_request(self, user, endpoint):
        self.c.force_login(user=user)
        data = {'user': user.pk}
        return self.c.post(endpoint, data=data)

    @staticmethod
    def add_tz(str_datetime):
        return pytz.utc.localize(datetime.datetime.strptime(str_datetime, entry_constants.DATETIME_NO_MICROSECOND))

    @staticmethod
    def format_timedelta(str_time):
        time = datetime.datetime.strptime(str_time, entry_constants.TIMEDELTA_DEFAULT_FORMAT)
        return datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

    @staticmethod
    def get_test_datetime():
        now = datetime.datetime.now(tz=pytz.UTC)
        return now.strftime(entry_constants.DEFAULT_DATETIME_FORMAT), now
