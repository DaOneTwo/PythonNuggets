from collections.abc import Mapping
from typing import Dict


def merge_dicts(base_dict: Dict, merge_dict: Dict, add_keys: bool = True):
    """Recursively merges 2 dictionaries without altering either dictionary passed.

    Will only merge mapping objects according to same rules as all other key/values.
    If similar keys exist the value in the merge dict presides.

    add_keys = controls whether keys which are not currently in the base dict but are in the merge_dict will be placed
    in the out put dictionary.
    """
    if not all([merge_dict, isinstance(merge_dict, Mapping), isinstance(base_dict, Mapping)]):
        return base_dict

    merged = {}
    b_keys, m_keys = set(base_dict), set(merge_dict)

    for key in b_keys:  # all keys in our base dict convey
        if all([merge_dict.get(key), isinstance(merge_dict.get(key), Mapping),
                isinstance(base_dict.get(key), Mapping)]):
            merged[key] = merge_dicts(base_dict[key], merge_dict[key], add_keys=add_keys)
        else:
            if key in m_keys:  # if key also in m_keys we must update it
                #  this handles explicit scenarios of None, empty string, and other overrides.  Rather than
                #  the .get w/default I used in my first iteration.
                merged[key] = merge_dict[key]
            else:
                merged[key] = base_dict[key]

    if add_keys is True:
        for k in m_keys.difference(b_keys):
            merged[k] = merge_dict[k]

    return merged
