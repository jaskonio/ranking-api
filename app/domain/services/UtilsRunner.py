import re
from datetime import timedelta


def strtobool(val):
    """Convert a string representation of truth to true or false.
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = str(val).lower()

    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %s",str(val))

def convert_string_to_timedelta(input_str, format_type):
    """_summary_

    Args:
        input_str (_type_): "03m 34s / km"
        format_type (_type_): "mm:ss / km"

    Returns:
        _type_: 0:03:34
    """
    time_str = re.sub(r'[^0-9]', '', input_str)  # Eliminar todos los caracteres que no sean dígitos
    minutes = seconds = 0

    if format_type == "mm:ss / km":
        minutes = int(time_str[:2]) if time_str[:2] else 0
        seconds = int(time_str[2:4]) if time_str[2:4] else 0

    time_delta = timedelta(minutes=minutes, seconds=seconds)
    return time_delta


def convert_timedelta_to_string(td:timedelta, format_type):
    hours = td.seconds // 3600
    minutes = (td.seconds // 60) % 60
    seconds = td.seconds % 60

    td_string = ''
    if format_type == "mm:ss / km":
        td_string = "{}:{} / km".format(minutes, seconds)

    return td_string

def time_seconds_to_string_format(time):
    total_seconds = time // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

    return formatted_time

def average_to_format_string(average):
    ms_per_km = average  # ms/km
    s_per_km = ms_per_km * 1000      # s/km
    min_per_km = s_per_km / 60       # min/km

    ritmo_minutes = int(min_per_km)
    ritmo_seconds = int((min_per_km - ritmo_minutes) * 60)
    formatted_ritmo = f"{ritmo_minutes}'{ritmo_seconds:02}\"/km"

    return formatted_ritmo
