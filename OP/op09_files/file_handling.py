"""OP09."""
import csv
import re
from datetime import datetime
import os


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
    files = []
    keys = []
    for filename in os.listdir(f'{directory}'):
        if filename[-4:] == '.csv':
            files.append(f'{directory}/{filename}')
            temp = find_keys(f'{directory}/{filename}')
            for key in temp:
                if key not in keys:
                    keys.append(key)
    # print(keys)
    # print(files)
    data = []
    for file in files:
        data.append(read_csv_file_into_list_of_dicts_using_datatypes(file))
    # print(data)
    people_data = {}
    for sublist in data:
        for item in sublist:
            # print(item)
            id = item['id']
            if id not in people_data:
                people_data[id] = {'id': id, **{key: None for key in keys[1:]}}
            people_data[id].update(item)
    return people_data


def find_keys(file: str):
    """Find all keys from data."""
    with open(file, 'r') as file:
        reader = csv.reader(file)
        keys = next(reader)
        return keys


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
    data = read_people_data(person_data_directory)
    # print(data)
    report_data = []
    for person in data.values():
        birth_date = person.get('birth')
        death_date = person.get('death')
        if birth_date:
            current_date = datetime.now().date()
            if death_date:
                age = (death_date - birth_date).days // 365
                status = 'dead'
            else:
                age = (current_date - birth_date).days // 365
                status = 'alive'
        else:
            age = -1
            status = 'unknown'
        person['status'] = status
        person['age'] = age
        for key, value in person.items():
            print(type(value))
            if value is None:
                person[key] = '-'
            if re.match(r'\d{4}-\d{2}-\d{2}', str(value)):
                person[key] = f'{str(value).split("-")[2]}.{str(value).split("-")[1]}.{str(value).split("-")[0]}'

        report_data.append(person)

    report_data.sort(key=lambda x: (x['age'], x.get('birth', datetime.max.date()), x.get('name', ''), x['id']))
    # print(report_data)

    with open(report_filename, 'w', newline='') as file:
        fieldnames = report_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_data)


print(generate_people_report('data', 'report.csv'))

