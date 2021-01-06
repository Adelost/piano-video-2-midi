def get_attr_of_object(obj):
    keys = dir(obj)
    attr_map = {}
    for k in keys:
        if not k.startswith('_'):
            attr_map[k] = getattr(obj, k)
    return attr_map


def set_matching_attr_of_object(obj, args):
    for k, v in args.items():
        if hasattr(obj, str(k)):
            setattr(obj, k, v)
