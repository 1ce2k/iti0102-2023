"""OP09."""
import csv
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
    list_not_types = read_csv_file_into_list_of_dicts(filename)
    if not list_not_types:
        return []
    keys_list = []
    dict_same_type = {}
    final_list = []
    for key in list_not_types[0].keys():
        keys_list.append(key)
        dict_same_type[key] = is_all_same_type(list_not_types, key)
    for dictionary in list_not_types:
        sub_dict = {}
        for key in keys_list:
            if dict_same_type[key]:
                type_info = find_info_type(dictionary[key])
                if type_info == "-":
                    sub_dict[key] = None
                elif type_info == "int":
                    sub_dict[key] = int(dictionary[key])
                elif type_info == "date":
                    my_date = datetime.date(datetime.datetime.strptime((dictionary[key]), "%d.%m.%Y"))
                    sub_dict[key] = my_date
                else:
                    sub_dict[key] = dictionary[key]
            else:
                if dictionary[key] == "-":
                    sub_dict[key] = None
                else:
                    sub_dict[key] = dictionary[key]
        final_list.append(sub_dict)
    return final_list


def is_all_same_type(list_of_dicts: list, key: str) -> bool:
    element_list = []
    for dictionary in list_of_dicts:
        element_list.append(dictionary[key])
    for element in element_list:
        if element == "-":
            continue
        first_type = find_info_type(element)
    for element in element_list:
        if element == "-":
            continue
        type_element = find_info_type(element)
        if first_type != type_element:
            return False
    return True


def find_info_type(info: str) -> str:
    if info == "-":
        return "-"
    try:
        int(info)
        return "int"
    except ValueError:
        try:
            datetime.datetime.strptime(info, "%d.%m.%Y") or datetime.datetime.strptime(info, "%Y.%m.%d")
            return "date"
        except ValueError:
            return "str"

# def read_people_data(directory: str) -> dict[int, dict]:
#     """
#     Read people data from CSV files and merge information.
#
#     This function reads CSV files located inside the specified directory, and all *.csv files are read.
#     Each file is expected to have an integer field "id" which is used to merge information.
#     The result is a single dictionary where the keys are "id" and the values are
#     dictionaries containing all the different values across the files.
#     Missing keys are included in every dictionary with None as the value.
#
#     File: a.csv
#     id,name
#     1,john
#     2,mary
#     3,john
#
#     File: births.csv
#     id,birth
#     1,01.01.2001
#     2,05.06.1990
#
#     File: deaths.csv
#     id,death
#     2,01.02.2022
#     1,-
#
#     Will become:
#     {
#         1: {"id": 1, "name": "john", "birth": datetime.date(2001, 1, 1), "death": None},
#         2: {"id": 2, "name": "mary", "birth": datetime.date(1990, 6, 5),
#             "death": datetime.date(2022, 2, 1)},
#         3: {"id": 3, "name": "john", "birth": None, "death": None},
#     }
#
#     :param directory: The directory containing CSV files.
#     :return: A dictionary with "id" as keys and data dictionaries as values.
#     """
#     files = []
#     keys = []
#     for filename in os.listdir(f'{directory}'):
#         if filename[-4:] == '.csv':
#             files.append(f'{directory}/{filename}')
#             temp = find_keys(f'{directory}/{filename}')
#             for key in temp:
#                 if key not in keys:
#                     keys.append(key)
#     # print(keys)
#     # print(files)
#     data = []
#     for file in files:
#         data.append(read_csv_file_into_list_of_dicts_using_datatypes(file))
#     # print(data)
#     people_data = {}
#     for sublist in data:
#         for item in sublist:
#             # print(item)
#             id = item['id']
#             if id not in people_data:
#                 people_data[id] = {'id': id, **{key: None for key in keys[1:]}}
#             people_data[id].update(item)
#     return people_data


# def find_keys(file: str):
#     """Find all keys from data."""
#     with open(file, 'r') as file:
#         reader = csv.reader(file)
#         keys = next(reader)
#         return keys


# def generate_people_report(person_data_directory: str, report_filename: str) -> None:
#     """
#     Generate a report about people data from CSV files.
#
#     Note: Use the read_people_data() function to read the data from CSV files.
#
#     Input files should contain fields "birth" and "death," which are dates in the format "dd.mm.yyyy".
#     There are no duplicate headers in the files except for the "id" field.
#
#     The report is a CSV file that includes all fields from the input data along with two fields:
#     - "status": Either "dead" or "alive" based on the presence of a death date;
#     - "age": The current age or the age of death, calculated in full years.
#       If there is no birthdate, the age is set to -1.
#
#     Example:
#     - Birth 01.01.1940, death 01.01.2022 => age: 80
#     - Birth 02.01.1940, death 01.01.2022 => age: 79
#
#     Hint: You can compare dates directly when calculating age.
#
#     The lines in the report are ordered based on the following criteria:
#     - Age ascending (younger before older); lines with incalculable age come last;
#     - If the age is the same, birthdate descending (newer birth before older birth);
#     - If both the age and birthdate are the same, sorted by name ascending (a before b);
#       If a name is not available, use "" (people with missing names should come before people with name);
#     - If names are the same or the name field is missing, ordered by id ascending.
#
#     :param person_data_directory: The directory containing CSV files.
#     :param report_filename: The name of the file to write to.
#     :return: None
#     """
#     data = read_people_data(person_data_directory)
#     # print(data)
#     report_data = []
#     for person in data.values():
#         birth_date = person.get('birth')
#         death_date = person.get('death')
#         if birth_date:
#             current_date = datetime.datetime.now().date()
#             if death_date:
#                 age = round((death_date - birth_date).days // 365.25)
#                 status = 'dead'
#             else:
#                 age = round((current_date - birth_date).days // 365.25)
#                 status = 'alive'
#         else:
#             age = -1
#             status = 'unknown'
#         person['status'] = status
#         person['age'] = age
#
#         report_data.append(person)
#
#     report_data = sorted(report_data, key=sort_key)
#
#     ret = []
#     for person_ in report_data:
#         for key, value in person_.items():
#             if value is None:
#                 person_[key] = '-'
#             elif re.match(r'\d{4}-\d{2}-\d{2}', str(value)):
#                 person_[key] = datetime.datetime.strftime(value, '%d.%m.%Y')
#         ret.append(person_)
#
#     with open(report_filename, 'w', newline='') as file:
#         fieldnames = ret[0].keys()
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(ret)


# def sort_key(person):
#     age = person['age']
#     if age == -1:
#         return person['age'] < 0, person['age']
#     return person['age'] < 0, person['age'], -datetime.datetime.strptime(person.get('birth', datetime.date.today()).strftime('%d.%m.%Y'), '%d.%m.%Y').timestamp(), person.get('name', ''), person.get('last name', ''), person['id']


# (x.get('age', '-1'), -datetime.datetime.strptime(
#                                     x.get('birth', datetime.date.today()).strftime('%d.%m.%Y'), '%d.%m.%Y').timestamp(),
#                                     x.get('name', ''), x.get('last name', ''), x['id']))

# generate_people_report('data', 'report.csv')
