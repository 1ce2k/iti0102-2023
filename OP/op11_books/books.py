"""Books."""


class Book:
    """Book class."""

    def __init__(self, title: str, author: str, pages: int, sales: int, genres: list[str], publication_year: int):
        """
        Initialize a Book object.

        :param title: The title of the book.
        :param author: The author of the book.
        :param pages: The amount of pages in the book.
        :param sales: The amount of times the book has been sold.
        :param genres: The genres of the book.
        :param publication_year: The year the book was published.
        """
        self.title = title
        self.author = author
        self.pages = pages
        self.sales = sales
        self.genres = genres
        self.year = publication_year

    def __eq__(self, other) -> bool:
        """Return True if the Book objects are equal."""
        return type(other) is self.__class__ and \
            self.title == other.title and \
            self.author == other.author and \
            self.pages == other.pages and \
            self.sales == other.sales and \
            self.genres == other.genres and \
            self.year == other.year

    def __hash__(self) -> int:
        """Allow a Book object to be used as a key in a dictionary. Don't change this method."""
        return hash((self.title, self.author, self.pages, self.sales, tuple(self.genres), self.year))

    def __repr__(self) -> str:
        """Return a string representation of the Book object."""
        return f'"{self.title}" by {self.author}'


def author_book_count(library: list[Book], author: str) -> int:
    """
    Find the number of books written by the given author.

    :param library: The list of books to search through.
    :param author: The given author.
    :return: The amount of books written by the author.
    """
    count = 0
    for book in library:
        if book.author == author:
            count += 1
    return count


def author_page_count(library: list[Book], author: str) -> int:
    """
    Find the total number of pages written by the given author.

    :param library: The list of books to search through.
    :param author: The given author.
    :return: The total number of pages written by the author.
    """
    pages = 0
    for book in library:
        if book.author == author:
            pages += book.pages
    return pages


def most_popular_book(library: list[Book]) -> Book:
    """
    Find the book with the most sales.

    :param library: The list of books.
    :return: The Book object with the most sales.
    """
    all_sales = {}
    for book in library:
        all_sales[book] = book.sales
    return max(all_sales, key=all_sales.get)


def most_popular_author(library: list[Book]) -> str:
    """
    Find the author with the most sales.

    If two or more authors have the same amount of sales, it doesn't matter which one is returned.

    :param library: The list of books.
    :return: The author with the most sales.
    """
    all_authors = {}
    for book in library:
        if book.author not in all_authors:
            all_authors[book.author] = book.sales
        else:
            all_authors[book.author] += book.sales
    return max(all_authors, key=all_authors.get)


def average_author_book_length(library: list[Book], author: str) -> float:
    """
    Find the average length of a book (amount of pages), that is written by the given author.

    :param library: The list of books.
    :param author: The given author.
    :return: The average length of the author's books.
    """
    pages = author_page_count(library, author)
    books = author_book_count(library, author)
    return pages / books


def find_best_selling_genre(library: list[Book]) -> str:
    """
    Find the genre, that has the most sales. If two or more genres have the same amount of sales, return either one.

    :param library: The list of books.
    :return: The genre with the most total sales.
    """
    genres = {}
    for book in library:
        for genre in book.genres:
            if genre not in genres:
                genres[genre] = 0
            genres[genre] += book.sales
    return max(genres, key=genres.get)


def find_books_by_genre_and_year(library: list[Book], genre: str, year: int) -> list[Book]:
    """
    Find all books in the given list, that match the given year and genre.

    For the genre, you should check if the given genre is contained in the list of genres of the book.
    The result should be sorted by sales (descending) and if two or more books have the same sales,
    then sort them by title (alphabetically).

    :param library: The list of books to search from.
    :param genre: The genre to search for.
    :param year: The year to search for.
    :return: A list of books, that match the given genre and year, sorted by sales (descending) and title (alphabetically).
    """
    books = []
    for book in library:
        if book.year == year and genre in book.genres:
            books.append(book)
    ret = sorted(books, key=lambda x: (-x.sales, x.title))
    return ret


def most_popular_author_per_century(library: list[Book]) -> dict[int, str]:
    """
    Find the author with the most sales for each century.

    If two or more authors have the same amount of sales, it doesn't matter which one is returned in the dictionary.

    :param library: The list of books.
    :return: A dictionary, where the keys are the centuries and the values are the authors with the most sales in that
    century.
    """
    books_per_century = {}

    for book in library:
        century = century_from_year(book.year)
        if century not in books_per_century:
            books_per_century[century] = []
        books_per_century[century].append(book)
    print(books_per_century)
    most_popular_authors = {}
    for century in books_per_century.keys():
        most_popular_authors[century] = most_popular_author(books_per_century[century])
    return most_popular_authors


def century_from_year(year):
    """Find century."""
    return (year - 1) // 100 + 1


