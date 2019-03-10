def string_modify(_string, _index, _new_value):
    _string = _string[:_index] + _new_value + _string[_index + 1:]
    return _string


def string_switch(_string, _index1, _index2):
    helper = _string[_index1]
    _string = string_modify(_string, _index1, _string[_index2])
    _string = string_modify(_string, _index2, helper)
    return _string
