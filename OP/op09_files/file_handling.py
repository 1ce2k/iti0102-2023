import csv
import re
from datetime import datetime


def read_csv_file_into_list_of_dicts_using_datatypes(filename: str) -> list[dict]:
    """
    Read data from a CSV file and cast values into different data types based on their content.

    Fields containing only numbers are cast into integers.
    Fields containing dates (in the format dd.mm.yyyy) are cast into date.
    Otherwise, the data type remains string (default by csv reader).
    The order of elements in the list matches the lines in the file.
    None values don't affect the data type (the column will have the type based on the existing values).

    Hint: For date parsing, you can use the strptime method. See examples here:
    https://docs.python.org/3/library/datetime.html#examples-of-usage-date

    If a field contains only numbers, it's cast to int:
    name,age
    john,11
    mary,14

    Will become ('age' is int):
    [
      {'name': 'john', 'age': 11},
      {'name': 'mary', 'age': 14}
    ]

    If a field contains text or mixed content, it remains as a string:
    name,age
    john,11
    mary,14
    ago,unknown

    Will become ('age' cannot be cast to int because of "ago"):
    [
      {'name': 'john', 'age': '11'},
      {'name': 'mary', 'age': '14'},
      {'name': 'ago', 'age': 'unknown'}
    ]

    If a field contains only dates, it's cast to date:
    name,date
    john,01.01.2022
    mary,07.09.2023

    Will become:
    [
      {'name': 'john', 'date': datetime.date(2022, 1, 1)},
      {'name': 'mary', 'date': datetime.date(2023, 9, 7)},
    ]

    Example:
    name,date
    john,01.01.2022
    mary,late 2023

    Will become:
    [
      {'name': 'john', 'date': "01.01.2022"},
      {'name': 'mary', 'date': "late 2023"},
    ]

    A missing value "-" is interpreted as None (data type is not affected):
    name,date
    john,-
    mary,07.09.2023

    Will become:
    [
      {'name': 'john', 'date': None},
      {'name': 'mary', 'date': datetime.date(2023, 9, 7)},
    ]

    :param filename: The name of the CSV file to read.
    :return: A list of dictionaries containing processed field values.
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        line_count = sum(1 for row in reader)
        if line_count == 1:
            return []
        keys = next(reader)
        res = [[] for _ in range(len(keys))]
        converted_data = []
        for line in reader:
            line_parts = line
            for i in range(len(keys)):
                res[i].append(line_parts[i])
        for item in res:
            is_digits = all_elements_int_or_dash(item)
            is_dates = all_elements_date_or_dash(item)
            temp = []
            if is_digits:
                temp = convert_to_int(item)
            elif is_dates:
                temp = convert_to_dates(item)
            else:
                temp = convert_strings(item)
            converted_data.append(temp)
    ret = [{key: value[i] for key, value in zip(keys, converted_data)} for i in range(len(converted_data[0]))]
    return ret


def all_elements_int_or_dash(input_list: list):
    """Check if all elements are same type."""
    for item in input_list:
        if not (item.isdigit() or item == '-'):
            return False
    return True


def all_elements_date_or_dash(data: list):
    """Check if all elements are same type."""
    date_pattern = r'\d{2}\.\d{2}.\d{4}'
    for item in data:
        if item != '-' and not re.match(date_pattern, item) or (item != '-' and not is_valid_date(item)):
            return False
    return True


def is_valid_date(date_str):
    """Check if date exists."""
    day, month, year = map(int, date_str.split('.'))
    if (1 <= month <= 12) and (1 <= day <= 31):
        if month in [4, 6, 9, 11] and day > 30:
            return False
        if month == 2:
            if (day > 29) or (day == 29 and not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))):
                return False
        return True
    return False


def convert_to_int(data: list):
    """Convert from str to int."""
    res = []
    for element in data:
        if element.isdigit():
            res.append(int(element))
        elif element == '-':
            res.append(None)
    return res


def convert_to_dates(data: list):
    """Convert from str t0 datetime.date."""
    res = []
    for element in data:
        if element != '-':
            res.append(datetime.strptime(element, '%d.%m.%Y').date())
        else:
            res.append(None)
    return res


def convert_strings(data: list):
    """Convert from - to None in str."""
    res = []
    for item in data:
        res.append(None) if item == '-' else res.append(item)
    return res


print(read_csv_file_into_list_of_dicts_using_datatypes('../../EX/ex09_files/input.csv'))
