def str_to_pair_int(string):
    return zip(list(map(int, string.split(","))))

def list_to_pairs(base_list):
    """
    Convert a list of elements into a list of pairs
    :param base_list: The list of elements to convert
    :return: The list in the form of a list of elements
    """
    return list(zip(base_list[::2], base_list[1::2]))

