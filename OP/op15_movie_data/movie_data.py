"""What should we watch, Honey?..."""
import pandas as pd


class MovieData:
    """
    Class MovieData.

    Here we keep the initial data and the cleaned-up aggregate dataframe.
    """

    def __init__(self):
        """
        Class initialization.

        Here we declare variables for storing initial data and a variable for storing
        an aggregate of processed initial data.
        """
        self.movies = None or pd.DataFrame
        self.ratings = None or pd.DataFrame
        self.tags = None or pd.DataFrame
        self.aggregate_movie_dataframe = None or pd.DataFrame

    def load_data(self, movies_filename: str, ratings_filename: str, tags_filename: str) -> None:
        """
        Load Data from files into dataframes.

        Raise the built-in ValueError exception if either movies_filename, ratings_filename or
        tags_filename is None.

        :param movies_filename: file path for movies.csv file.
        :param ratings_filename: file path for ratings.csv file.
        :param tags_filename: filepath for tags.csv file.
        :return: None
        """
        if movies_filename is None or ratings_filename is None or tags_filename is None:
            raise ValueError("File path cannot be empty.")

        self.movies = pd.read_csv(movies_filename)
        self.ratings = pd.read_csv(ratings_filename)
        self.tags = pd.read_csv(tags_filename)

    def create_aggregate_movie_dataframe(self, nan_placeholder: str = '') -> None:
        """
        Create an aggregate dataframe from frames self.movies, self.ratings and self.tags.

        No columns with name 'userId' or 'timestamp' allowed. Columns should be in order
        'movieId', 'title', 'genres', 'rating', 'tag'. Several lines in the tags.csv file
        with the same movieId should be joined together under the tag column.

        When created correctly, first 3 rows of the dataframe should look like below (some spaces omitted so as not
        to create a style error):
                movieId             title                                       genres  rating              tag
        0             1  Toy Story (1995)  Adventure|Animation|Children|Comedy|Fantasy     4.0  pixar pixar fun
        1             1  Toy Story (1995)  Adventure|Animation|Children|Comedy|Fantasy     4.0  pixar pixar fun
        2             1  Toy Story (1995)  Adventure|Animation|Children|Comedy|Fantasy     4.5  pixar pixar fun

        :param nan_placeholder: Value to replace all np.nan-valued elements in column 'tag'.
        :return: None
        """
        rating_temp = self.ratings.drop(labels=['userId', 'timestamp'], axis=1)
        tag_temp = self.tags.groupby(by=['movieId']).agg({'tag': lambda x: ' '.join(x)})
        result = self.movies.merge(rating_temp, on='movieId', how='left')
        result = result.merge(tag_temp, on='movieId', how='left')
        result['tag'] = result['tag'].fillna(nan_placeholder)
        self.aggregate_movie_dataframe = result

    def get_aggregate_movie_dataframe(self):
        """
        Return aggregate_movie_dataframe variable.

        :return: pandas DataFrame
        """
        return self.aggregate_movie_dataframe

    def get_movies_dataframe(self):
        """
        Return movies dataframe.

        :return: pandas DataFrame
        """
        return self.movies

    def get_ratings_dataframe(self):
        """
        Return ratings dataframe.

        :return: pandas DataFrame
        """
        return self.ratings

    def get_tags_dataframe(self):
        """
        Return tags dataframe.

        :return: pandas DataFrame
        """
        return self.tags


