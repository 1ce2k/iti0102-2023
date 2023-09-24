"""Play best the odds game."""


import collections
import random
from heapq import nlargest


def the_game(filename, word_count):
    """Play the game."""
    d = read_words(filename)
    c = collections.Counter(d)
    dictionary_size = sum(c.values())
    correct_sentence = " ".join([x for _, x in nlargest(word_count, ((random.random(), x) for x in c.elements()))])
    sentence = "".join([x if x == ' ' else '_' for x in correct_sentence])
    guessed_letters = []
    print("Correct sentence: " + correct_sentence)
    print(sentence)
    cnt = 0
    while True:
        guessed_letter = guess(sentence, guessed_letters, d)
        if guessed_letter is None or guessed_letter in guessed_letters:
            print("Nothing to guess any more, breaking.")
            break
        print('guessed:' + guessed_letter)
        guessed_letters.append(guessed_letter)
        sentence = "".join([c if c == guessed_letter else sentence[i] for i, c in enumerate(correct_sentence)])
        print("Sentence: " + sentence)
        cnt += 1
        if '_' not in sentence:
            print("Congrats! Number of guesses:" + str(cnt))
            break


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


def guess(sentence: str, guessed_letters: list, word_dict: dict):
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
    the third word can be: that, test
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
    # split the sentence to parts
    words = sentence.split(' ')

    # find all possible words to sentence part
    possible_words_to_part = []
    for word in words:
        possible_words_to_part.append(filter_words_by_pattern(word, guessed_letters, word_dict))

    # Find best letters for each sentence part
    best_letters_list = []
    for i in range(len(words)):
        letter = find_letter_probability(possible_words_to_part[i], guessed_letters)
        best_letters_list.append(letter)

    # Merge best letter to one dict using the max value
    best_letters_dict = {}
    for d in best_letters_list:
        for key, value in d.items():
            if key not in best_letters_dict or value > best_letters_dict[key]:
                best_letters_dict[key] = value
    if best_letters_dict:
        best_letter = max(best_letters_dict, key=best_letters_dict.get)
        return best_letter
    return None


def filter_words_by_pattern(pattern: str, letters_to_keep: list, word_dict: dict) -> dict:
    """Find all possible words for the guess from dictionary."""
    filtered_dict = {}
    for word, count in word_dict.items():
        if len(word) == len(pattern):
            if all((p == '_' or p == w) for p, w in zip(pattern, word)):
                if all((letter in word or letter == '_') for letter in pattern):
                    if all(word.count(let) == pattern.count(let) for let in letters_to_keep):
                        filtered_dict[word] = count
    return filtered_dict


def find_letter_probability(word_dict: dict, guessed_letters: list) -> dict:
    """Return best letter for sentence part."""
    # list_of_words = []
    # for key in word_dict.keys():
    #     for i in range(word_dict[key]):
    #         list_of_words.append(key)
    frequency = {}
    for word, count in word_dict.items():
        for letter in word:
            if letter not in guessed_letters:
                for letter in word:
                    if letter not in guessed_letters:
                        frequency[letter] = frequency.get(letter, 0) + 1
    probabilities = {}
    total_letters = 0
    for value in word_dict.values():
        total_letters += value
    if frequency:
        for key in frequency.keys():
            probabilities[key] = int(frequency[key] / total_letters * 100)
    if probabilities:
        max_value = max(probabilities.values())
        max_key = [key for key, value in probabilities.items() if value == max_value][0]
        best_letter = {max_key: max_value}
        return best_letter
    return {}
