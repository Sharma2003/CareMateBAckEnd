from datetime import datetime, timedelta


def _add_minutes_to_time(start_time, minutes: int):
    dt = datetime.combine(datetime.today(), start_time)
    dt = dt + timedelta(minutes=minutes)
    return dt.time()


