import pathfinder

def test_file_can_be_read_into_a_2d_list():
    # the first value in elevation_small is 4713
    # the last value in elevation_small is 3948
    file = open('elevation_small.txt')
    elevation_data = pathfinder.read_elevation_data_into_2d_list(file)
    assert(elevation_data[0][0] == 4713)
    assert(elevation_data[-1][-1] == 3948)


def test_max_elevation_can_be_found():
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert(pathfinder.find_max_elevation(data) == 9)


def test_min_elevation_can_be_found():
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert(pathfinder.find_min_elevation(data) == 1)


def test_alpha_value_can_be_calculated():
    min_value = 1
    max_value = 9
    assert(pathfinder.calculate_alpha_value(min_value, max_value, 9) == 255)
    assert(pathfinder.calculate_alpha_value(min_value, max_value, 1) == 0)


def test_next_pixel_can_be_found_with_greedy_algorithm():
    # 11 3  146
    # 43 56 54
    # 2  8  43
    # 48 10 112
    # 74 9  28
    two_d_list = [[11, 3, 146], [43, 56, 54], [2, 8, 43], [48, 10, 112], [74, 9, 28]]
    start_row = 3
    start_column = 0
    next_pixel_row, next_pixel_column = pathfinder.greedy_walk_to_next_pixel(two_d_list, start_row, start_column)
    assert(two_d_list[next_pixel_row][next_pixel_column] == 10)