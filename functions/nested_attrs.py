import functools


def get_nested_attr(obj, attr, *args):
    """getattr that takes an entire object path split by "."  Works the same as getattr except walks the path.  returns
    detail if path fails anywhere along the way
    example: 'message_context.custom_data.value_pair'

    DOES NOT account for indexing or slicing into individual attrs along the way.  Admittedly this was pulled straight
    from a stack overflow and I no longer know the link to provide reference.  :-)
    """
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))