class MovieFilter:
    """
    Class MovieFilter.

    Here we keep the aggregate dataframe from MovieData class and operate on that data.
    """

    def __init__(self):
        """
        Class initialization.

        Here we only need to store the aggregate dataframe from MovieData class for now.
        For OP part, some more variables might be a good idea here.
        """
        self.movie_data = None or pd.DataFrame
        self.average_rating = 0
        self.median_rating = 0

    def set_movie_data(self, movie_data: pd.DataFrame) -> None:
        """
        Set the value of self.movie_data to be given argument movie_data.

        :param movie_data: pandas DataFrame object
        :return: None
        """
        self.movie_data = movie_data

    #  -> pd.DataFrame | None
    def filter_movies_by_rating_value(self, rating: float, comp: str):
        """
        Return pandas DataFrame of self.movie_data filtered according to rating and comp string value.

        Raise the built-in ValueError exception if rating is None or < 0.
        Raise the built-in ValueError exception if comp is not 'greater_than', 'equals' or 'less_than'.

        :param rating: value for comparison operation to compare to
        :param comp: string representation of the comparison operation
        :return: pandas DataFrame object of the filtration result
        """
        if rating is None or rating < 0:
            raise ValueError("Enter rating.")

        if comp is None or comp not in {'greater_than', 'equals', 'less_than'}:
            raise ValueError("Enter valid comp.")

        df = self.movie_data
        if comp == 'equals':
            return df[df['rating'].astype(float) == float(rating)]
        elif comp == 'less_than':
            return df[df['rating'].astype(float) < float(rating)]
        elif comp == 'greater_than':
            return df[df['rating'].astype(float) > float(rating)]

    def filter_movies_by_genre(self, genre: str) -> pd.DataFrame:
        """
        Return a pandas DataFrame of self.movie_data filtered by parameter genre.

        Only rows where the given genre is in column 'genres' should be in the result.
        Operation should be case-insensitive.

        Raise the built-in ValueError exception if genre is an empty string or None.

        :param genre: string value to filter by
        :return: pandas DataFrame object of the filtration result
        """
        if genre is None:
            raise ValueError("Enter genre.")

        df = self.movie_data
        return df[df['genres'].str.lower().str.contains(genre.lower())]

    def filter_movies_by_tag(self, tag: str) -> pd.DataFrame:
        """
        Return a pandas DataFrame of self.movie_data filtered by parameter tag.

        Only rows where the given tag is in column 'tag' should be left in the result.
        Operation should be case-insensitive.

        Raise the built-in ValueError exception if tag is an empty string or None.

        :param tag: string value tu filter by
        :return: pandas DataFrame object of the filtration result
        """
        if tag is None:
            raise ValueError("Enter tag.")

        df = self.movie_data
        res = df[df['tag'].str.lower().str.contains(tag.lower())]
        return res

    def filter_movies_by_year(self, year: int) -> pd.DataFrame:
        """
        Return a pandas DataFrame of self.movie_data filtered by year of release.

        Only rows where the year of release matches given parameter year should be left in the result.

        Raise the built-in ValueError exception if year is None or < 0.

        :param year: integer value of the year to filter by
        :return: pandas DataFrame object of the filtration result
        """
        if year is None or year < 0:
            raise ValueError("Enter valid year.")
        df = self.movie_data
        df['year'] = df['title'].str.extract(r'\((\d{4})\)')
        filtered = df[df['year'].astype(float) == float(year)]
        return filtered.drop(labels='year', axis=1)

    def get_decent_movies(self) -> pd.DataFrame:
        """
        Return all movies with a rating of at least 3.0.

        :return: pandas DataFrame object of the search result
        """
        return self.filter_movies_by_rating_value(2.9, 'greater_than')

    def get_decent_comedy_movies(self):
        """
        Return all movies with a rating of at least 3.0 and where genre is 'Comedy'.

        :return: pandas DataFrame object of the search result
        """
        df = self.movie_data
        return df[(df['rating'].astype(float) >= 3.0) & (df['genres'].str.lower().str.contains('comedy'))]

    #  -> pd.DataFrame | None
    def get_decent_children_movies(self):
        """
        Return all movies with a rating of at least 3.0 and where genre is 'Children'.

        :return: pandas DataFrame object of the search result
        """
        df = self.movie_data
        return df[(df['rating'].astype(float) >= 3.0) & (df['genres'].str.lower().str.contains('children'))]

    def get_median_rating(self):
        """
        Return self.median_rating.

        :return: float value of the median rating for all entries in self.movie_data
        """
        return self.median_rating

    def get_average_rating(self):
        """
        Return self.average_rating.

        :return: float value of the average rating for all entries in self.movie_data
        """
        return self.average_rating

    def calculate_rating_statistics(self):
        """
        Calculate median and average ratings for all entries in self.movie_data, rounded to three decimal places.

        Store results in self.median_rating and self.average_rating
        :return:
        """
        df = self.movie_data
        median = df['rating'].median()
        average = df['rating'].mean()
        median_rating = round(median, 3)
        average_rating = round(average, 3)
        self.median_rating = median_rating
        self.average_rating = average_rating

    def get_movies_above_average_by_genre(self, genre: str) -> pd.DataFrame:
        """
        Return all movies with the given genre where the rating is above the calculated self.average_rating value. Search is case-insensitive.

        If genre is an empty string or None, raise ValueError.

        :param genre: string value to filter by
        :return: pandas DataFrame object of the search result
        """
        if genre is None:
            raise ValueError("Enter valid genre.")
        df = self.movie_data
        return df[(df['rating'].astype(float) > self.average_rating) & (df['genres'].str.lower().str.contains(genre.lower()))]

    def calculate_mean_rating_for_every_movie(self) -> pd.DataFrame:
        """
        Return a new DataFrame where there is only one line per unique movie and the rating of every movie is the mean rating of all the individual ratings for that movie in self.movie_data, rounded to three decimal places.

        If the mean rating value is NaN, it should be dropped from the result.

        :return: pandas DataFrame object
        """
        pass

    def get_top_movies_by_genre(self, genre: str, n: int = 3) -> pd.DataFrame:
        """
        Return the top n best rated movies with the given genre. Search is case-insensitive.

        If genre is an empty string or None of if n is negative, a ValueError should be raised.

        :param genre: string value to filter by
        :param n: number of best rated movies to include in the result
        :return: pandas DataFrame object of the search result
        """
        pass

    def get_best_movie_by_year_genre_and_tag(self, year: int, genre: str, tag: str) -> pd.DataFrame:
        """
        Return the best rated movie with given year of release, genre and tag. Search is case-insensitive.

        If year is negative, a ValueError should be raised.
        If either tag or genre is an empty string or None, a ValueError should be raised.

        :param year: integer value to filter by
        :param genre: string value to filter by
        :param tag: string value to filter by
        :return: pandas DataFrame object of the search result
        """
        pass


if __name__ == '__main__':
    # this pd.option_context menu is for better display purposes
    # in terminal when using print. Keep these settings the same
    # unless you wish to display more than 10 rows
    with pd.option_context('display.max_rows', 10,
                           'display.max_columns', 5,
                           'display.width', 200):
        my_movie_data = MovieData()
        my_movie_data.load_data("movies.csv", "ratings.csv", "tags.csv")
        my_movie_data.create_aggregate_movie_dataframe('--empty--')
        my_movie_filter = MovieFilter()
        my_movie_filter.set_movie_data(my_movie_data.get_aggregate_movie_dataframe())
        my_movie_filter.calculate_rating_statistics()
        print(my_movie_filter.average_rating)
        print(my_movie_filter.median_rating)
