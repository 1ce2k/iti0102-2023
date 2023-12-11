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
        for line in data_list[1:]:
            new_dict = {
                'date': datetime.datetime.strptime(line[0], '%Y-%m-%d'),
                'book': line[1],
                'user': line[2],
                'action': line[3]
            }
            self.data.append(new_dict)

    def get_borrower_names(self):
        borrower_names = []
        for line in self.data:
                if line['user'] not in borrower_names:
                    borrower_names.append(line['user'])
        return borrower_names

    def get_book_titles(self):
        books = []
        for line in self.data:
            if line['book'] not in books:
                books.append(line['book'])
        return books

    def get_total_transactions(self):
        return len(self.data)


class Controller:
    pass


if __name__ == "__main__":
    library = LibraryStats('example.csv')
    print(library.data)
    print(library.get_borrower_names())
    print(library.get_book_titles())