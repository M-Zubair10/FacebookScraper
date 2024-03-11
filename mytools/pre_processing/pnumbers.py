def maxN(list_to_search: list, n: int = 1) -> list:
    """
    Get top_n max numbers
    :param list_to_search: input list
    :param n: integer value that defines top_n
    :return: list of max values
    """
    
    max_vals = []
    list_to_search = list_to_search.copy()
    for i in range(n):
        _max = max(list_to_search)
        list_to_search.remove(_max)
        max_vals.append(_max)
    return max_vals


def minN(list_to_search: list, n: int = 1):
    """
    Get min_n numbers
    :param list_to_search: input list
    :param n: integer value that defines min_n
    :return: list of min values
    """

    min_vals = []
    list_to_search = list_to_search.copy()
    for i in range(n):
        _min = min(list_to_search)
        list_to_search.remove(_min)
        min_vals.append(_min)
    return min_vals


def number_augmentation(num, operators=['+'], include_self=True, max_boundary=None):
    """
    Get possible transformations
    :param num: number
    :param operators: list of operators that can be performed
    :param max_boundary: Use it only use '-' as operator
    :return:
    """
    
    augmented_numbers = []
    if include_self:
        augmented_numbers.append(num)
    for op in operators:
        input_num = num
        subset = []
        if op == '+':
            for i in range(1, num):
                input_num -= 1
                subset.append((i, input_num))
        elif op == '-':
            for i in range(1, max_boundary - input_num + 1):
                input_num += 1
                subset.append((input_num, i))
        else:
            raise Exception("Not implemented yet!")
        augmented_numbers.append(subset)
    return augmented_numbers if len(operators) > 1 else augmented_numbers[0]


if __name__ == '__main__':
    print(number_augmentation(7, operators=['+', '-'], max_boundary=10))