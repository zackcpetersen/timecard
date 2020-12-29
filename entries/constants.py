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
