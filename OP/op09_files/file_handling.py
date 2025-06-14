"""OP09."""
import csv
import os
import re
import datetime


def read_csv_file_into_list_of_dicts(filename: str) -> list[dict[str, str]]:
    """Read a CSV file into a list of dictionaries."""
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    if len(data) < 2:
        return []
    keys = data[0]
    # print(keys)
    result = []
    for line in data[1:]:
        data_dict = {}
        for i in range(len(keys)):
            data_dict[keys[i]] = line[i]
        result.append(data_dict)
    return result


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
        first = next(reader, None)
        check = next(reader, None)
        if check is None or first is None:
            return []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
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
            res.append(datetime.datetime.strptime(element, '%d.%m.%Y').date())
        else:
            res.append(None)
    return res


def convert_strings(data: list):
    """Convert from - to None in str."""
    res = []
    for item in data:
        res.append(None) if item == '-' else res.append(item)
    return res


def read_people_data(directory: str) -> dict[int, dict]:
    """
    Read people data from CSV files and merge information.

    This function reads CSV files located inside the specified directory, and all *.csv files are read.
    Each file is expected to have an integer field "id" which is used to merge information.
    The result is a single dictionary where the keys are "id" and the values are
    dictionaries containing all the different values across the files.
    Missing keys are included in every dictionary with None as the value.

    File: a.csv
    id,name
    1,john
    2,mary
    3,john

    File: births.csv
    id,birth
    1,01.01.2001
    2,05.06.1990

    File: deaths.csv
    id,death
    2,01.02.2022
    1,-

    Will become:
    {
        1: {"id": 1, "name": "john", "birth": datetime.date(2001, 1, 1), "death": None},
        2: {"id": 2, "name": "mary", "birth": datetime.date(1990, 6, 5),
            "death": datetime.date(2022, 2, 1)},
        3: {"id": 3, "name": "john", "birth": None, "death": None},
    }

    :param directory: The directory containing CSV files.
    :return: A dictionary with "id" as keys and data dictionaries as values.
    """
    # files = []
    # keys = []
    # for filename in os.listdir(f'{directory}'):
    #     if filename[-4:] == '.csv':
    #         files.append(f'{directory}/{filename}')
    #         temp = find_keys(f'{directory}/{filename}')
    #         for key in temp:
    #             if key not in keys:
    #                 keys.append(key)
    # print(keys)
    # print(files)
    # data = []
    # for file in files:
    #     data.append(read_csv_file_into_list_of_dicts_using_datatypes(file))
    # # print(data)
    # people_data = {}
    # for sublist in data:
    #     for item in sublist:
    #         # print(item)
    #         id = item['id']
    #         if id not in people_data:
    #             people_data[id] = {'id': id, **{key: None for key in keys[1:]}}
    #         people_data[id].update(item)
    # return people_data
    all_list = []
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            file_data = read_csv_file_into_list_of_dicts_using_datatypes(os.path.join(directory, file))
            all_list.append(file_data)
    id_list = []
    for dictionary in all_list[0]:
        id_list.append(dictionary['id'])
    id_list.sort()
    final_dict = {}
    for id in id_list:
        id_dict = {}
        for sub_list in all_list:
            for dictionary in sub_list:
                if dictionary['id'] == id:
                    for key in dictionary.keys():
                        id_dict[key] = dictionary[key]
        final_dict[id] = id_dict
    return final_dict


def calculate_age(birth: datetime, death: datetime) -> str:
    """Calculate age."""
    birth_year = birth.year
    if death == '-':
        current_year, current_month, current_day = datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day
    else:
        current_year, current_month, current_day = death.year, death.month, death.day
    age_rough = int(current_year) - int(birth_year)
    if current_month > birth.month:
        return str(age_rough)
    elif current_month < birth.month:
        return str(age_rough - 1)
    else:
        if current_day >= birth.day:
            return str(age_rough)
        else:
            return str(age_rough - 1)


def find_all_keys(input_list: list) -> list:
    """Fina keys."""
    key_list = []
    for dict in input_list:
        for key in dict.keys():
            if key not in key_list:
                key_list.append(key)
    return key_list


def sort_age(age: str) -> int:
    """Sort age."""
    if int(age) >= 0:
        return int(age)
    return int(age) + 1000


def sort_birth(birth: str) -> int:
    """Sort birth dates."""
    if birth == '-':
        return 0
    total_days = int(birth[:2]) + int(birth[3:5]) * 30 + int(birth[6:]) * 365
    return total_days


