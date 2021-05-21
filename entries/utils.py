def append_zero(duration):
    if duration < 10:
        duration = '0{}'.format(duration)
    return duration


def format_timedelta(time_delta):
    seconds = int(time_delta.total_seconds())
    hours = append_zero(seconds // 3600)
    minutes = append_zero((seconds % 3600) // 60)
    seconds = append_zero(seconds % 60)
    return '{}:{}:{}'.format(hours, minutes, seconds)
