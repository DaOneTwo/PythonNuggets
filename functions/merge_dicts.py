from copy import deepcopy
from collections.abc import Mapping
from typing import Dict


def merge_dicts(base_dict: Dict, merge_dict: Dict, add_keys: bool = True, with_deepcopy=True):
    """Recursively merges 2 dictionaries without altering either dictionary passed.

    Will only merge mapping objects according to same rules as all other key/values.
    If similar keys exist the value in the merge dict presides.

    add_keys = controls whether keys which are not currently in the base dict but are in the merge_dict will be placed
    in the out put dictionary.

    with_deepcopy = controls whether a deepcopy of originals are made or not.  Recursive calls will not use a deepcopy
    because we should already be working of a base deepcopy OR the caller has said they do not need one in the first
    place.
    """
    if not all([merge_dict, isinstance(merge_dict, Mapping), isinstance(base_dict, Mapping)]):
        return base_dict

    # deep copy keeps later mutations of any dicts from effecting each other good idea to use this
    m_d, b_d = merge_dict, base_dict
    if with_deepcopy is True:
        m_d, b_d = deepcopy(merge_dict), deepcopy(base_dict)

    merged = {}
    b_keys, m_keys = set(b_d), set(m_d)

    for key in b_keys:  # all keys in our base dict convey
        if all([m_d.get(key), isinstance(m_d.get(key), Mapping),
                isinstance(b_d.get(key), Mapping)]):
            # first call either has a deepcopy or not (controlled by caller) we do not need one for the recursive calls
            # This should help with memory consumption in recursive calls.
            merged[key] = merge_dicts(b_d[key], m_d[key], add_keys=add_keys, with_deepcopy=False)
        else:
            if key in m_keys:  # if key also in m_keys we must update it
                #  this handles explicit scenarios of None, empty string, and other overrides.  Rather than
                #  the .get w/default I used in my first iteration.
                merged[key] = m_d[key]
            else:
                merged[key] = b_d[key]

    if add_keys is True:
        for k in m_keys.difference(b_keys):
            merged[k] = m_d[k]

    return merged
