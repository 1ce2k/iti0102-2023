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
        table.append(f'{"user".ljust(max_width)}' + '| ' + f'{", ".join(sorted(user))}')
    if error:
        table.append(f'{"error".ljust(max_width)}' + '| ' + f'{", ".join(str(x) for x in sorted(error))}')
    if ipv4:
        table.append(f'{"ipv4".ljust(max_width)}' + '| ' + f'{", ".join(sorted(ipv4))}')
    if endpoint:
        table.append(f'{"endpoint".ljust(max_width)}' + '| ' + f'{", ".join(sorted(endpoint))}')
    ret = '\n'.join(table)
    return ret


def get_max_width(time, user, error, ipv4, endpoint) -> int:
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
    regex_pattern = r'\[(\d{1,2})[^\d](\d{1,2}) UTC([+-]?\d{1,2})'
    return [(int(hour), int(minute), int(offset)) for hour, minute, offset in re.findall(regex_pattern, text) if
            -12 <= int(offset) <= 12 and 0 <= int(hour) <= 23 and 0 <= int(minute) <= 59]


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
    return re.findall(r'/[A-Za-z0-9&\/=?\-_%]+', text)


def format_times(text: str) -> list[str]:
    times = get_times(text)
    times_in_minute = []
    for hour, minute, offset in times:
        new_time = hour - offset
        if new_time < 0:
            new_time = 24 + new_time
        time_in_minute = new_time * 60 + minute
        times_in_minute.append(time_in_minute)
    ret = []
    for minute in sorted(set(times_in_minute)):
        new_time = ''
        if 60 <= minute <= 720:
            new_time = f'{minute // 60}:{minute % 60:02d} AM'
        elif minute <= 59:
            new_time = f'12:{minute % 60:02d} AM'
        elif 721 <= minute <= 1380:
            new_time = f'{(minute - 12 * 60) // 60}:{minute % 60:02d} PM'
        elif 1381 <= minute < 1440:
            new_time = f'23:{minute % 60:02d} PM'
        ret.append(new_time)
    return ret


if __name__ == '__main__':
    logs = """
            [14?36 UTC+9] /tere eRRoR 418 192.168.0.255
            [8B48 UTC-6] usr:kasutaja
            """
    print(create_table_string(logs))
    # time     | 5:36 AM, 2:48 PM
    # user     | kasutaja
    # error    | 418
    # ipv4     | 192.168.0.255
    # endpoint | /tere

    print()

    logs2 = """
        [-1b35 UTC-4] errOR 741
        [24a48 UTC+0] 776.330.579.818
        [02:53 UTC+5] usr:96NC9yqb /aA?Y4pK
        [5b05 UTC+5] ERrOr 700 268.495.856.225
        [24-09 UTC+10] usr:uJV5sf82_ eRrOR 844 715.545.485.989
        [04=54 UTC+3] eRROR 452
        [11=57 UTC-6] 15.822.272.473 error 9
        [15=53 UTC+7] /NBYFaC0 468.793.214.681
        [23-7 UTC+12] /1slr8I
        [07.46 UTC+4] usr:B3HIyLm 119.892.677.533
        [0:60 UTC+0] bad
        [0?0 UTC+0] ok
        [0.0 UTC+0] also ok
        """
    print(create_table_string(logs2))
    # time     | 12:00 AM, 12:05 AM, 1:54 AM, 3:46 AM, 8:53 AM, 11:07 AM, 5:57 PM, 9:53 PM
    # user     | 96NC9yqb, B3HIyLm, uJV5sf82_
    # error    | 9, 452, 700, 741, 844
    # ipv4     | 119.892.677.533, 15.822.272.473, 268.495.856.225, 468.793.214.681, 715.545.485.989, 776.330.579.818
    # endpoint | /1slr8I, /NBYFaC0, /aA?Y4pK

    # print(format_times(logs2))