from datetime import datetime

import typing as List


def get_datetime(year: str, month: str, day: str) -> datetime:
    '''
    build datetime object
    :param year:
    :param month:
    :param day:
    :return: datetime object
    '''
    ex = f"{year}-{month}-{day}T00:00:00"
    return datetime.strptime(ex + "+0100", "%Y-%m-%dT%H:%M:%S%z")


def find_loc(loc: str, localities: List) -> (str, str, str):
    '''
    get coordinates for specified location
    :param loc: locality to search
    :param localities: list of all localities
    :return: coordinates of the location
    '''
    for single_loc in localities:
        if loc == single_loc["locality"]:
            return single_loc["latitude"], single_loc["longitude"], single_loc["elevation"]

