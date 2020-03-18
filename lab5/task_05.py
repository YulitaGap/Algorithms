from functools import lru_cache


@lru_cache(maxsize=None)  # caching all calls of function
def recursive_search(nitems, weight_):
    if not nitems:  # no items
        return 0
    elif items_[nitems - 1][1] > weight_:
        return recursive_search(nitems - 1, weight_)
    else:
        return max(
            recursive_search(nitems - 1, weight_),
            recursive_search(nitems - 1, weight_ - items_[nitems - 1][1])
            + items_[nitems - 1][0])


def knapsack(items, weight):
    global items_
    items_ = items
    result_list, total_value = [], 0
    for i in reversed(range(len(items))):
        if recursive_search(i + 1, weight) > recursive_search(i, weight):
            total_value += items[i][0]
            result_list.append(i)
            weight -= items[i][1]
    return total_value, sorted(result_list)