APPROVED = 'approved'
UNVERIFIED = 'unverified'
NEEDS_APPROVAL = 'needs_approval'

ENTRY_STATUSES = (
    (APPROVED, 'Approved'),
    (UNVERIFIED, 'Unverified'),
    (NEEDS_APPROVAL, 'Needs Approval')
)

DEFAULT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_NO_MICROSECOND = '%Y-%m-%d %H:%M:%S'
TIMEDELTA_DEFAULT_FORMAT = '%H:%M:%S'
