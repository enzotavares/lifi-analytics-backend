import pytz
from datetime import datetime, timedelta


def get_delta_count(utc_tz, utc_midnight, last_timestamp):
    count = 0
    while True:
        tmstp = int(utc_tz.localize(utc_midnight - timedelta(count)).timestamp())
        if tmstp > last_timestamp:
            count += 1
        else:
            break
    count += 4
    return count


def get_prep_cut_off(last_timestamp):
    utc_tz = pytz.timezone("UTC")

    utc_midnight = datetime.strptime(
        str(datetime.utcnow().date()) + " 00:00:00", "%Y-%m-%d %H:%M:%S"
    )

    delta_count = get_delta_count(utc_tz, utc_midnight, last_timestamp)

    expiry_cut_off = str(
        int(utc_tz.localize(utc_midnight - timedelta(delta_count)).timestamp())
    )
    return expiry_cut_off
