"""Beat the odds."""
import collections
import re


def read_words(filename: str) -> dict:
    """
    Read words from file into dictionary.

    Read file and return dictionary
    where keys represent words
    and values represent the count of the given word.

    Each word is on a separate line.
    :param filename: File to read
    :return: Dictionary of word counts
    """
    dict = collections.defaultdict(int)
    with open(filename, 'r') as fail:
        for line in fail:
            word = line.strip()
            dict[word] += 1
    return dict


def guess(sentence: str, guessed_letters: list, word_dict: dict) -> str:
    """
    Offer the letter which would most probably give the best result.

    The goal of the game is to guess the sentence.
    The sentence is revealed by revealing letters.
    The player guesses a letter, if the letter
    exists in the sentence, all the given letters
    are revealed. The sentence is revealed when all
    the letters are revealed.

    The function should take into account possible
    words from word_dict parameter. The sentence is
    combined using the words from the dictionary and
    spaces between words.

    The sentence parameter represents the sentence
    to be guessed. The value consists of letters,
    spaces ( ) and underscores (_). Space represents
    the space between the words. Underscore indicates
    a letter which has to be guessed. Letter itself
    represents already guessed and revealed letters.

    In addition, the function takes guessed_letters
    parameter which indicates already guessed letters
    which are not in the sentence.

    The best guess is the letter which would have the
    highest probability to reveal letters in the sentence.
    It doesn't matter how many letters will be reveled,
    the function should take into account the probability
    that at least one letter would be revealed.

    Some examples:
    format:
    x)
    correct sentence
    sentence given to the function
    guessed_letters given to the function
    word_dict given to the function

    1)
    hi
    __
    []
    {"hi": 1}

    If the whole sentence is "hi" (one word)
    it is represented as "__".
    If the dictionary consists of only one word "hi",
    then the probability that "h" or "i" would reveal
    at least one letter is 100% for both.

    2)
    hi
    __
    []
    {"hi": 1, "he": 1}
    probabilities:
    h: 100%
    i: 50%
    e: 50%

    3)
    hi
    __
    []
    {"hi": 1, "he": 1, "so": 1}
    probs:
    h: 66%
    i: 33%
    e: 33%
    s: 33%
    o: 33%

    4)
    hi
    __
    []
    {"hi": 1, "he": 3, "so": 1}
    probs:
    h: 80% (4 cases out of 5)
    e: 60% (3 / 5)
    rest 20% (1 / 5)

    5)
    so fun
    __ ___
    {'this': 2, 'is':2, 'he': 3, 'so': 1, 'fun': 1, 'sun': 2, 'far': 1}
    as we have 2 words, we will give probabilities for both words separately:
    n: 0% 75% (3 out of 4): fuN, suN, suN, far
    u: 0% 75% the same
    s: 50% 50% in first word: So, iS, iS, he, he, he.
               second word: Sun, Sun, fun, far
    f: 0% 50%
    h: 50% 0%
    e: 50% 0%
    i: 33% 0%
    a: 0% 25%
    r: 0% 25%
    o: 16% 0%

    6)
    thin is test
    t___ __ t__t
    ['t'] - 't' is already guessed and revealed
    {'term': 3, 'is': 1, 'of': 1, 'that': 4, 'test': 5, 'thin': 2, 'tide': 2}
    as 't' is already revealed and guessed, the words
    in the sentence cannot contain any more 't' letters.
    The first word can be: term, thin, tide (others have another t)
    the hird word can be: that, test
    Percentages:
    e: 71% 0% 55%
    i: 57% 50% 0%
    s: 0% 50% 55%
    f: 0% 50% 0%
    ....

    :param sentence: Sentence to be guessed.
    :param guessed_letters: A list of already guessed letters
    (both revealed and not existing letters).
    :param word_dict: A dictionary of words and their counts.
    Use the output from read_words.
    :return: The letter with the best probability.
    """
    letter_probabilities = {}

    # Создаем регулярное выражение для поиска слов в предложении
    word_pattern = re.compile(r'\b\w+\b')

    # Разбиваем угадываемое предложение на слова
    words_in_sentence = re.findall(word_pattern, sentence)

    for word in words_in_sentence:
        # Проверяем, есть ли это слово в словаре
        if word in word_dict:
            word_length = len(word)
            word_count = word_dict[word]

            for letter in word:
                # Проверяем, не угадана ли уже данная буква
                if letter not in guessed_letters:
                    # Вычисляем вероятность буквы в данном слове
                    letter_probability = int(1 / (word_length * word_count) * 100)

                    # Добавляем вероятность буквы в словарь
                    if letter in letter_probabilities:
                        letter_probabilities[letter] += letter_probability
                    else:
                        letter_probabilities[letter] = letter_probability
    if letter_probabilities:
        best_letter = max(letter_probabilities, key=letter_probabilities.get)
        return best_letter
    else:
        return ''



if __name__ == "__main__":
    sentence = 'hi this is me'
    filename = 'wordlist.txt'
    x = {'hi': 1}
    guessed_letters = ['h']
    print(guess(sentence, guessed_letters, x))
