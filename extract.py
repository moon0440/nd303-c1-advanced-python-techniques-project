"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO_DONE: Load NEO data from the given CSV file.
    #  milestone: Task 2
    neo_collection = []
    csv_header_map = {'pdes': 'designation', 'name': 'name', 'pha': 'hazardous', 'diameter': 'diameter'}
    with open(neo_csv_path, 'r') as f:
        for r in csv.DictReader(f):
            neo_args = {csv_header_map[k]: v for k, v in r.items() if k in csv_header_map.keys()}
            neo_collection.append(NearEarthObject(**neo_args))

    return neo_collection


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    #  milestone: Task 2
    return ()
