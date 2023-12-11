import csv
import datetime


class LibraryStats:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'r', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            data_list = []
            for line in reader:
                data_list.append(line)
            keys = data_list[0]
        for line in data_list[1:]:
            y = {}
            for x in range(len(keys)):
                y[keys[x]] = line[x]
                self.data.append(y)

    def get_borrower_names(self):
        borrower_names = []
        for line in self.data:
            return line
            # if line['action'] == 'laenutus':
            #     if line['user'] not in borrower_names:
            #         borrower_names.append(line['user'])
        # return borrower_names


class Controller:
    pass


if __name__ == "__main__":
    library = LibraryStats('example.csv')
    print(library.data)
    print(library.get_borrower_names())