def correct_titles_and_count_books(library: list[Book]) -> dict[Book, int]:
    """
    Due to an unknown error, some of the titles in the given list of books have a letter missing.

    Your task is to correct the titles of the Book objects in the list and return a dictionary,
    where the Book objects are the keys and their occurrences in the list are the values.
    You should correct the book's title, if there is another book in the list,
    that has the exact same attributes, except for the title, which has a missing letter.

    For example, if the list of books has the following books:
    Book("The Great Gatsby", "F. Scott Fitzgerald", 218, 100_000, ["Classic", "Fiction"], 1925)
    Book("The Great Gatsb", "F. Scott Fitzgerald", 218, 100_000, ["Classic", "Fiction"], 1925)
    Book("Tender Is the Night", "F. Scott Fitzgerald", 320, 90_000, ["Classic", "Fiction"], 1934)
    Book("Tender Is the Nigh", "F. Scott Fitzgerald", 321, 90_000, ["Classic", "Fiction"], 1934)

    Then the second book's title should be corrected to "The Great Gatsby", while the fourth book's title should
    remain the same, because "Tender Is the Night" has a different amount of pages.

    :param library: The list of books.
    :return: The amount of books in the list.
    """
    books_dict = {}
    books_by_title_length = sorted(library, key=lambda x: -len(x.title))
    # print(books_by_title_length)
    while books_by_title_length:
        first = books_by_title_length[0]
        matching_books = [book for book in books_by_title_length if only_name_difference(first, book)]

        count = len(matching_books) + 1
        if first in books_dict:
            books_dict[first] += count
        else:
            books_dict[first] = count
        books_by_title_length.remove(first)
        for book in matching_books:
            books_by_title_length.remove(book)
    return books_dict


def only_name_difference(book1: Book, book2: Book) -> bool:
    """Return whether different is only title or not."""
    book1_chars = chars_in_str(book1.title)
    book2_chars = chars_in_str(book2.title)
    chars_dif_is_one = chars_different(book1_chars, book2_chars) == 1
    len_dif_is_one = abs(len(book1.title) - len(book2.title)) == 1

    title_matches = chars_dif_is_one and len_dif_is_one
    same_author = book1.author == book2.author
    same_pages_count = book1.pages == book2.pages
    same_sales = book1.sales == book2.sales
    same_year = book1.year == book2.year
    same_genres = book1.genres == book2.genres
    return title_matches and same_author and same_pages_count and same_sales and same_year and same_genres


def chars_in_str(s: str):
    """Count all chars in title."""
    chars = {}
    for x in s:
        if x not in chars:
            chars[x] = 1
        else:
            chars[x] += 1
    return chars


def chars_different(dict1: dict, dict2: dict) -> int:
    """Find how many chars are different."""
    differences = dict1
    for key in dict2:
        if key in differences:
            differences[key] = abs(differences[key] - dict2[key])
        else:
            differences[key] = dict2[key]
        if differences[key] == 0:
            del differences[key]
    if not differences:
        return 0
    return sum(differences.values())


if __name__ == '__main__':
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", 218, 100_000, ["Classic", "Fiction"], 1925)
    book2 = Book("Tender Is the Night", "F. Scott Fitzgerald", 320, 90_000, ["Classic", "Fiction"], 1934)
    book3 = Book("The Beautiful and Damned", "F. Scott Fitzgerald", 348, 120_000, ["Classic", "Fiction"], 1922)
    book4 = Book("To Kill a Mockingbird", "Harper Lee", 324, 80_000, ["Fiction"], 1960)
    book5 = Book("Go Set a Watchman", "Harper Lee", 278, 70_000, ["Fiction"], 2015)
    book6 = Book("In Cold Blood", "Harper Lee", 368, 110_000, ["True Crime"], 1966)
    book7 = Book("1984", "George Orwell", 328, 200_000, ["Dystopian", "Fiction"], 1949)
    book8 = Book("Animal Farm", "George Orwell", 144, 70_000, ["Satire", "Fiction"], 1945)
    book9 = Book("Nineteen Eighty-Four", "George Orwell", 328, 95_000, ["Dystopian", "Fiction"], 1949)
    book10 = Book("Pride and Prejudice", "Jane Austen", 432, 85_000, ["Classic", "Romance"], 1813)

    book_list: list[Book] = [book1, book2, book3, book4, book5, book6, book7, book8, book9, book10]
    #
    # print(author_book_count(book_list, "Harper Lee"))  # 3
    # print(author_page_count(book_list, "Harper Lee"))  # 970
    # print(author_book_count(book_list, "Willy Wonka"))  # 0
    # print(author_page_count(book_list, "Walter White"))  # 0
    # print()
    #
    # print(most_popular_book(book_list))  # "1984" by George Orwell
    # print(most_popular_author(book_list))  # George Orwell
    # print(average_author_book_length(book_list, "Harper Lee"))  # 323.3333333333333
    # print()
    #
    # print(find_best_selling_genre(book_list))  # Fiction
    # print(find_books_by_genre_and_year(book_list, "Fiction", 1949))  # ["1984" by George Orwell, "Nineteen Eighty-Four" by George Orwell]
    print(most_popular_author_per_century(book_list))  # {19: 'Jane Austen', 20: 'George Orwell', 21: 'Harper Lee'}
    # print()

    # print(correct_titles_and_count_books([
    #     Book("The Great Gatsby", "F. Scott Fitzgerald", 218, 100_000, ["Classic", "Fiction"], 1925),
    #     Book("The Great Gatsb", "F. Scott Fitzgerald", 218, 100_000, ["Classic", "Fiction"], 1925),
    #     Book("Tender Is the Night", "F. Scott Fitzgerald", 320, 90_000, ["Classic", "Fiction"], 1934),
    #     Book("Tender Is the Nigh", "F. Scott Fitzgerald", 321, 90_000, ["Classic", "Fiction"], 1934)
    # ]))
    # {
    #     "The Great Gatsby" by F. Scott Fitzgerald: 2,
    #     "Tender Is the Night" by F. Scott Fitzgerald: 1,
    #     "Tender Is the Nigh" by F. Scott Fitzgerald: 1
    # }