def sort_dict_by_keys(input_list: list) -> list:
    """Sort dicts."""
    sorted_list = []
    age_dicts = []
    birth_dicts = []
    for dictionary in input_list:
        if dictionary["age"] != "-1":
            age_dicts.append(dictionary)
        else:
            birth_dicts.append(dictionary)
    if "name" in age_dicts[0].keys():
        age_dicts.sort(
            key=lambda x: (sort_age(x["age"]), -sort_birth(x["birth"]), x["name"], x["id"]))
    else:
        age_dicts.sort(key=lambda x: (sort_age(x["age"]), -sort_birth(x["birth"]), x["id"]))
    for dic in age_dicts:
        sorted_list.append(dic)
    birth_dicts.sort(key=lambda x: (sort_birth(x["birth"]), x["name"], x["id"]))
    for dictionary in birth_dicts:
        sorted_list.append(dictionary)
    return sorted_list


def create_list_to_write(info_dict):
    """Create list to write."""
    list_to_write = []
    for value in info_dict.values():
        list_to_write.append(value)
    return list_to_write


def help_func_1(sub_dict, dictionary, key_list):
    """Help func."""
    if 'name' in key_list:
        sub_dict['name'] = dictionary['name']
    elif 'notname' in key_list:
        sub_dict['name'] = dictionary['notname']
    if sub_dict['death'] == '-':
        sub_dict['status'] = 'alive'
    else:
        sub_dict['status'] = 'dead'
    if dictionary['birth'] == '-':
        sub_dict['age'] = '-1'
    else:
        sub_dict['age'] = calculate_age(dictionary['birth'], dictionary['death'])
    return sub_dict


def generate_people_report(person_data_directory: str, report_filename: str) -> None:
    """
    Generate a report about people data from CSV files.

    Note: Use the read_people_data() function to read the data from CSV files.

    Input files should contain fields "birth" and "death," which are dates in the format "dd.mm.yyyy".
    There are no duplicate headers in the files except for the "id" field.

    The report is a CSV file that includes all fields from the input data along with two fields:
    - "status": Either "dead" or "alive" based on the presence of a death date;
    - "age": The current age or the age of death, calculated in full years.
      If there is no birthdate, the age is set to -1.

    Example:
    - Birth 01.01.1940, death 01.01.2022 => age: 80
    - Birth 02.01.1940, death 01.01.2022 => age: 79

    Hint: You can compare dates directly when calculating age.

    The lines in the report are ordered based on the following criteria:
    - Age ascending (younger before older); lines with incalculable age come last;
    - If the age is the same, birthdate descending (newer birth before older birth);
    - If both the age and birthdate are the same, sorted by name ascending (a before b);
      If a name is not available, use "" (people with missing names should come before people with name);
    - If names are the same or the name field is missing, ordered by id ascending.

    :param person_data_directory: The directory containing CSV files.
    :param report_filename: The name of the file to write to.
    :return: None
    """
    info_dict = read_people_data(person_data_directory)
    list_to_write = create_list_to_write(info_dict)
    final_list = []
    keys_list = find_all_keys(list_to_write)
    for dictionary in list_to_write:
        sub_dict = {}
        for key in keys_list:
            if key not in dictionary.keys() or dictionary[key] is None:
                dictionary[key] = "-"
            if str(type(dictionary[key])) == "<class 'datetime.date'>":
                sub_dict[key] = dictionary[key].strftime("%d.%m.%Y")
            else:
                sub_dict[key] = dictionary[key]
            sub_dict['id'] = dictionary['id']
        if dictionary['birth'] != '-':
            sub_dict['birth'] = dictionary['birth'].strftime('%d.%m.%Y')
        else:
            sub_dict['birth'] = dictionary['birth']
        if dictionary['death'] != '-':
            sub_dict['death'] = dictionary['death'].strftime('%d.%m.%Y')
        else:
            sub_dict['death'] = dictionary['death']
        sub_dict = help_func_1(sub_dict, dictionary, keys_list)
        final_list.append(sub_dict)
        sorted_list = sort_dict_by_keys(final_list)
        write_list_of_dicts_to_csv_file(report_filename, sorted_list)


# generate_people_report('data', 'report.csv')


def write_list_of_dicts_to_csv_file(filename: str, data: list[dict]) -> None:
    """Write a list of dictionaries to a CSV file."""
    if not data:
        return
    keys = set(key for row in data for key in row.keys())
    print(keys)
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
