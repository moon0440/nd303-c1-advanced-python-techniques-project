"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""

import csv
import json
from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """

    neo_collection = []
    with open(neo_csv_path, 'r') as f:
        for r in csv.DictReader(f):
            neo_collection.append(NearEarthObject.serialize_from_csv(csv_row_dict=r))

    return neo_collection


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """

    cad_collection = []
    with open(cad_json_path, 'r') as f:
        cad_json = json.load(f)
        for d in cad_json['data']:
            cad_dict = dict(zip(cad_json['fields'], d))
            cad_collection.append(CloseApproach.serialize_from_json(cad_dict))

    return cad_collection
