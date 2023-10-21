"""Create table from the given string."""
import re


def create_table_string(text: str) -> str:
    """
    Create table string from the given logs.

    Example of logs:

    [10:50 UTC+8] nothing here
    [12:25 UTC-2] error 404

    There are a total of five categories you need to find the items for.
    Here are the rules for finding them:

    1. Time
    - Hour can be one or two characters long (1, 01, and 11)
    - Minute can be one or two characters long (2, 02, 22)
    - UTC offset ranges from -12 to 12
    - Times in the text are formatted in 24 hour time format (https://en.wikipedia.org/wiki/24-hour_clock)
    - Minimum time is 00:00 (0:00 and 0,00 and 00-0 are also valid)
    - Maximum time is 23:59
    - Hour and minute can be separated by any non-numeric character (01:11, 1.2, 6;5 and 1a4 are valid while 12345 is not)
    2. Username starts after "usr:" and contains letters, numbers and underscores ("_")
    3. Error code is a non-negative number up to 3 digits and comes after a case-insensitive form of "error "
    4. IPv4 address is good enough if it's a group of four 1- to 3-digit numbers separated by dots
    5. Endpoint starts with a slash ("/") and contains letters, numbers and "&/=?-_%"

    Each table row consists of a category name and items belonging to that category.
    Categories are named and ordered as follows: "time", "user", "error", "ipv4" and "endpoint".

    Table from the above input example:

    time  | 2.50 AM, 14.25 PM
    error | 404

    The category name and its items are separated by a vertical bar ("|").
    The length between the category name and separator is one whitespace (" ") for the longest category name in the table.
    The length between the separator and items is one whitespace.
    Items for each category are unique and are separated by a comma and a whitespace (", ") and must be sorted in ascending order.
    Times in the table are formatted in 12 hour time format (https://en.wikipedia.org/wiki/12-hour_clock), like "1:12 PM"
    and "12:00 AM".
    Times in the table should be displayed in UTC(https://et.wikipedia.org/wiki/UTC) time.
    """
    time = format_times(text)
    user = get_usernames(text)
    error = get_errors(text)
    ipv4 = get_addresses(text)
    endpoint = get_endpoints(text)
    max_width = get_max_width(time, user, error, ipv4, endpoint)
    table = []
    if time:
        table.append(f'{"time".ljust(max_width)}' + '| ' + f'{", ".join(time)}')
    if user:
        table.append(f'{"user".ljust(max_width)}' + '| ' + f'{", ".join(sorted(set(user)))}')
    if error:
        table.append(f'{"error".ljust(max_width)}' + '| ' + f'{", ".join(str(x) for x in sorted(set(error)))}')
    if ipv4:
        table.append(f'{"ipv4".ljust(max_width)}' + '| ' + f'{", ".join(sorted(set(ipv4)))}')
    if endpoint:
        table.append(f'{"endpoint".ljust(max_width)}' + '| ' + f'{", ".join(sorted(set(endpoint)))}')
    ret = '\n'.join(table)
    return ret


def get_max_width(time, user, error, ipv4, endpoint) -> int:
    """Find max length of left column."""
    if endpoint:
        return 9
    if error:
        return 6
    if user or time or ipv4:
        return 5


def get_times(text: str) -> list[tuple[int, int, int]]:
    """
    Get times from text using the time pattern.

    The result should be a list of tuples containing the time that's not normalized and UTC offset.

    For example:

    [10:53 UTC+3] -> [(10, 53, 3)]
    [1:43 UTC+0] -> [(1, 43, 0)]
    [14A3 UTC-4] [14:3 UTC-4] -> [(14, 3, -4), (14, 3, -4)]

    :param text: text to search for the times
    :return: list of tuples containing the time and offset
    """
    regex_pattern = r'\[(\d{1,2})[^\d]+(\d{1,2}).*?UTC([+-]?\d{1,2})'
    ret = []
    for hour, minute, offset in re.findall(regex_pattern, text):
        if -12 <= int(offset) <= 12 and 0 <= int(hour) <= 23 and 0 <= int(minute) <= 59:
            ret.append((int(hour), int(minute), int(offset)))
    return ret


def get_usernames(text: str) -> list[str]:
    """Get usernames from text."""
    return re.findall(r'usr:(\w+)', text)


def get_errors(text: str) -> list[int]:
    """Get errors from text."""
    return [int(error) for error in re.findall(r'(?i)error (\d{1,3})', text)]


def get_addresses(text: str) -> list[str]:
    """Get IPv4 addresses from text."""
    return re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)


def get_endpoints(text: str) -> list[str]:
    """Get endpoints from text."""
    return re.findall(r'/(?![^\[\]]*\sUTC[+-]\d+)\S+', text)


def format_times(text: str) -> list[str]:
    """Format time from 24h to 12h."""
    times = get_times(text)
    in_minutes = []

    for hour, minute, offset in times:
        hour = hour - offset
        if hour < 0:
            hour = 24 + hour
        elif hour >= 24:
            hour = hour - 24
        in_minute = hour * 60 + minute
        in_minutes.append(in_minute)
    ret = []
    for minute in sorted(set(in_minutes)):
        hour = minute // 60
        meridian = "AM" if hour < 12 else "PM"
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12
        new_time = f"{hour}:{minute % 60:02d} {meridian}"
        ret.append(new_time)
    return ret


if __name__ == '__main__':
    logs = """
            [14?36yjjynybutcUTC+9] /tere eRRoR 418 192.168.0.255
            [8B48 UTC-6] usr:kasutaja
            """
    print(create_table_string(logs))
    # time     | 5:36 AM, 2:48 PM
    # user     | kasutaja
    # error    | 418
    # ipv4     | 192.168.0.255
    # endpoint | /tere
