import datetime
import pytz

from django.test import Client, TestCase
from freezegun import freeze_time

from accounts.models import User
from entries import constants as entry_constants
from entries.models import Entry
from projects import constants as proj_constants
from projects.models import Project, ProjectType


class EntryTests(TestCase):
    def setUp(self):
        # Create User
        self.user1 = User.objects.create(first_name='Tester',
                                         last_name='Testerson',
                                         email='testworkshard@gmail.com')
        self.admin_user = User.objects.create(
            first_name='Admin',
            last_name='User',
            email="admin@user.com",
            is_admin=True,
            is_staff=True,
        )
        self.proj_type_test = ProjectType.objects.create(name="test")
        self.project = Project.objects.create(name="project1", status=proj_constants.STATUS_ACTIVE, type=self.proj_type_test)
        self.start_time_endpoint = '/api/start-time/'
        self.update_entry_endpoint = '/api/update-entry/'
        self.end_time_endpoint = '/api/end-time/'
        self.start_pause_endpoint = '/api/start-pause/'
        self.end_pause_endpoint = '/api/end-pause/'
        self.csv_download_endpoint = '/api/entry-download/'
        self.entry_filter_endpoint = '/api/filter-entries/'
        self.entry_status_endpoint = '/api/entry-status/'
        self.c = Client()

        self.default_entry_data = [
            {
                'start_time': '2020-11-10 12:00:00',
                'end_time': '2020-11-10 17:00:00',
                'start_pause': '2020-11-10 12:00:00',
                'end_pause': '2020-11-10 13:00:00',
                'project': self.project,
            },
            {
                'start_time': '2020-11-11 12:00:00',
                'end_time': '2020-11-11 17:00:00',
                'start_pause': '2020-11-11 12:00:00',
                'end_pause': '2020-11-11 13:00:00',
                'project': self.project,
            },
            {
                'start_time': '2020-11-12 12:00:00',
                'end_time': '2020-11-12 17:00:00',
                'start_pause': '2020-11-12 12:00:00',
                'end_pause': '2020-11-12 13:00:00',
                'project': self.project,
            },
            {
                'start_time': '2020-11-13 12:00:00',
                'end_time': '2020-11-13 17:00:00',
                'start_pause': '2020-11-13 12:00:00',
                'end_pause': '2020-11-13 13:00:00',
                'project': self.project,
            },
            {
                'start_time': '2020-11-15 12:00:00',
                'end_time': '2020-11-15 17:00:00',
                'start_pause': '2020-11-15 12:00:00',
                'end_pause': '2020-11-15 13:00:00',
                'project': self.project,
            },
        ]

    def test_entry_endpoints(self):
        """
        Test Entry endpoints
        """
        self.c.force_login(user=self.user1)
        data = {'user': self.user1.pk}
        with freeze_time("2020-11-7 9:00:00"):
            request = self.c.post(self.start_time_endpoint, data=data)
            exp_start_formatted, exp_start_raw = self.get_test_datetime()
            self.assertEqual(request.json()['start_time'], exp_start_formatted)

        # add project to entry
        patch_url = self.update_entry_endpoint + str(request.json()['id']) + "/"
        request = self.c.patch(patch_url, data={'project': self.project.pk}, content_type='application/json')
        self.assertEqual(request.json()['project'], self.project.pk)

        with freeze_time("2020-11-7 12:00:00"):
            request = self.c.post(self.start_pause_endpoint, data=data)
            exp_pause_formatted, exp_pause_raw = self.get_test_datetime()
            self.assertEqual(request.json()['start_pause'], exp_pause_formatted)
            _, start_pause = self.get_test_datetime()

        with freeze_time("2020-11-7 13:00:00"):
            request = self.c.post(self.end_pause_endpoint, data=data)
            expected_time_paused_1 = datetime.datetime.now(tz=pytz.UTC) - start_pause
            resp_pause_time = request.json()['time_paused']

            # convert string into a timedelta obj
            actual_pause_time = self.string_to_timedelta(resp_pause_time)
            self.assertEqual(expected_time_paused_1, actual_pause_time)

        with freeze_time("2020-11-7 14:00:00"):
            request = self.c.post(self.start_pause_endpoint, data=data)
            exp_pause_formatted, exp_pause_raw = self.get_test_datetime()
            self.assertEqual(request.json()['start_pause'], exp_pause_formatted)
            _, start_pause = self.get_test_datetime()

        with freeze_time("2020-11-7 14:30:00"):
            request = self.c.post(self.end_pause_endpoint, data=data)
            expected_time_paused_2 = datetime.datetime.now(tz=pytz.UTC) - start_pause
            expected_time_paused_secs_total = expected_time_paused_2 + expected_time_paused_1
            resp_pause_time = request.json()['time_paused']

            actual_pause_time = self.string_to_timedelta(resp_pause_time)
            self.assertEqual(expected_time_paused_secs_total, actual_pause_time)

        with freeze_time("2020-11-7 17:00:00"):
            request = self.c.post(self.end_time_endpoint, data=data)
            exp_end_formatted, exp_end_raw = self.get_test_datetime()
            self.assertEqual(request.json()['end_time'], exp_end_formatted)

            total_pause_time = expected_time_paused_1 + expected_time_paused_2
            expected_time_worked = exp_end_raw - total_pause_time - exp_start_raw
            resp_time_worked = request.json()['time_worked']
            actual_time_worked = self.string_to_timedelta(resp_time_worked)
            self.assertEqual(actual_time_worked, expected_time_worked)

    def test_entry_edge(self):
        """
        Test entry when start_pause has a value but end_pause is None
        """
        with freeze_time("2020-11-7 9:00:00"):
            _, start_time = self.get_test_datetime()
            entry = Entry.objects.create(user=self.user1, start_time=start_time, project=self.project)
        with freeze_time("2020-11-7 12:00:00"):
            _, start_pause = self.get_test_datetime()
            entry.start_pause = start_pause
        with freeze_time("2020-11-7 17:00:00"):
            _, end_time = self.get_test_datetime()
            entry.end_time = end_time
            entry.save()

        expected_time_worked = start_pause - start_time
        self.assertEqual(entry.time_worked, expected_time_worked)

    def test_entry_csv_download(self):
        self.maxDiff = None

        entries = self.create_entries("2020-11-15 9:00:00", self.default_entry_data)
        entry_pks = [entry.pk for entry in entries]

        data = {
            'start_date': '2020-11-10',
            'end_date': '2020-11-15',
            'entries': entry_pks,
        }
        self.c.force_login(user=self.admin_user)
        response = self.c.post(self.csv_download_endpoint, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

        expected_content = """Entries for 2020-11-10 - 2020-11-15\r\nUser,Hours Worked\r\nTester Testerson,00:00:00\r\n""\r\nProject,Hours Worked\r\nproject1,00:00:00\r\n""\r\nid,name,start_time,end_time,time_paused,time_worked,project_name,status,comments,created_at,updated_at\r\n1,Tester Testerson,2020-11-10 05:00:00,2020-11-10 10:00:00,00:00:00,00:00:00,project1,needs_approval,,2020-11-15 02:00:00,2020-11-15 02:00:00\r\n2,Tester Testerson,2020-11-11 05:00:00,2020-11-11 10:00:00,00:00:00,00:00:00,project1,needs_approval,,2020-11-15 02:00:00,2020-11-15 02:00:00\r\n3,Tester Testerson,2020-11-12 05:00:00,2020-11-12 10:00:00,00:00:00,00:00:00,project1,needs_approval,,2020-11-15 02:00:00,2020-11-15 02:00:00\r\n4,Tester Testerson,2020-11-13 05:00:00,2020-11-13 10:00:00,00:00:00,00:00:00,project1,needs_approval,,2020-11-15 02:00:00,2020-11-15 02:00:00\r\n5,Tester Testerson,2020-11-15 05:00:00,2020-11-15 10:00:00,00:00:00,00:00:00,project1,needs_approval,,2020-11-15 02:00:00,2020-11-15 02:00:00\r\n"""  # noqa: E501
        expected_content_bytes = expected_content.encode('utf-8')
        self.assertEqual(expected_content_bytes, response.content)

    def test_entry_status_view(self):
        entries = self.create_entries("2020-11-15 9:00:00", self.default_entry_data)
        data = {"entries": [entry.pk for entry in entries], "status": entry_constants.APPROVED}
        self.c.force_login(user=self.admin_user)
        response = self.c.post(self.entry_status_endpoint, data=data)
        self.assertEqual(response.status_code, 200)
        entries = response.json()
        self.assertEqual(len(entries), 5)

        for entry in entries:
            self.assertEqual(entry['status'], entry_constants.APPROVED)

        # only update entries that are not active
        entry_data = [
            {
                'start_time': '2020-11-10 12:00:00',
                'project': self.project,
            },
            {
                'start_time': '2020-11-11 12:00:00',
                'project': self.project,
            },
        ]
        to_be_created = []
        for data in entry_data:
            to_be_created.append(Entry(
                user=self.user1,
                start_time=self.add_tz(data['start_time']),
                project=data['project'],
            ))
        entries = Entry.objects.bulk_create(to_be_created)
        data = {"entries": [entry.pk for entry in entries], "status": entry_constants.APPROVED}
        response = self.c.post(self.entry_status_endpoint, data=data)
        self.assertEqual(response.status_code, 400)

        # Missing data should fail
        response = self.c.post(self.entry_status_endpoint, data={})
        self.assertEqual(response.status_code, 400)

        # Non-admin user tries to update statuses should fail
        self.c.force_login(user=self.user1)
        response = self.c.post(self.entry_status_endpoint, data=data)
        self.assertEqual(response.status_code, 403)

    def test_entry_filter_view(self):
        # Test admin can pull all entries
        _ = self.create_entries("2023-9-8 9:00:00", self.default_entry_data)
        data = {"start_date": "2020-11-9", "end_date": "2020-11-15", "timezone": "America/Denver"}
        self.c.force_login(user=self.admin_user)
        response = self.c.post(self.entry_filter_endpoint, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

        # Test user2 cannot see entries from user1
        user2 = User.objects.create(first_name='Tester2', last_name="Testerson2", email="some_email@aol.net")
        self.c.force_login(user=user2)
        response = self.c.post(self.entry_filter_endpoint, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

        # Test missing required fields
        response = self.c.post(self.entry_filter_endpoint, data={})
        self.assertEqual(response.status_code, 400)

        # Test invalid timezone
        response = self.c.post(self.entry_filter_endpoint, data={"timezone": "invalid"})
        self.assertEqual(response.status_code, 400)

    def create_entries(self, time_freeze, entry_data, status=entry_constants.NEEDS_APPROVAL):
        entry_list = []
        for entry in entry_data:
            entry_list.append(
                Entry(
                    user=self.user1,
                    start_time=self.add_tz(entry['start_time']),
                    end_time=self.add_tz(entry['end_time']),
                    start_pause=self.add_tz(entry['start_pause']),
                    end_pause=self.add_tz(entry['end_pause']),
                    project=entry['project'],
                    status=status,
                )
            )

        with freeze_time(time_freeze):
            entries = Entry.objects.bulk_create(entry_list)
        return entries

    @staticmethod
    def string_to_timedelta(str_time):
        hours, minutes, seconds = map(int, str_time.split(':'))
        return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def add_tz(str_datetime):
        return pytz.utc.localize(datetime.datetime.strptime(str_datetime, entry_constants.DATETIME_NO_MICROSECOND))

    @staticmethod
    def get_test_datetime():
        now = datetime.datetime.now(tz=pytz.UTC)
        return now.strftime(entry_constants.DEFAULT_DATETIME_FORMAT), now
