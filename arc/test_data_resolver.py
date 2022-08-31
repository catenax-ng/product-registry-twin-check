import json
from collections import OrderedDict, namedtuple
import os

RESSOURCES_PATH = os.path.dirname(os.path.abspath(__file__))

def create_namedtuple_from_dict(obj):
    """converts given list or dict to named tuples, generic alternative to dataclass"""
    if isinstance(obj, dict):
        fields = sorted(obj.keys())
        namedtuple_type = namedtuple(
            typename='TestData',
            field_names=fields,
            rename=True,
        )
        field_value_pairs = OrderedDict(
            (str(field), create_namedtuple_from_dict(obj[field]))
            for field in fields
        )
        try:
            return namedtuple_type(**field_value_pairs)
        except TypeError:
            # Cannot create namedtuple instance so fallback to dict (invalid attribute names)
            return dict(**field_value_pairs)
    elif isinstance(obj, (list, set, tuple, frozenset)):
        return [create_namedtuple_from_dict(item) for item in obj]
    else:
        return obj


def inject_test_data(file):
    """
        Read the content of the JSON file and convert it to a named tuple,
        can be used for injecting test data set to tests, helps in separating test data from the tests
    """
    file = os.path.join(RESSOURCES_PATH, file)
    with open(file) as f:
        raw_data = json.load(f)
    return create_namedtuple_from_dict(raw_data)

