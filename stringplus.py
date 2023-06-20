

def get_substring(start_string: str, end_string: str, data: str, contain_start=False, contain_end=False) -> str:
    if not start_string:
        pos0 = 0
    else:
        pos0 = data.find(start_string)

        if -1 == pos0:
            return ""

        if not contain_start:
            pos0 += len(start_string)

    data = data[pos0:]
    if not end_string:
        pos1 = len(data)
    else:
        pos1 = data.find(end_string)

    if -1 == pos1:
        return ""

    if contain_end:
        pos1 += len(end_string)

    data = data[:pos1]

    return data
