def insertion_sort(array):
    """
    (list) -> int
    Function for insertion sort realisation
    Returns the amount of comparison operations while running algorithm.
    """
    comparison_num = 0
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            comparison_num += 1
            array[j + 1] = array[j]
            j -= 1
        comparison_num += 1
        array[j + 1] = key
    return comparison_num


def shell_sort(array):
    """
    (list) -> int
    Function for shell sort realisation
    Returns the amount of comparison operations while running algorithm.
    """
    comparison_num = 0
    gap = len(array) // 2
    while gap > 0:
        for i in range(gap, len(array)):
            cur_value = array[i]
            j = i
            while j >= gap and array[j - gap] > cur_value:
                array[j] = array[j - gap]
                j -= gap
                comparison_num += 1
            array[j] = cur_value
            comparison_num += 1
        gap //= 2
    return comparison_num


def selection_sort(array):
    """
    (list) -> int
    Function for selection sort realisation
    Returns the amount of comparison operations while running algorithm.
    """
    comparison_num = 0
    for i in range(len(array)):
        min_position = i
        for j in range(i + 1, len(array)):
            if array[min_position] > array[j]:
                min_position = j
            comparison_num += 1
        temp = array[i]
        array[i] = array[min_position]
        array[min_position] = temp
    return comparison_num