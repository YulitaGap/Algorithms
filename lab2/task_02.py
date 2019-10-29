import math

# Starting with helper functions.


def distance_calculator(p1, p2):
    """
    (tuple,tuple) -> float
    The function for calculating distance between two points by classical formula.
    :param p1: coordinates of 1st point
    :param p2: coordinates of 2nd point
    :return: distance between 2 points given
    """
    distance = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    return distance


def perimeter_calculator(p1, p2, p3):
    """
    (tuple,tuple,tuple) -> float
    The function for calculating perimeter of triange with points coordinates given.
    :param p1: coordinates of 1st point
    :param p2: coordinates of 2nd point
    :param p3: coordinates of 3rd point
    :return: perimeter as a sum point's distances
    """
    a = distance_calculator(p1, p2)
    b = distance_calculator(p1, p3)
    c = distance_calculator(p2, p3)
    perimeter = a + b + c
    if a < b + c and b < a + c and c < a + b:  # basic triangle existence condition
        return perimeter
    else:
        return -1


def bruteforce_comparison(x_sorted):
    """
    (list) -> list, list, float
    Function for brute force comparison of distances used for <=3 points.
    :param x_sorted: points lost sorted by x coordinate.
    :return: pair with min distances coordinates, distance between them
    """
    curr_min = distance_calculator(x_sorted[0], x_sorted[1])
    p1, p2 = x_sorted[0], x_sorted[1]
    points_amount = len(x_sorted)
    if points_amount == 2:  # For only one pair of points their distance is a minimum.
        return p1, p2, curr_min
    for i in range(points_amount-1):
        for j in range(i + 1, points_amount):
            if i != 0 and j != 1:
                dist = distance_calculator(x_sorted[i], x_sorted[j])
                if dist < curr_min:  # Checking for new min distance
                    curr_min = dist
                    p1, p2 = x_sorted[i], x_sorted[j]
    return p1, p2, curr_min


def bruteforce_perimeter(x_sorted):
    """
    (list) -> float, list, list, list
    Function for brute minimal perimeter calculation.
    :param x_sorted: points list sorted by x coordinate.
    :return: triangle points coordinates and minimal perimeter value.
    """
    minp = 100000
    points_amount = len(x_sorted)
    min_point1, min_point2, min_point3 = -1, -1, -1
    for i in range(len(x_sorted)):
        for j in range(i + 1, points_amount):
            for k in range(j + 1, points_amount):
                curr_minp = perimeter_calculator(x_sorted[i], x_sorted[j], x_sorted[k])
                if curr_minp != -1 and minp > curr_minp:
                    minp = curr_minp
                    min_point1 = x_sorted[i]
                    min_point2 = x_sorted[j]
                    min_point3 = x_sorted[k]

    return minp, min_point1, min_point2, min_point3


