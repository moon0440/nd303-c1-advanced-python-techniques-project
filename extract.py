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
from helpers import cd_to_datetime
from models import NearEarthObject, CloseApproach
from enum import Enum


class HAZARDOUS(Enum):
    Y = True
    N = False


def parse_float(v):
    return float(v) if v.replace('.', '').isnumeric() else float('nan')


def parse_hazardous(v):
    return HAZARDOUS[v].value if v else False


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO_DONE: Load NEO data from the given CSV file.
    #  milestone: Task 2
    neo_collection = []
    neo_map = {
        'pdes': {'cls_param': 'designation', 'parser': str},
        'name': {'cls_param': 'name', 'parser': str},
        'pha': {'cls_param': 'hazardous', 'parser': parse_hazardous},
        'diameter': {'cls_param': 'diameter', 'parser': parse_float}
    }
    with open(neo_csv_path, 'r') as f:
        for r in csv.DictReader(f):
            neo_args = {neo_map[k]['cls_param']: neo_map[k]['parser'](v) for k, v in r.items() if k in neo_map.keys()}
            neo_collection.append(NearEarthObject(**neo_args))

    return neo_collection


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO_DONE: Load close approach data from the given JSON file.
    #  milestone: Task 2
    cad_collection = []
    cad_map = {
        'des': {'cls_param': '_designation', 'parser': str},
        'cd': {'cls_param': 'time', 'parser': cd_to_datetime},
        'dist': {'cls_param': 'distance', 'parser': parse_float},
        'v_rel': {'cls_param': 'velocity', 'parser': parse_float}
    }

    with open(cad_json_path, 'r') as f:
        cad_json = json.load(f)
        
    for d in cad_json['data']:
        cad_data = dict(zip(cad_json['fields'], d))
        cad_args = {cad_map[k]['cls_param']: cad_map[k]['parser'](v) for k, v in cad_data.items() if
                    k in cad_map.keys()}
        cad_collection.append(CloseApproach(**cad_args))

    return cad_collection
