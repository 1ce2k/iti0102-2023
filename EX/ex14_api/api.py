"""API exercise."""
# from typing import Any
import requests
import requests.exceptions


def get_request(url: str) -> int:
    """
    Send an HTTP GET request to the specified URL.

    Return the resulting response object status code.

    :param url: The URL to which the GET request will be sent.
    :return: Server's response to the request.
    """
    return requests.get(url).status_code


def get_request_error_handling(url: str):
    """
    Send an HTTP GET request to the specified URL with error handling.

    Handle any exceptions that may occur during the request.

    :param url: The URL to which the GET request will be sent.
    :return: Server's response object or the exception object if an error occurs.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException as e:
        return e


def post_request(url: str, data: dict):
    """
    Send an HTTP POST request with JSON data to the specified URL.

    Handle any exceptions that may occur during the request.

    :param url: The URL to which the POST request will be sent.
    :param data: Dictionary to be sent along with the POST request.
    :return: Server's response json object or the exception object if an error occurs.
    """
    try:
        return requests.post(url, json=data)
    except requests.exceptions.RequestException as e:
        return e


def delete_request(url: str):
    """
    Send an HTTP DELETE request to the specified URL.

    Handle any exceptions that may occur during the request.

    :param url: The URL to which the DELETE request will be sent.
    :return: Server's response status code or the exception object if an error occurs.
    """
    try:
        return requests.delete(url).status_code
    except requests.exceptions.RequestException as e:
        return e


def stream_request(url: str) -> str:
    """
    Send an HTTP GET request to the specified URL and stream the response.

    More information:
    https://requests.readthedocs.io/en/latest/user/advanced/#streaming-requests

    Return a string containing the streamed content.

    :param url: The URL to send the GET request to.
    :return: A string containing the streamed content.
    """
    r = requests.get(url, stream=True)
    ret = ''
    for line in r.iter_lines():
        ret += str(line) + '\n'
    return ret


def get_authenticated_request(url: str, auth_token: str):
    """
    Send an authenticated HTTP GET request using the provided token.

    Note: Do not push your auth token into GIT.

    :param url: The URL to which the GET request will be sent.
    :param auth_token: The authentication token for the request.
    :return: Server's response json object or the exception object if an error occurs.

    """
    try:
        return requests.get(url, headers={'Authorization': f'Bearer {auth_token}'}).json()
    except requests.exceptions.RequestException as e:
        return e


def advanced_user_filter(url, min_followers: int, min_posts: int, min_following: int) -> list:
    """
    Fetch user data from a URL and filter based on specified criteria.

    Return specific fields for users meeting the follower, post, and following thresholds.
    Each user in the returned list has to include their username, full_name, followers, following, and posts.

    :param url: URL for user data.
    :param min_followers: Minimum followers required.
    :param min_posts: Minimum posts required.
    :param min_following: Minimum following required.
    :return: List of user data dictionaries.
    """
    data = requests.get(url).json()
    list_of_users = []
    for person in data:
        if person['following'] >= min_following and person['followers'] >= min_followers and person['posts'] >= min_posts:
            new_person = {
                'username': person['username'],
                'full_name': person['full_name'],
                'followers': person['followers'],
                'following': person['following'],
                'posts': person['posts']
            }
            list_of_users.append(new_person)
    return list_of_users


def fetch_aggregate_data(url: str) -> dict:
    """
    Process a list of JSON objects to aggregate specific data points.

    Aggregate such as the total and average number of followers,
    posts, and following for all users.

    https://cs.taltech.ee/services/ex14/json-data

    The dictionary should have the following information:
    - 'average_followers'
    - 'average_following'
    - 'average_posts'
    - 'total_followers'
    - 'total_following'
    - 'total_posts'

    :param url: URL from which to fetch user data.
    :return: Aggregated data including total and average values.
    """
    total_followers, total_following, total_posts = 0, 0, 0
    data = requests.get(url).json()
    for person in data:
        total_following += person['following']
        total_followers += person['followers']
        total_posts += person['posts']
    ret = {
        'average_followers': total_followers / len(data),
        'average_following': total_following / len(data),
        'average_posts': total_posts / len(data),
        'total_followers': total_followers,
        'total_following': total_following,
        'total_posts': total_posts
    }
    return ret
