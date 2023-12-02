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

def convert_to_int(value):
    """_summary_

    Args:
        value (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


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