# report_data = [{'first kiss': '-', 'death': '18.09.2015', 'radius': '-', 'size': '69', 'city': 'dstd', 'id': '95', 'status': 'dead', 'location': 'hudw', 'name': 'qqfx', 'birthday': '-', 'some number': '-', 'age': '1', 'birth': '06.09.2014'}, {'first kiss': '-', 'death': '05.01.2019', 'radius': '75', 'size': '-', 'city': '-', 'id': '21', 'status': 'dead', 'location': 'ubes', 'name': 'nspf', 'birthday': '-', 'some number': '5', 'age': '2', 'birth': '07.05.2016'}, {'first kiss': '16.06.1948', 'death': '10.08.1994', 'radius': '-', 'size': '92', 'city': 'pruh', 'id': '82', 'status': 'dead', 'location': '-', 'name': 'pyiw', 'birthday': '-', 'some number': '95', 'age': '2', 'birth': '26.06.1992'}, {'first kiss': '-', 'death': '07.04.2020', 'radius': '88', 'size': '-', 'city': 'wivy', 'id': '72', 'status': 'dead', 'location': 'fyfq', 'name': 'mjzk', 'birthday': '-', 'some number': '-', 'age': '4', 'birth': '01.01.2016'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '11', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '05.11.1933', 'some number': '-', 'age': '5', 'birth': '20.07.2018'}, {'first kiss': '-', 'death': '-', 'radius': '100', 'size': '65', 'city': '-', 'id': '7', 'status': 'alive', 'location': 'dbcw', 'name': '-', 'birthday': '-', 'some number': '35', 'age': '8', 'birth': '28.10.2015'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '75', 'city': 'zgaz', 'id': '22', 'status': 'alive', 'location': 'mfzu', 'name': '-', 'birthday': '-', 'some number': '50', 'age': '8', 'birth': '12.11.2014'}, {'first kiss': '01.05.1995', 'death': '-', 'radius': '29', 'size': '47', 'city': '-', 'id': '36', 'status': 'alive', 'location': 'mlwh', 'name': 'gkyv', 'birthday': '-', 'some number': '-', 'age': '13', 'birth': '21.12.2009'}, {'first kiss': '-', 'death': '-', 'radius': '45', 'size': '-', 'city': 'aatn', 'id': '29', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '14.02.1939', 'some number': '23', 'age': '13', 'birth': '28.11.2009'}, {'first kiss': '19.11.2004', 'death': '-', 'radius': '59', 'size': '85', 'city': 'vpyc', 'id': '6', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '14', 'birth': '20.09.2009'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '38', 'status': 'alive', 'location': 'uxmb', 'name': 'exsr', 'birthday': '25.04.1994', 'some number': '61', 'age': '15', 'birth': '28.10.2008'}, {'first kiss': '05.03.1980', 'death': '-', 'radius': '-', 'size': '75', 'city': '-', 'id': '48', 'status': 'alive', 'location': 'ncoz', 'name': '-', 'birthday': '-', 'some number': '51', 'age': '15', 'birth': '26.09.2008'}, {'first kiss': '09.12.1967', 'death': '26.05.2005', 'radius': '77', 'size': '-', 'city': '-', 'id': '66', 'status': 'dead', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '38', 'age': '15', 'birth': '13.09.1989'}, {'first kiss': '25.11.1940', 'death': '-', 'radius': '-', 'size': '18', 'city': 'modm', 'id': '23', 'status': 'alive', 'location': 'brij', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '16', 'birth': '01.05.2007'}, {'first kiss': '-', 'death': '28.08.1982', 'radius': '92', 'size': '99', 'city': 'vgji', 'id': '27', 'status': 'dead', 'location': '-', 'name': 'pbps', 'birthday': '-', 'some number': '-', 'age': '16', 'birth': '19.04.1966'}, {'first kiss': '-', 'death': '-', 'radius': '67', 'size': '-', 'city': 'dugi', 'id': '39', 'status': 'alive', 'location': 'fnbo', 'name': '-', 'birthday': '10.12.1943', 'some number': '70', 'age': '17', 'birth': '21.02.2006'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': 'ppzy', 'id': '5', 'status': 'alive', 'location': 'dhnu', 'name': 'rdlq', 'birthday': '06.02.1992', 'some number': '-', 'age': '17', 'birth': '12.11.2005'}, {'first kiss': '02.03.1961', 'death': '-', 'radius': '-', 'size': '80', 'city': '-', 'id': '1', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '07.02.1981', 'some number': '-', 'age': '19', 'birth': '16.03.2004'}, {'first kiss': '-', 'death': '-', 'radius': '17', 'size': '22', 'city': '-', 'id': '35', 'status': 'alive', 'location': 'perj', 'name': 'iigt', 'birthday': '19.01.1964', 'some number': '98', 'age': '20', 'birth': '08.07.2003'}, {'first kiss': '-', 'death': '-', 'radius': '70', 'size': '86', 'city': '-', 'id': '19', 'status': 'alive', 'location': 'qwrk', 'name': 'vwkk', 'birthday': '10.01.2000', 'some number': '-', 'age': '20', 'birth': '02.11.2002'}, {'first kiss': '-', 'death': '-', 'radius': '30', 'size': '-', 'city': '-', 'id': '96', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '02.04.1974', 'some number': '-', 'age': '22', 'birth': '08.04.2001'}, {'first kiss': '28.08.1958', 'death': '-', 'radius': '96', 'size': '8', 'city': '-', 'id': '50', 'status': 'alive', 'location': 'dnvv', 'name': '-', 'birthday': '-', 'some number': '28', 'age': '23', 'birth': '06.08.2000'}, {'first kiss': '-', 'death': '-', 'radius': '77', 'size': '6', 'city': 'qvcm', 'id': '80', 'status': 'alive', 'location': 'armn', 'name': '-', 'birthday': '-', 'some number': '67', 'age': '23', 'birth': '08.04.2000'}, {'first kiss': '-', 'death': '06.12.1964', 'radius': '-', 'size': '-', 'city': 'wpua', 'id': '30', 'status': 'dead', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '11', 'age': '23', 'birth': '23.08.1941'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '81', 'city': 'vaop', 'id': '10', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '09.01.1931', 'some number': '-', 'age': '26', 'birth': '25.07.1997'}, {'first kiss': '13.08.1968', 'death': '-', 'radius': '-', 'size': '24', 'city': 'cghn', 'id': '94', 'status': 'alive', 'location': 'mlxq', 'name': 'qlyx', 'birthday': '07.08.1997', 'some number': '-', 'age': '27', 'birth': '05.04.1996'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '34', 'city': 'rlbx', 'id': '93', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '02.04.1974', 'some number': '-', 'age': '27', 'birth': '06.01.1996'}, {'first kiss': '26.02.2008', 'death': '-', 'radius': '-', 'size': '8', 'city': 'eqyp', 'id': '43', 'status': 'alive', 'location': 'noch', 'name': '-', 'birthday': '28.08.2015', 'some number': '-', 'age': '28', 'birth': '22.08.1995'}, {'first kiss': '12.03.1936', 'death': '-', 'radius': '19', 'size': '-', 'city': '-', 'id': '42', 'status': 'alive', 'location': 'oyzj', 'name': 'diet', 'birthday': '-', 'some number': '82', 'age': '28', 'birth': '12.02.1995'}, {'first kiss': '26.02.1994', 'death': '18.08.2016', 'radius': '5', 'size': '91', 'city': 'mjoa', 'id': '47', 'status': 'dead', 'location': '-', 'name': 'vvwi', 'birthday': '23.11.1979', 'some number': '-', 'age': '28', 'birth': '06.06.1988'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '55', 'status': 'alive', 'location': 'pfub', 'name': 'qvxe', 'birthday': '09.05.1963', 'some number': '-', 'age': '29', 'birth': '22.09.1994'}, {'first kiss': '-', 'death': '-', 'radius': '88', 'size': '-', 'city': '-', 'id': '98', 'status': 'alive', 'location': '-', 'name': 'amfp', 'birthday': '-', 'some number': '-', 'age': '29', 'birth': '24.01.1994'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': 'mrpt', 'id': '28', 'status': 'alive', 'location': 'qrtj', 'name': '-', 'birthday': '-', 'some number': '72', 'age': '30', 'birth': '12.08.1993'}, {'first kiss': '20.07.1954', 'death': '-', 'radius': '-', 'size': '27', 'city': '-', 'id': '71', 'status': 'alive', 'location': 'hrgy', 'name': 'hdxi', 'birthday': '02.04.1955', 'some number': '-', 'age': '34', 'birth': '24.02.1989'}, {'first kiss': '-', 'death': '-', 'radius': '50', 'size': '-', 'city': 'znlv', 'id': '4', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '44', 'age': '37', 'birth': '05.05.1986'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '7', 'city': '-', 'id': '24', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '37', 'birth': '15.01.1986'}, {'first kiss': '-', 'death': '-', 'radius': '10', 'size': '-', 'city': 'ruhx', 'id': '74', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '18.07.1959', 'some number': '46', 'age': '38', 'birth': '16.12.1984'}, {'first kiss': '26.04.1980', 'death': '-', 'radius': '-', 'size': '5', 'city': 'zybm', 'id': '26', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '18.04.2014', 'some number': '6', 'age': '39', 'birth': '16.08.1984'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '45', 'city': '-', 'id': '37', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '20.09.1945', 'some number': '-', 'age': '40', 'birth': '03.06.1983'}, {'first kiss': '-', 'death': '-', 'radius': '47', 'size': '92', 'city': '-', 'id': '34', 'status': 'alive', 'location': '-', 'name': 'rihv', 'birthday': '14.04.2009', 'some number': '5', 'age': '41', 'birth': '12.06.1982'}, {'first kiss': '21.01.1930', 'death': '-', 'radius': '-', 'size': '77', 'city': '-', 'id': '67', 'status': 'alive', 'location': '-', 'name': 'omkj', 'birthday': '-', 'some number': '25', 'age': '42', 'birth': '26.10.1981'}, {'first kiss': '-', 'death': '-', 'radius': '17', 'size': '-', 'city': 'rsyb', 'id': '32', 'status': 'alive', 'location': 'djzz', 'name': '-', 'birthday': '28.07.1968', 'some number': '81', 'age': '42', 'birth': '25.10.1981'}, {'first kiss': '01.06.1952', 'death': '-', 'radius': '29', 'size': '-', 'city': '-', 'id': '53', 'status': 'alive', 'location': 'ltsm', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '42', 'birth': '18.06.1981'}, {'first kiss': '25.12.1930', 'death': '-', 'radius': '-', 'size': '9', 'city': 'sdtz', 'id': '41', 'status': 'alive', 'location': 'lstk', 'name': 'beqy', 'birthday': '26.02.1930', 'some number': '41', 'age': '43', 'birth': '12.12.1979'}, {'first kiss': '12.06.1947', 'death': '-', 'radius': '75', 'size': '61', 'city': 'chhx', 'id': '91', 'status': 'alive', 'location': 'ibaa', 'name': 'yapq', 'birthday': '24.01.2008', 'some number': '-', 'age': '45', 'birth': '02.06.1978'}, {'first kiss': '-', 'death': '-', 'radius': '36', 'size': '48', 'city': '-', 'id': '97', 'status': 'alive', 'location': 'rjbm', 'name': 'foqm', 'birthday': '02.09.1934', 'some number': '-', 'age': '45', 'birth': '24.02.1978'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '76', 'status': 'alive', 'location': '-', 'name': 'wsck', 'birthday': '-', 'some number': '17', 'age': '45', 'birth': '24.02.1978'}, {'first kiss': '-', 'death': '-', 'radius': '4', 'size': '-', 'city': 'vbdg', 'id': '56', 'status': 'alive', 'location': 'iafx', 'name': 'qtwc', 'birthday': '-', 'some number': '-', 'age': '46', 'birth': '10.08.1977'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '90', 'status': 'alive', 'location': '-', 'name': 'srzk', 'birthday': '-', 'some number': '57', 'age': '47', 'birth': '22.05.1976'}, {'first kiss': '-', 'death': '-', 'radius': '15', 'size': '-', 'city': '-', 'id': '52', 'status': 'alive', 'location': 'rosb', 'name': '-', 'birthday': '20.01.2013', 'some number': '-', 'age': '48', 'birth': '07.01.1975'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': 'ziyu', 'id': '61', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '18.12.1950', 'some number': '-', 'age': '51', 'birth': '22.03.1972'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '65', 'status': 'alive', 'location': '-', 'name': 'uqhi', 'birthday': '-', 'some number': '-', 'age': '52', 'birth': '22.10.1971'}, {'first kiss': '11.01.2002', 'death': '-', 'radius': '-', 'size': '-', 'city': 'ojuz', 'id': '13', 'status': 'alive', 'location': '-', 'name': 'ajma', 'birthday': '10.10.1989', 'some number': '86', 'age': '52', 'birth': '06.02.1971'}, {'first kiss': '25.05.1969', 'death': '-', 'radius': '-', 'size': '21', 'city': 'csos', 'id': '14', 'status': 'alive', 'location': 'lwty', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '53', 'birth': '24.05.1970'}, {'first kiss': '13.02.1955', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '73', 'status': 'alive', 'location': '-', 'name': 'vbmi', 'birthday': '09.01.1961', 'some number': '-', 'age': '54', 'birth': '18.10.1969'}, {'first kiss': '17.03.1930', 'death': '-', 'radius': '87', 'size': '-', 'city': '-', 'id': '51', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '21.10.1954', 'some number': '-', 'age': '55', 'birth': '21.01.1968'}, {'first kiss': '-', 'death': '-', 'radius': '91', 'size': '-', 'city': 'cxcc', 'id': '79', 'status': 'alive', 'location': '-', 'name': 'entw', 'birthday': '-', 'some number': '84', 'age': '56', 'birth': '02.06.1967'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '81', 'status': 'alive', 'location': 'desu', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '56', 'birth': '18.05.1967'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '65', 'city': 'nkik', 'id': '87', 'status': 'alive', 'location': 'lxan', 'name': '-', 'birthday': '01.05.2019', 'some number': '-', 'age': '58', 'birth': '06.09.1965'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': 'nrdx', 'id': '69', 'status': 'alive', 'location': 'pouw', 'name': '-', 'birthday': '-', 'some number': '62', 'age': '58', 'birth': '17.06.1965'}, {'first kiss': '-', 'death': '-', 'radius': '93', 'size': '81', 'city': 'llwx', 'id': '8', 'status': 'alive', 'location': 'krfr', 'name': 'wfyz', 'birthday': '-', 'some number': '-', 'age': '58', 'birth': '18.05.1965'}, {'first kiss': '-', 'death': '-', 'radius': '62', 'size': '-', 'city': 'oumd', 'id': '85', 'status': 'alive', 'location': 'wstq', 'name': '-', 'birthday': '23.09.1994', 'some number': '-', 'age': '58', 'birth': '14.11.1964'}, {'first kiss': '05.09.1974', 'death': '-', 'radius': '97', 'size': '94', 'city': 'ldwa', 'id': '83', 'status': 'alive', 'location': 'ggpc', 'name': 'mumr', 'birthday': '-', 'some number': '96', 'age': '59', 'birth': '10.09.1964'}, {'first kiss': '04.04.1964', 'death': '-', 'radius': '80', 'size': '96', 'city': 'kvex', 'id': '78', 'status': 'alive', 'location': '-', 'name': 'jvke', 'birthday': '-', 'some number': '52', 'age': '60', 'birth': '22.06.1963'}, {'first kiss': '17.12.1951', 'death': '-', 'radius': '29', 'size': '-', 'city': 'zonx', 'id': '44', 'status': 'alive', 'location': 'fmll', 'name': 'wyxf', 'birthday': '-', 'some number': '86', 'age': '60', 'birth': '10.12.1962'}, {'first kiss': '-', 'death': '-', 'radius': '39', 'size': '47', 'city': 'ezqo', 'id': '88', 'status': 'alive', 'location': '-', 'name': 'duxb', 'birthday': '-', 'some number': '-', 'age': '63', 'birth': '16.09.1960'}, {'first kiss': '19.12.1959', 'death': '-', 'radius': '56', 'size': '100', 'city': 'jaxu', 'id': '75', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '63', 'age': '64', 'birth': '12.02.1959'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '92', 'status': 'alive', 'location': 'jmwf', 'name': 'eoya', 'birthday': '11.08.1977', 'some number': '40', 'age': '66', 'birth': '05.07.1957'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '86', 'status': 'alive', 'location': 'qteq', 'name': 'wtwr', 'birthday': '25.05.1931', 'some number': '-', 'age': '66', 'birth': '21.03.1957'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '58', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '68', 'birth': '01.10.1955'}, {'first kiss': '14.06.2018', 'death': '-', 'radius': '-', 'size': '-', 'city': 'evgk', 'id': '40', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '24', 'age': '69', 'birth': '20.09.1954'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '87', 'city': '-', 'id': '63', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '70', 'birth': '04.12.1952'}, {'first kiss': '26.10.1952', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '45', 'status': 'alive', 'location': 'upxh', 'name': 'gauk', 'birthday': '-', 'some number': '20', 'age': '73', 'birth': '14.07.1950'}, {'first kiss': '-', 'death': '-', 'radius': '7', 'size': '-', 'city': 'qqdz', 'id': '49', 'status': 'alive', 'location': 'tzwx', 'name': '-', 'birthday': '05.02.1983', 'some number': '35', 'age': '73', 'birth': '03.01.1950'}, {'first kiss': '24.02.1992', 'death': '-', 'radius': '-', 'size': '96', 'city': '-', 'id': '15', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '74', 'birth': '26.03.1949'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': 'xrkq', 'id': '20', 'status': 'alive', 'location': 'ohat', 'name': 'zljx', 'birthday': '24.04.1979', 'some number': '72', 'age': '75', 'birth': '02.07.1948'}, {'first kiss': '23.07.1943', 'death': '-', 'radius': '52', 'size': '-', 'city': '-', 'id': '12', 'status': 'alive', 'location': '-', 'name': 'xexi', 'birthday': '-', 'some number': '33', 'age': '76', 'birth': '13.05.1947'}, {'first kiss': '28.08.1945', 'death': '-', 'radius': '-', 'size': '-', 'city': '-', 'id': '68', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '19.10.1933', 'some number': '87', 'age': '78', 'birth': '02.06.1945'}, {'first kiss': '-', 'death': '-', 'radius': '4', 'size': '-', 'city': '-', 'id': '64', 'status': 'alive', 'location': '-', 'name': 'xjjr', 'birthday': '17.09.1979', 'some number': '-', 'age': '79', 'birth': '05.05.1944'}, {'first kiss': '-', 'death': '-', 'radius': '93', 'size': '3', 'city': 'vaxo', 'id': '17', 'status': 'alive', 'location': '-', 'name': 'rhsn', 'birthday': '-', 'some number': '6', 'age': '79', 'birth': '16.01.1944'}, {'first kiss': '09.02.1936', 'death': '-', 'radius': '-', 'size': '8', 'city': 'igqa', 'id': '25', 'status': 'alive', 'location': 'jjjg', 'name': 'khgu', 'birthday': '-', 'some number': '-', 'age': '83', 'birth': '27.09.1940'}, {'first kiss': '25.06.1941', 'death': '-', 'radius': '-', 'size': '97', 'city': 'kvuk', 'id': '3', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '09.01.1934', 'some number': '-', 'age': '86', 'birth': '15.01.1937'}, {'first kiss': '-', 'death': '-', 'radius': '73', 'size': '-', 'city': '-', 'id': '89', 'status': 'alive', 'location': 'teyf', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '87', 'birth': '26.03.1936'}, {'first kiss': '27.04.2018', 'death': '-', 'radius': '42', 'size': '57', 'city': '-', 'id': '16', 'status': 'alive', 'location': 'wsuh', 'name': '-', 'birthday': '-', 'some number': '-', 'age': '87', 'birth': '20.03.1936'}, {'first kiss': '-', 'death': '-', 'radius': '2', 'size': '61', 'city': 'pprx', 'id': '57', 'status': 'alive', 'location': 'fdmc', 'name': 'hsip', 'birthday': '03.04.2004', 'some number': '10', 'age': '88', 'birth': '28.11.1934'}, {'first kiss': '-', 'death': '-', 'radius': '7', 'size': '85', 'city': '-', 'id': '60', 'status': 'alive', 'location': 'gwum', 'name': 'ifrd', 'birthday': '-', 'some number': '43', 'age': '88', 'birth': '25.11.1934'}, {'first kiss': '23.08.1999', 'death': '-', 'radius': '-', 'size': '-', 'city': 'cdmk', 'id': '31', 'status': 'alive', 'location': '-', 'name': '-', 'birthday': '25.05.2003', 'some number': '84', 'age': '91', 'birth': '21.06.1932'}, {'first kiss': '12.10.2007', 'death': '-', 'radius': '-', 'size': '82', 'city': '-', 'id': '77', 'status': 'alive', 'location': '-', 'name': 'mfmq', 'birthday': '-', 'some number': '-', 'age': '91', 'birth': '24.05.1932'}, {'first kiss': '22.06.1984', 'death': '-', 'radius': '-', 'size': '50', 'city': 'ahva', 'id': '84', 'status': 'alive', 'location': 'eget', 'name': 'jmxt', 'birthday': '-', 'some number': '-', 'age': '93', 'birth': '22.09.1930'}, {'first kiss': '12.07.1975', 'death': '-', 'radius': '5', 'size': '43', 'city': '-', 'id': '18', 'status': 'alive', 'location': 'kzoc', 'name': 'jbpd', 'birthday': '-', 'some number': '58', 'age': '93', 'birth': '15.06.1930'}, {'first kiss': '-', 'death': '-', 'radius': '-', 'size': '-', 'city': 'tobj', 'id': '62', 'status': 'alive', 'location': '-', 'name': 'tytq', 'birthday': '17.06.1976', 'some number': '-', 'age': '93', 'birth': '03.03.1930'}]
# with open('report_1', 'w', newline='') as file:
#     fieldnames = report_data[0].keys()
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(report_data)
