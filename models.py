"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""

import datetime
from math import isnan
from operator import attrgetter

from helpers import cd_to_datetime, datetime_to_str, float_or_nan


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation: str = '', name: str = None, hazardous: bool = False,
                 diameter: float = float('nan')):
        """Create a new `NearEarthObject`.

        :param string designation: The primary designation for this NearEarthObject.
        :param string name: The IAU name for this NearEarthObject. Not all NearEarthObject in dataset have a name
        :param float diameter: The diameter, in kilometers, of this NearEarthObject.
        :param bool hazardous: Whether or not this NearEarthObject is potentially hazardous.
        """
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous

        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f'{self.designation} ({self.name})' if self.name else f'{self.designation}'

    @property
    def serialize_to_json(self):
        """Converts instance to a dict using the required json output field names. """
        json_output_map = {'designation': 'designation',
                           'name': 'name',
                           'diameter_km': 'diameter',
                           'potentially_hazardous': 'hazardous'
                           }
        return {k: attrgetter(v)(self) for k, v in json_output_map.items()}

    @classmethod
    def serialize_from_csv(cls, csv_row_dict: dict):
        """ Mapping csv header to class attributes & types
                -> csv_input_field:(class_attribute_name, target_type)
        """
        csv_input_map = {
            'pdes': ('designation', str),
            'name': ('name', lambda x: None if not x else x),
            'pha': ('hazardous', lambda x: False if not x else {'Y': True, 'N': False}[x]),
            'diameter': ('diameter', float_or_nan)
        }
        kwargs = {v[0]: v[1](csv_row_dict[k]) for k, v in csv_input_map.items()}
        return cls(**kwargs)

    def __str__(self):
        """Return `str(self)`."""
        diameter_string = "an unknown diameter" if isnan(self.diameter) else f"a diameter of {self.diameter:.3f} km"
        return f"NEO {self.fullname} has {diameter_string} and " \
               f"{['is not', 'is'][int(self.hazardous)]} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={repr(self.designation)}, name={repr(self.name)}, "
                f"diameter={self.diameter:.3f}, hazardous={repr(self.hazardous)})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, _designation: str = '', time: datetime.datetime = None, distance: float = float('nan'),
                 velocity: float = float('nan')):
        """Create a new `CloseApproach`.

        :param datetime time: The date and time, in UTC, at which the NEO passes closest to Earth.
        :param float distance: The nominal approach distance, in astronomical units, of the NEO to
            Earth at the closest point.
        :param float velocity: The velocity, in kilometers per second, of the NEO relative
            to Earth at the closest point.
        :param NearEarthObject neo: The NearEarthObject that is making a close approach to Earth.
        """
        self._designation = _designation
        self.time = time
        self.distance = distance
        self.velocity = velocity

        self._neo = None

    @property
    def neo(self):
        """ Return neo private attribute """
        return self._neo

    @neo.setter
    def neo(self, neo_obj: NearEarthObject):
        """ Set private neo attribute and update approaches"""
        self._neo = neo_obj
        neo_obj.approaches.append(self)

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    @property
    def fullname(self):
        """Return a representation of the full name of this CloseApproach."""
        fullname = f'{self._designation}'
        if self._neo and self._neo.name:
            fullname += f' ({self._neo.name})'

        return fullname

    @property
    def serialize_to_csv(self):
        """ Converts instance to a dict using the required csv output field names. """
        csv_output_map = {'datetime_utc': 'time_str',
                          'distance_au': 'distance',
                          'velocity_km_s': 'velocity',
                          'designation': 'neo.designation',
                          'name': 'neo.name',
                          'diameter_km': 'neo.diameter',
                          'potentially_hazardous': 'neo.hazardous'
                          }
        return {k: attrgetter(v)(self) for k, v in csv_output_map.items()}

    @property
    def serialize_to_json(self):
        """ Converts instance to a dict using the required json output field names. """
        json_output_map = {'datetime_utc': 'time_str',
                           'distance_au': 'distance',
                           'velocity_km_s': 'velocity',
                           'neo': 'neo.serialize_to_json',
                           }
        return {k: attrgetter(v)(self) for k, v in json_output_map.items()}

    @classmethod
    def serialize_from_json(cls, json_dict: dict):
        """ Mapping json keys to class attributes & types
                -> csv_input_field:(class_attribute_name, target_type)
        """
        json_input_map = {
            'des': ('_designation', str),
            'cd': ('time', cd_to_datetime),
            'dist': ('distance', float_or_nan),
            'v_rel': ('velocity', float_or_nan)
        }
        kwargs = {v[0]: v[1](json_dict[k]) for k, v in json_input_map.items()}
        return cls(**kwargs)

    def __str__(self):
        """Return `str(self)`."""
        return f"At {datetime_to_str(self.time)}, {repr(self._designation)} approaches Earth at a " \
               f"distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={repr(self.time_str)}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={repr(self.neo)})")
