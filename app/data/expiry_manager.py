import pytz
from datetime import datetime, timedelta


def update_cut_off(expiry_cut_off):
    utc_tz = pytz.timezone("UTC")

    utc_midnight = datetime.strptime(
        str(datetime.utcnow().date()) + " 00:00:00", "%Y-%m-%d %H:%M:%S"
    )

    expiry_cut_off = str(int(utc_tz.localize(utc_midnight - timedelta(1)).timestamp()))
    return expiry_cut_off
