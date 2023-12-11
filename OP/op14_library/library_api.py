import datetime


class User:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        if isinstance(book, Book) and book not in self.books:
            self.books.append(book)

class Book:
    def __init__(self):
        pass


class LibraryStat:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                parts = line.split(';')
                date = datetime.datetime.strptime(parts[0], '%Y-%M-%D')
                book_name = parts[1]
                user_name = parts[2]
                action = parts[3]
                info = {date, book_name, user_name, action}
                self.data.append(info)

    def get_borrower_names(self):
        ret = []
        for line in self.data:
            if line['action'] == 'borrow':
                ret.append(line['user_name'])
        return ret