def closest_split_pair(p_x, p_y, delta, best_pair):
    """
    Function for searching a minimal distanced points with possible delta difference.
    (list,list,float,) -> list, list, float
    :param p_x: points list sorted by x coordinates
    :param p_y: points list sorted by y coordinates
    :param delta: possible difference
    :param best_pair: current minimal distanced pair of points
    :return: pair with min distances coordinates, distance between them
    """
    points_amount_x = len(p_x)  # Storing length
    mid_x = p_x[points_amount_x // 2][0]  # Defining midpoint x coordinate of x-sorted array
    # Creating a subarray of points not further than delta from midpoint on x-sorted array
    s_y = [x for x in p_y if mid_x - delta <= x[0] <= mid_x + delta]
    best = delta  # assign best value to delta
    points_amount_y = len(s_y)  # store length of subarray for quickness
    for i in range(points_amount_y - 1):
        for j in range(i+1, min(i + 7, points_amount_y)):
            p, q = s_y[i], s_y[j]
            dst = distance_calculator(p, q)
            if dst < best:
                best_pair = p, q
                best = dst
    return best_pair[0], best_pair[1], best


def recursive_closest(x_sorted, y_sorted):
    """
    (list, list) -> list, list, float
    Recursive function to find pair of points with minimal distance
    by splitting on the middle and recursive calls for split parts.
    :param x_sorted: points list presorted by x
    :param y_sorted:points list presorted by y
    :return: pair with min distances coordinates, distance between them
    """
    points_amount = len(x_sorted)
    if points_amount <= 3:
        return bruteforce_comparison(x_sorted)
    mid_point = points_amount // 2  # Calculating middle point index
    left_x = x_sorted[:mid_point]  # Splitting for 2 parts
    right_x = x_sorted[mid_point:]

    midpoint = x_sorted[mid_point][0]  # Defining middle point

    left_y, right_y = [], []
    for point in y_sorted:
        if point[0] <= midpoint:  # Splitting for 2 parts if points:  less and bigger then middle point
            left_y.append(point)
        else:
            right_y.append(point)

    (p1, q1, left_min) = recursive_closest(left_x, left_y)  # Calling function recursively for points less then middle point
    (p2, q2, right_min) = recursive_closest(right_x, right_y)  # Calling recursively for points bigger then middle point

    # Choosing minimal distanced points from left and right parts found
    if left_min <= right_min:
        curr_min = left_min
        min_points = (p1, q1)
    else:
        curr_min = right_min
        min_points = (p2, q2)

    # Calling splitting function for points near middle
    (p3, q3, middle_min) = closest_split_pair(x_sorted, y_sorted, curr_min, min_points)

    # Choosing final minimum distanced points from left,right,middle parts
    if curr_min <= middle_min:
        return min_points[0], min_points[1], curr_min
    else:
        return p3, q3, middle_min


def closest_pair(points_list):
    """
    (list) -> float, tuple(list,list)
    Function for presorting a starting list to reduce running time value
    and calling of a main recursive function.
    :param points_list: starting list of points coordinates
    :return:minimal distance, coordinates of closest points pair
    """
    x_sorted = sorted(points_list, key=lambda x: x[0])  # Presorting by x coordinate
    y_sorted = sorted(points_list, key=lambda y: y[1])  # Presorting by y coordinate
    p1, p2, min_dist = recursive_closest(x_sorted, y_sorted)  # Call main recursive function
    return min_dist, (p1, p2)


def recursive_minp(x_sorted, y_sorted):
    """
    (list, list) -> float, list, list, list
    Recursive function to find points for triangle with minimal perimeter
    and calculating this perimeter.
    :param x_sorted: points list presorted by x
    :param y_sorted:points list presorted by y
    :return: triangle points coordinates and it's minimal perimeter value.
    """
    # print(x_sorted, y_sorted)
    points_len = len(x_sorted)
    if points_len <= 5:
        return bruteforce_perimeter(x_sorted)
    else:
        mid_point = points_len//2
        left_x, right_x = x_sorted[:mid_point], x_sorted[mid_point:]
        left_y, right_y = y_sorted[mid_point:], y_sorted[mid_point:]
        leftp, l1, l2, l3 = recursive_minp(left_x, left_y)
        rightp, r1, r2, r3 = recursive_minp(right_x, right_y)
        if leftp != -1:  # triangle exists
            if rightp != -1:  # triangle exists
                curr_min = min(leftp, rightp)
            else:
                curr_min = leftp
        else:
            curr_min = rightp

        pointer, merged = left_x[-1], []
        for i in range(points_len):
            for j in range(i + 1, min(i + 16, points_len)):
                curr_perimeter = perimeter_calculator(x_sorted[i], x_sorted[j], pointer)
                if curr_perimeter < curr_min and curr_perimeter != -1:
                    merged.append(x_sorted[i])
                    merged.append(x_sorted[j])
        merged.append(pointer)
        y_sorted_merged = sorted(merged, key=lambda y: y[1])
        minp = 2 ** 18
        min_p1, min_p2, min_p3 = -1, -1, -1
        for i in range(len(y_sorted_merged)):
            for j in range(i + 1, len(y_sorted_merged)):
                for k in range(j + 1, len(y_sorted_merged)):
                    curr_perimeter = perimeter_calculator(y_sorted_merged[i], y_sorted_merged[j], y_sorted_merged[k])
                    if curr_perimeter != -1 and minp > curr_perimeter:
                        minp = curr_perimeter
                        min_p1, min_p2, min_p3 = y_sorted_merged[i], y_sorted_merged[j],  y_sorted_merged[k]
        if minp < curr_min and min_p1 != -1:
            return minp, min_p1, min_p2, min_p3
        if l1 != -1:
            if r1 != -1:
                if leftp < rightp:
                    return leftp, l1, l2, l3
                else:
                    return rightp, r1, r2, r3
            else:
                return leftp, l1, l2, l3
        else:
            return rightp, r1, r2, r3


def minimal_perimeter(points):
    """
    (list) -> float, tuple(list,list,list)
    Function for presorting a starting list to reduce running time value
    and calling of a main recursive function.
    :param points: starting list of points coordinates
    :return:minimal perimeter value, coordinates of triangle
    """
    x_sorted = sorted(points, key=lambda x: x[0])  # Presorting by x coordinate
    y_sorted = sorted(points, key=lambda y: y[1])  # Presorting by y coordinate
    minp, min_p1, min_p2, min_p3 = recursive_minp(x_sorted, y_sorted)
    return minp, (min_p1, min_p2, min_p3)


if __name__ == '__main__':
    p = []
    with open("input_100.txt") as f:
        lines = f.readlines()[1:]
        for l in lines:
            p.append([int(l.split()[0]), int(l.split()[1])])
    print(minimal_perimeter(p))
