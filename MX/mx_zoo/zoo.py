"""A small exercise in zookeeping."""
import math
from functools import reduce


def parse_animal(animal_str: str) -> list:
    """
    Parse a string containing animal data and return a structured list.

    The input string is expected to be in the format:
    "species,scientific_name,age_up_to,weight_range,height_range,diet,habitat"

    The returned list structure is as follows:
    [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    Example:
    Input:  "African bush elephant,Loxodonta africana,70,3000-6000,2.2-4,herbivorous,savannah"
    Output: ['African bush elephant', 'Loxodonta africana', 70, [3000.0, 6000.0], [2.2, 4.0], 'herbivorous', 'savannah']

    :param animal_str: The input string containing animal data.
    :return: A list containing structured animal data.
    """
    animal_info = animal_str.split(',')
    weight = [float(animal_info[3].split('-')[0]), float(animal_info[3].split('-')[1])]
    height = [float(animal_info[4].split('-')[0]), float(animal_info[4].split('-')[1])]

    return animal_info[:2] + [int(animal_info[2]), weight, height] + animal_info[5:]


def list_species_and_scientific_names(animal_data: list) -> list:
    """
    Extract and return species' common and scientific names from the given animal data.

    The function maps through the provided list and returns a list of tuples.
    Each tuple contains the common name (species name) as the first element
    and the scientific name as the second element.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: List of structured animal data.
    :return: List of tuples, where each tuple is structured as (common_name, scientific_name).
    """
    return list(map(lambda x: (x[0], x[1]), animal_data))


def animals_starting_with(animal_data: list, letter: str) -> list:
    """
    Return a list of animals where the common name starts with the provided letter.

    For instance, if the letter is 'A', it would return animals like 'Aardvark' or 'Antelope'.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: A list containing details about multiple animals.
    :param letter: The starting letter to filter animals by.
    :return: An alphabetically sorted list of common names of animals that start with the given letter.
    """
    return list(map(lambda x: x[0], sorted(filter(lambda x: x[0][0].lower() == letter.lower(), animal_data))))


def find_how_many_pumpkins_are_needed_to_feed_animals(animal_data: list) -> int:
    """
    Calculate the number of pumpkins required to feed all herbivorous and omnivorous animals over winter.

    Assumptions:
    1. There are 2 animals of each species.
    2. Each animal consumes an average of 6% of its body weight in pumpkins daily.
    3. A pumpkin weighs 3kg.
    4. Winter lasts 90 days.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: List of structured animal data.
    :return: Total number of pumpkins needed, rounded up to the nearest whole number.
    """
    if not animal_data:
        return 0
    total = reduce(lambda x, y: x + y,
                   map(lambda x: (sum(x[3])) * 0.06 if x[5].lower() in ('herbivorous', 'omnivorous') else 0,
                       animal_data))
    return math.ceil(total * 90 / 3)


def total_noise_level(animal_data: list) -> float:
    """
    Calculate the total noise level based on the weight of all animals. There is just one animal of each species.

    The noise level for each animal is calculated as 0.01 times the average of their weight range.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: A list containing details about multiple animals.
    :return: The total noise level of all animals in the list.
    """
    if not animal_data:
        return 0
    return reduce(lambda x, y: x + y, map(lambda x: (sum(x[3]) / 2) * 0.01, animal_data))


def zoo_parade_length(animal_data: list) -> float:
    """
    Calculate the total length of a zoo parade based on the horizontal length of all animals. There is just one animal of each species.

    The length added by each animal is assumed to be equivalent to the average of their height range.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: A list containing details about multiple animals.
    :return: The total parade length of all animals in the list.
    """
    if not animal_data:
        return 0
    return reduce(lambda x, y: x + y, map(lambda x: (sum(x[4]) / 2), animal_data))


def animal_olympics_winner(animal_data: list) -> str:
    """
    Determine the winner of the Animal Olympics based on speed.

    The speed of an animal is inversely proportional to their weight; lighter animals are faster.
    The fastest animal is determined based on the average of their weight range.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: A list containing details about multiple animals.
    :return: The species name of the winning animal.
    """
    return max(animal_data, key=lambda x: 1 / (sum(x[3]) / 2))[0]


def total_feather_count(animal_data: list) -> float:
    """
    Calculate the total feather count for all animals. There is just one animal of each species.

    The feather count for each animal is calculated as 1000 times the average of their weight range.
    (Note: This is a fictional metric for the sake of this exercise.)

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: A list containing details about multiple animals.
    :return: The total feather count of all animals in the list.
    """
    if not animal_data:
        return 0
    return reduce(lambda x, y: x + y, map(lambda x: (sum(x[3]) / 2) * 1000, animal_data))


