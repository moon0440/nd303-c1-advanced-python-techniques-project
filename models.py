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

You'll edit this file in Task 1.
"""
import datetime
from math import isnan
from helpers import cd_to_datetime, datetime_to_str
from enum import Enum


class HAZARDOUS(Enum):
    Y = True
    N = False


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

    # TODO_IGNORE: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, designation: str, name: str = '', hazardous: bool = False, diameter: float = float('nan')):
        """Create a new `NearEarthObject`.

        :param string designation: The primary designation for this NearEarthObject.
        :param string name: The IAU name for this NearEarthObject. Not all NearEarthObject in dataset have a name
        :param float diameter: The diameter, in kilometers, of this NearEarthObject.
        :param bool hazardous: Whether or not this NearEarthObject is potentially hazardous.
        """
        # TODO_DONE: Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        self.designation = designation
        self.name = name if name else None
        self.diameter = diameter
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # TODO_DONE: Use self.designation and self.name to build a fullname for this object.
        return f'{self.designation} ({self.name})' if self.name else f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        # TODO_DONE: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.

        """ Orginal suggested output"""
        # return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km " \
        #        f"and {['is not', 'is'][int(self.hazardous)]} potentially hazardous."

        """ Improved handling for case diameter is unknown """
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
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    # TODO_IGNORE: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, _designation: str = '', time: datetime.datetime = None, distance: float = float('nan'),
                 velocity: float = float('nan')):
        """Create a new `CloseApproach`.

        :param datetime time: The date and time, in UTC, at which the NEO passes closest to Earth.
        :param float distance: The nominal approach distance, in astronomical units, of the NEO to Earth at the closest point.
        :param float velocity: The velocity, in kilometers per second, of the NEO relative to Earth at the closest point.
        :param NearEarthObject neo: The NearEarthObject that is making a close approach to Earth.
        """
        # TODO_DONE: Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self._designation = _designation
        self.time = time  # TODO_DONE: Use the cd_to_datetime function for this attribute.
        self.distance = distance
        self.velocity = velocity

        # Create an attribute for the referenced NEO, originally None.
        self._neo = None

    @property
    def neo(self):
        return self._neo

    @neo.setter
    def neo(self, neo_obj: NearEarthObject):
        # TODO: Document neo setter function
        #  milestone: 2
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
        # TODO_DONE: Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        return datetime_to_str(self.time)

    @property
    def fullname(self):
        """Return a representation of the full name of this CloseApproach."""
        # TODO_DONE: Use self.designation and self.name to build a fullname for this object.
        #   Enable below once self.neo has been implemented
        fullname = f'{self._designation}'
        if self._neo and self._neo.name:
            fullname += f' ({self._neo.name})'

        return fullname

    def __str__(self):
        """Return `str(self)`."""
        # TODO_DONE: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"At {datetime_to_str(self.time)}, {repr(self._designation)} approaches Earth at a " \
               f"distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."
        # return f"At {self.time}, {repr(self.neo.fullname)} approaches Earth at a " \
        #        f"distance of {self.distance} au and a velocity of {self.velocity} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        # TODO_DONE: Extra - Replace !r with repr(x)
        #  https://www.python.org/dev/peps/pep-0498/#s-r-and-a-are-redundant
        return (f"CloseApproach(time={repr(self.time_str)}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={repr(self.neo)})")
