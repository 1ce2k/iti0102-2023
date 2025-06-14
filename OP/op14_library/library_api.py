"""OP 14."""
import csv
import re


class LibraryStats:
    """Library Stats class."""

    def __init__(self, filename):
        """Read file to dict."""
        self.data = []
        with open(filename, 'r', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            data_list = []
            for line in reader:
                data_list.append(line)
        for line in data_list:
            new_dict = {
                'date': line[0],
                'book': line[1],
                'user': line[2],
                'action': line[3]
            }
            self.data.append(new_dict)

    def get_borrower_names(self):
        """Return list of borrower names."""
        borrower_names = []
        for line in self.data:
            if line['user'] not in borrower_names:
                borrower_names.append(line['user'])
        return borrower_names

    def get_book_titles(self):
        """Return list of book titles."""
        books = []
        for line in self.data:
            if line['book'] not in books:
                books.append(line['book'])
        return books

    def get_total_transactions(self):
        """Return count of al transactions."""
        return len(self.data)

    def get_total_borrows_of_book(self, book_name):
        """Return how often book was borrowed."""
        count = 0
        for line in self.data:
            if line['book'] == book_name and line['action'] == 'laenutus':
                count += 1
        return count

    def get_total_borrows_by(self, username):
        """Return how often user borrows."""
        count = 0
        for line in self.data:
            if line['user'] == username and line['action'] == 'laenutus':
                count += 1
        return count

    def get_favourite_book(self, username):
        """Return users favourite book."""
        books = {}
        for line in self.data:
            if line['user'] == username and line['action'] == 'laenutus':
                if line['book'] not in books:
                    books[line['book']] = 0
                books[line['book']] += 1
        return max(books.keys(), key=books.get)

    def get_borrow_history(self, username):
        """Return user borrow history."""
        history = []
        for line in self.data:
            if line['user'] == username and line['action'] == 'laenutus':
                history.append(line['book'])
        return history

    def get_most_frequent_borrower(self, book_name):
        """Return most book frequent borrower."""
        users = {}
        for line in self.data:
            if line['book'] == book_name and line['action'] == "laenutus":
                if line['user'] not in users:
                    users[line['user']] = 0
                users[line['user']] += 1
        return max(users.keys(), key=users.get)

    def get_current_status(self, book_name):
        """Return book status."""
        book_data = []
        for line in self.data:
            if line['book'] == book_name:
                book_data.append(line)
        if book_data[-1]['action'] == 'laenutus':
            return 'laenatud'
        else:
            return 'tagastatud'

    def get_borrow_dates(self, book_name):
        """Return list of dates when book was borrowed."""
        dates = []
        for line in self.data:
            if line['book'] == book_name and line['action'] == 'laenutus':
                dates.append(line['date'])
        return dates


class Controller:
    """Controller class."""

    def __init__(self, librarystats: LibraryStats):
        """Init controller."""
        self.library = librarystats

    def get(self, path):
        """Return valid method from librarystats."""
        if path == '/books':
            return self.library.get_book_titles()
        elif path == '/borrowers':
            return self.library.get_borrower_names()
        elif path == '/total':
            return self.library.get_total_transactions()
        elif re.search(r'/book/([A-ZÜÕÖÄa-züõöä\d-]+)/', path) is not None:
            return self.get_data_per_book(path)
        # return path
        elif re.search(r'/borrower/([A-ZÜÕÖÄa-züõöä\d-]+)/', path) is not None:
            return self.get_data_per_user(path)

    def get_data_per_book(self, path):
        """Help func."""
        book = re.search(r'/book/([A-ZÜÕÖÄa-züõöä\d-]+)/', path).group(1)
        if path == f'/book/{book}/borrows':
            return self.library.get_total_borrows_of_book(book)
        elif path == f'/book/{book}/most-frequent-borrower':
            return self.library.get_most_frequent_borrower(book)
        elif path == f'/book/{book}/borrow-dates':
            return self.library.get_borrow_dates(book)
        elif path == f'/book/{book}/current-status':
            return self.library.get_current_status(book)

    def get_data_per_user(self, path):
        """Help func."""
        # return path
        user = re.search(r'/borrower/([A-ZÜÕÖÄa-züõöä\d-]+)/', path).group(1)
        if path == f'/borrower/{user}/total-borrows':
            return self.library.get_total_borrows_by(user)
        elif path == f'/borrower/{user}/favourite-book':
            return self.library.get_favourite_book(user)
        elif path == f'/borrower/{user}/borrow-history':
            return self.library.get_borrow_history(user)


if __name__ == "__main__":
    library = LibraryStats('example.csv')
    print(library.data)
