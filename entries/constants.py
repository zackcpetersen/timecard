APPROVED = 'approved'
NEEDS_APPROVAL = 'needs_approval'
FLAGGED = 'flagged'
ACTIVE = 'active'

ENTRY_STATUSES = (
    (APPROVED, 'Approved'),
    (NEEDS_APPROVAL, 'Needs Approval'),
    (FLAGGED, 'Flagged'),
    (ACTIVE, 'Active')
)

DEFAULT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_NO_MICROSECOND = '%Y-%m-%d %H:%M:%S'
TIMEDELTA_DEFAULT_FORMAT = '%H:%M:%S'
DATE_ONLY_FORMAT = '%Y-%m-%d'

ENTRY_ATTRS = ['id', 'user', 'start_time', 'end_time', 'start_pause', 'end_pause',
               'time_paused', 'time_paused_secs', 'time_worked', 'time_worked_secs', 'project',
               'project_name', 'loc_latitude', 'loc_longitude', 'loc_errors', 'status',
               'comments', 'created_at', 'updated_at', 'entry_images']

ENTRY_CSV_ATTRS = ['id', 'name', 'start_time', 'end_time',
                   'time_paused', 'time_worked',
                   'project_name', 'status', 'comments',
                   'created_at', 'updated_at']
