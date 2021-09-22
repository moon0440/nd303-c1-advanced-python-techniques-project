"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.
The `limit` function simply limits the maximum number of values produced by an
iterator.
"""

import operator
from itertools import islice


class ApproachFilter:
    """ An Approach Object filter.py

    A `ApproachFilter` is used to create an object that is used to get a boolean
    value after applying a set of conditions. It primary use is to create a filter that will
    be reused. A `CloseApproach` can be evaluated against this filter by calling the
    initialized `ApproachFilter` with a `CloseApproach` as a parameter.

    Example:
            close_approach = CloseApproach(...)
            f = ApproachFilter(value=500, op=operator.ge, approach_attr='distance')
            f(close_approach)  # => True

    In the example above a `CloseApproach` objects `.distance` attribute is checked for
    being greater than equal to 500.
    """

    def __init__(self, value, op, approach_attr, return_method=None):
        """ Creates a new `ApproachFilter`

        To create an `ApproachFilter` for later use to compare a `CloseApproach`es attributes
        against conditions. These conditions are set when initialized, and condition is tested when
        the initialized class is called with a `CloseApproach` as a parameter.

        The param return_method is a special case, currently only used on `CloseApproach`es `.time`
        attribute. After the attribute is returned from the `CloseApproach` class but before it is
        conditionally checked the return_method will be run on the returned attribute.

        :param value: Value that is used for comparison.
        :param op: Function from the operator library(https://docs.python.org/3/library/operator.html)
        :param approach_attr: Attribute on `CloseApproach` class to compare
        :param return_method: Optional value used on attributes return value.
        """
        self.value = value
        self.op = op
        self.approach_attr = approach_attr
        self.return_method = return_method if not return_method else operator.methodcaller(return_method)

    def __call__(self, approach):
        """Invoke `self(approach)` but only if the filter has an active value for comparison."""
        if self.value is not None:
            return self.op(self.get(approach, self.approach_attr, self.return_method), self.value)

        return True

    @classmethod
    def get(cls, approach, attr, return_method):
        """Get an attribute of interest from a close approach and apply return_method if set"""
        attr_value = operator.attrgetter(attr)(approach)
        return attr_value if not return_method else return_method(attr_value)


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occurred
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    filters = [
        ApproachFilter(value=date, op=operator.eq, approach_attr='time', return_method='date'),
        ApproachFilter(value=start_date, op=operator.ge, approach_attr='time', return_method='date'),
        ApproachFilter(value=end_date, op=operator.le, approach_attr='time', return_method='date'),
        ApproachFilter(value=distance_min, op=operator.ge, approach_attr='distance'),
        ApproachFilter(value=distance_max, op=operator.le, approach_attr='distance'),
        ApproachFilter(value=velocity_min, op=operator.ge, approach_attr='velocity'),
        ApproachFilter(value=velocity_max, op=operator.le, approach_attr='velocity'),
        ApproachFilter(value=diameter_min, op=operator.ge, approach_attr='neo.diameter'),
        ApproachFilter(value=diameter_max, op=operator.le, approach_attr='neo.diameter'),
        ApproachFilter(value=hazardous, op=operator.is_, approach_attr='neo.hazardous'),
    ]
    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :return: The first (at most) `n` values from the iterator using islice generator.
    """
    n = n if n else None
    return islice(iterator, n)