def zoo_weight_on_other_planet(animal_data: list) -> float:
    """
    Calculate the total weight of the zoo on another planet. There is just one animal of each species.

    The weight on the other planet is 50% of the Earth's weight for each animal.
    The weight used for each animal is the average of their weight range.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: A list containing details about multiple animals.
    :return: The total weight of the zoo on the other planet.
    """
    if not animal_data:
        return 0
    return reduce(lambda x, y: x + y, map(lambda x: (sum(x[3]) / 2) * 0.5, animal_data))


def sort_alphabetically_by_scientific_name(animal_data: list) -> list:
    """
    Sort animals by scientific names.

    Sort animals by their scientific names in ascending alphabetical order and return a tuple of
    (common name, scientific name) for each animal.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: List of structured animal data.
    :return: List of tuples with (common name, scientific name) sorted by scientific name.
    """
    return list(map(lambda x: (x[0], x[1]), sorted(animal_data, key=lambda x: x[1])))


def find_animals_whose_height_is_less_than(animal_data: list, height_limit: float) -> list:
    """
    Identify animals that do not exceed a specified height, considering the maximum possible height for each species.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: List of structured animal data.
    :param height_limit: Maximum height (in meters) as a float.
    :return: List of common names of animals that are shorter than the specified height limit, sorted from shortest to tallest.
    """
    return list(
        map(lambda x: x[0], sorted(filter(lambda x: x[4][1] <= height_limit, animal_data), key=lambda x: x[4][0])))


def filter_animals_based_on_diet(animal_data: list, diet: str) -> list:
    """
    Filter animals based on their dietary habits.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: List of structured animal data.
    :param diet: A string indicating the diet (e.g., "herbivorous", "carnivorous").
    :return: Alphabetically sorted list of common names of animals that match the specified diet.
    """
    return list(map(lambda x: x[0], sorted(filter(lambda x: x[5].lower() == diet.lower(), animal_data))))


def find_animal_with_longest_lifespan(animal_data: list) -> str:
    """
    Identify the animal with the longest potential lifespan.

    In the case of a tie (multiple animals with the same lifespan), the function will return the name of the first occurrence.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: List of structured animal data.
    :return: The common name of the animal with the longest lifespan.
    """
    return max(animal_data, key=lambda x: x[2])[0]


def create_animal_descriptions(animal_data: list) -> list:
    """
    Generate descriptions for each animal, suitable for display at the zoo.

    The description format is:
    "[Species name] ([Scientific name]) lives in [habitat] and its diet is [diet].
     These animals can live up to [max age] years, and they weigh between [min weight]
     kg and [max weight] kg as adults."

     Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: List of structured animal data.
    :return: List of string descriptions for each animal.
    """
    return list(map(lambda x: f"{x[0]} ({x[1]}) lives in {x[-1]} and its diet is {x[5]}. These animals can live up to {x[2]} years, and they weigh between {x[3][0]} kg and {x[3][1]} kg as adults.", animal_data))


def calculate_ecological_impact_score(animal_data: list) -> float:
    """
    Calculate a combined ecological impact score for all animals in the zoo.

    The score is calculated based on factors such as the animal's average weight, diet, and habitat.
    Each animal starts with a base score of 10. Additional factors are applied as follows:

    - Weight Factor: Adds 0.001 times the average weight of the animal to the score.
    - Diet Factor: Multiplies the score by a factor based on the diet.
      - Herbivorous: 1.2
      - Carnivorous: 1.5
      - Omnivorous: 1.3
    - Habitat Factor: Adds a fixed score based on the habitat.
      - Savannah: +5
      - Tropics: +4
      - Temperate Forest: +3
    If the habitat is not one of the ones listed above, the habitat score is considered 0.

    The final score is the sum of individual scores of all animals.

    Reminder: [species, scientific_name, age_up_to, [min_weight, max_weight], [min_height, max_height], diet, habitat]

    :param animal_data: List of structured animal data.
    :return: The total ecological impact score.
    """
    if not animal_data:
        return 0
    return reduce(lambda y, x: y + (10 + sum(x[3]) / 2 * 0.001) * {'herbivorous': 1.2, 'carnivorous': 1.5, 'omnivorous': 1.3}.get(x[5].lower(), 1) + {'savannah': 5, 'tropics': 4, 'temperate forest': 3}.get(x[6].lower(), 0), animal_data, 0)
