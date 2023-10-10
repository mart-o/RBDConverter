import datetime


def time_to_str(time: datetime.datetime) -> str:
    return '{0:02d}:{1:02d}:{2:02d},{3:03d}'.format(time.hour, time.minute, time.second, time.microsecond // 1000)


def time_to_str_without_millis(time: datetime.datetime) -> str:
    return '{0:02d}:{1:02d}:{2:02d}'.format(time.hour, time.minute, time.second)


def datetime_to_str(time: datetime.datetime) -> str:
    return '{0:02d}.{1:02d}.{2:04d} {3}'.format(time.day, time.month, time.year, time_to_str_without_millis(time))

